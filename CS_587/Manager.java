import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.TimeUnit;



class Manager
{
   public static void main(String args[]) throws Exception
   {	
	    int port = 8888;
        DatagramSocket socket = new DatagramSocket(port); // initiate udp socket
        Map<Integer, Status> client_IDs = new Hashtable<Integer, Status>(); // hash table with key = client ID, value is the status
        

        System.out.println("Starting server with port: 8888");
        Thread my_beacon_listener = new Thread(new BeaconListener(socket, client_IDs));
        Thread my_agent_monitor   = new Thread(new AgentMonitor(client_IDs, 10));
        my_beacon_listener.start();
        my_agent_monitor.start();  
        my_beacon_listener.join();
        my_agent_monitor.join();
        
   }
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////
// thread classes
// Agent Monitor Thread 
class AgentMonitor implements Runnable{
	Map<Integer, Status> client_IDs;
	int waiting_time;
	public AgentMonitor(Map<Integer, Status> array_client_IDs,int Wait)
	{
		client_IDs = array_client_IDs;
		waiting_time = Wait; // wait 10 secs
	}
	public void run()
	{
		while (true) // keep looping through client_IDs every 10 secs and update status
		{
			// get the current time to compare
			long time = System.currentTimeMillis()/1000;
			// going through the array_client_IDs
			synchronized (client_IDs) 
			{
				for (int client_ID: client_IDs.keySet())
				{
					Status client_ID_Status = client_IDs.get(client_ID);
					if (!client_ID_Status.is_dead()) // if the client is alive from the last time
					{
						// check if the number of receive is less than 2 from expected
						int value =(int) (time - client_ID_Status.Time_stamp)/waiting_time;
						if (value - client_ID_Status.Received_Beacon >=2)
						{	
							System.out.println("expected number of beacon:"+Integer.toString(value));
							System.out.println("received number of beacon:"+Integer.toString(client_ID_Status.Received_Beacon));
							// it means we miss 2 beacon
							client_ID_Status.dead = true;
							System.out.println("Client ID "+Integer.toString(client_ID)+" just died");
						}
						else 
						{
							// check if the time start up is differen
							// if it is, means that the client is terminated then re run immediately
							if (client_ID_Status.previous_startup_time!= client_ID_Status.new_start_up_time)
							{
								client_ID_Status.restarted 			   = true;
								// have to set previous start up equal to new start up
								client_ID_Status.previous_startup_time = client_ID_Status.new_start_up_time;
								// have to reset timestamp
								client_ID_Status.Time_stamp 	       = time;
								client_ID_Status.Received_Beacon	   = 1;
								System.out.println("Client ID "+Integer.toString(client_ID)+" just restarted ");
							}
						}
					}
					else
					{
						if (client_ID_Status.previous_startup_time!= client_ID_Status.new_start_up_time)
						{
							client_ID_Status.restarted 			   = true;
							client_ID_Status.dead  				   = false; // it is not dead
							// have to set previous start up equal to new start up
							client_ID_Status.previous_startup_time = client_ID_Status.new_start_up_time;
							// have to reset timestamp
							client_ID_Status.Time_stamp 	       = time;
							client_ID_Status.Received_Beacon	   = 1;
							System.out.println("Client ID "+Integer.toString(client_ID)+" was dead and restarted ");

						}
					}
				}
			}
			// wait for the amount of waiting time
//			try 
//			{
//				wait(waiting_time);
//			} 
//			catch (InterruptedException e) 
//			{
//				// TODO Auto-generated catch block
//				e.printStackTrace();
//			}
		}
		
	}
}

// BeaconListener Thread
class BeaconListener implements Runnable{
	DatagramSocket UDP_socket = null;
	Map<Integer, Status> client_IDs;
	public BeaconListener(DatagramSocket socket,Map<Integer, Status> array_client_IDs)
	{
		UDP_socket = socket;
		client_IDs = array_client_IDs;
	}
	public void run() 
	{
		while (true)
        {	
			byte[] receive = new byte[1024]; // reinitiate every time so it wont store extra thing
        	DatagramPacket receivePacket = new DatagramPacket(receive, receive.length); // initialize empty packet
        	try {
				UDP_socket.receive(receivePacket);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} // receive packet from the port
        	String mess = new String(receivePacket.getData());
        	// System.out.println("Server has receive this mess:" + mess);
        	// look into the info of the packet to send back this UDP
        	
        	// parse this mess into BEACON structure
        	String[] parts = mess.split(",");
        	int cmdPort = Integer.parseInt(parts[6].trim()); // have to trim
        	
        	int[] IP_address = new int[4];
        	for (int i=0;i<4;i++)
        	{
        		IP_address[0] = Integer.parseInt(parts[i+2]);
        	}
        	// create a BEACON object
        	BEACON bacon = new BEACON(Integer.parseInt(parts[0]), Integer.parseInt(parts[1]),IP_address, cmdPort);
        	System.out.println("Successful receiving the BEACON from client ID:"+parts[0]);
        	// check if the ID is already in the HashTable
        	// have to syncrhonized
        	synchronized (client_IDs) 
				
        	{
	        	if (client_IDs.containsKey(bacon.ID))
	        	{
	        		// just update the current status: number of received beacon
	        		// and  new previous_startup_time swap with last new_start_up_time
	        		// and  new new_start_up_time updated with bacon startuptime
	        		Status current_status = client_IDs.get(bacon.ID);
	        		int beacon_num = current_status.Received_Beacon+1;
	        		client_IDs.put(bacon.ID, 
	        				new Status(beacon_num, current_status.dead, current_status.restarted
	        						, current_status.new_start_up_time, bacon.StartUpTime, current_status.Time_stamp,
	        						current_status.CmdPort));
	        		
	        	}
	        	else
	        	{
	        		// put my beautiful bacon into the hashtable
	        		System.out.println("New client is spawn with ID:"+String.valueOf(bacon.ID)+" at time:"+String.valueOf(bacon.StartUpTime));
	        		long time = System.currentTimeMillis()/1000;
	        		System.out.println("Received Beacon at system time:"+Long.toString(time));
	        		client_IDs.put(bacon.ID, new Status(1, false, false, bacon.StartUpTime, bacon.StartUpTime, time,cmdPort));
	        		Thread my_client_agent = new Thread(new ClientAgent(cmdPort));
	        		my_client_agent.start();
	        		try 
	        		{
						my_client_agent.join();
					} catch (InterruptedException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
	        	}
        	}
              		
        }
		}
	
	
}

// ClientAgent Thread
class ClientAgent implements Runnable {
	Socket TCP_socket = null;
	int tcp_port;
	public ClientAgent(int port) 
	{
		tcp_port = port; // set the port that agent listen to

	}
	public void run()
		{	
		try 
		{
			TCP_socket = new Socket("127.0.0.1", tcp_port);
		} 
		catch (IOException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		InetAddress my_address = TCP_socket.getInetAddress(); //address
        System.out.print("Connecting on : "+my_address.getHostAddress()+" with hostname : "+my_address.getHostName()+"\n" );
        byte[] send = new byte[1024];
        byte[] receive = new byte[1024];
        String sentence;
        DataOutputStream outToAgent = null;
		try 
		{
			outToAgent = new DataOutputStream(TCP_socket.getOutputStream());
		} 
		catch (IOException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        String message = "Give me your OSSSSSSS and system time!!! \n";
//        System.out.println("Sent: " + message);
        send = message.getBytes();
        try 
        {
			outToAgent.write(send);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        try 
        {
			BufferedReader inFromAgent =
			   new BufferedReader(new InputStreamReader(TCP_socket.getInputStream()));
			sentence = inFromAgent.readLine();
			System.out.println(sentence);
		} 
        catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////
// helper classes
// class BEACON to store struct from the client ID
class BEACON
{	int ID;
	int StartUpTime;
	int[] IP;
	int CmdPort;
	public BEACON(int client_ID, int Client_StartUpTime, int[] client_IP, int client_port)
	{
		ID = client_ID;
		StartUpTime = Client_StartUpTime;
		IP = client_IP;
		CmdPort = client_port;
		
	}
}

// class status to store the status of an agent
class Status
{	int Received_Beacon = 0; // number of received beacon until now
	boolean dead = false; // boolean for status is dead
	boolean restarted = false; // boolean for status restarted
	int previous_startup_time; // for angentMonitor to check and BEaconListener just update
	int new_start_up_time;
	long Time_stamp; // use this and a local time to calculated the expected number of beacon
	int CmdPort;
	public Status(int received, boolean gone, boolean revived, int previous, int current ,long time_stamp, int udp_port)
		{
			Received_Beacon 	  = received;
			dead 				  = gone;
			restarted = revived;
			previous_startup_time = previous;
			new_start_up_time     = current;
			Time_stamp 			  = time_stamp;
			CmdPort 			  = udp_port;
		}
	
	
	public boolean is_dead()
	{
		return dead;
	}
	
	public boolean is_restarted()
	{
		return restarted;
	}
}
