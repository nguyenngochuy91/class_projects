import java.io.*;
import java.net.*;
import java.util.*;


class Server_UDP
{
   public static void main(String args[]) throws Exception
   {	
	    int port = 8888;
        DatagramSocket socket = new DatagramSocket(port); // initiate udp socket
        Map<Integer, Status> client_IDs = new Hashtable<Integer, Status>(); // hash table with key = client ID, value is the status
        

        System.out.println("Starting server with port: 8888");
        while (true)
        {	byte[] receive = new byte[1024]; // reinitiate every time so it wont store extra thing
        	DatagramPacket receivePacket = new DatagramPacket(receive, receive.length); // initialize empty packet
        	socket.receive(receivePacket); // receive packet from the port
        	String mess = new String(receivePacket.getData());
        	System.out.println("Server has receive this mess:" + mess);
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
        	if (client_IDs.containsKey(bacon.ID))
        	{
        		Status New_Client_Status = new Status(0, false, false, bacon.StartUpTime);
        		client_IDs.put(bacon.ID,client_IDs.get(bacon.ID).update_status(New_Client_Status));
        	}
        	else
        	{
        		// put my beautiful bacon into the hashtable
        		System.out.println("New client is spawn with ID:"+String.valueOf(bacon.ID)+" at time:"+String.valueOf(bacon.StartUpTime));
        		client_IDs.put(bacon.ID, new Status(0, false, false, bacon.StartUpTime));
        		new Thread(new ClientAgent(cmdPort)).start();
        	}
        	
//        	if (client_IDs.get(bacon.ID).dead)
//        	{
//        		break;
//        	}
        		

        		
        }
        // socket.close();
   }
}

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
        try 
        {
			BufferedReader inFromAgent =
			   new BufferedReader(new InputStreamReader(TCP_socket.getInputStream()));
		} 
        catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
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
        String message = "Hello friend!!! \n";
        System.out.println("Sent: " + message);
        send = message.getBytes();
        try 
        {
			outToAgent.write(send);
		} catch (IOException e) {
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
{	int Missed_Beacon = 0; // ranging from 0 to 2, if 2 then this agent is dead
	boolean dead = false; // boolean for status is dead
	boolean restarted = false; // boolean for status restarted
	int Time;

	public Status(int missed, boolean gone, boolean revived, int time)
		{
			Missed_Beacon = missed;
			dead = gone;
			restarted = revived;
			Time = time;
		}
	
	public Status update_status(Status new_status)
	{
		// update missed beacon
		Missed_Beacon += new_status.Missed_Beacon;
		if (Missed_Beacon >= 2)
		{
			dead = true; 
		}
		if (Time != new_status.Time)
		{
			restarted = true; // update restarted
		}
		Time = new_status.Time; // update new Time
		return new Status(Missed_Beacon,dead,restarted,Time);
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
