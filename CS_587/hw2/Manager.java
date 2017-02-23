package hw2;
import java.io.*;
import java.math.BigInteger;
import java.net.*;
import java.nio.charset.Charset;
import java.util.*;
// javac -cp .  hw2/Manager.java
// java hw2/Manager
public class Manager {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		// testing GetLocalTime 
		GetLocalTime my_obj_1 = new GetLocalTime();
		System.out.println("valid:"+my_obj_1.valid);
		System.out.println("time:"+my_obj_1.time);
		my_obj_1.valid.setValue(0);
		my_obj_1.execute("127.0.0.1", 8888);
		int time = my_obj_1.time.getValue();
		// print out time
		System.out.println("Time "+ time);
		// testing GetLocalTime 
//		GetLocalOS my_obj_2 = new GetLocalOS();	
//		my_obj_2.valid.setValue(0);
//		my_obj_2.execute("127.0.0.1", 8888);	
//		String os = my_obj_2.os.getValue();				
//		// print out time
//		System.out.println("Os "+ os);

	}

}

//class GetLocalTime 
class GetLocalTime
{
	c_int time;
	c_char valid;
	// helper function to allocate parameter , function id, parameter length into a given buf
	public void allocate(byte[] buf,int length)
	{
		// create a binary buffer
		byte[] length_to_byte = BigInteger.valueOf(length).toByteArray();
		// make a buf of this size
		// marshall parameter into buffer
		// name of our function
		String function_name = "GetLocalTime";
		byte[] function_name_to_byte = function_name.getBytes(Charset.forName("UTF-8"));
		// assign the function name byte value to our buf
		for (int i = 0; i<function_name.length();i++)
		{
			buf[i] = function_name_to_byte[i];
		}
		// assign the length of cmdbuf into our buf 
		for (int i = 100; i<length_to_byte.length;i++) // why here is .length but not .length() 
		{
			buf[i] = length_to_byte[i];
		}
		// offset that accounts for function name length and parameter length
		int offset     = 104; 
		// byte for time, and valid
		byte[] time_byte  = time.toByte();
		for (int i = offset; i<time.getSize();i++) // why here is .length but not .length() 
		{
			buf[i] = time_byte[i];
		}
		byte[] valid_byte = valid.toByte();
		offset+= time.getSize();
		for (int i = offset; i<valid.getSize();i++) // why here is .length but not .length() 
		{
			buf[i] = valid_byte[i];
		}
	}
	public int execute(String IP, int port) {
		int parameter_length = time.getSize() + valid.getSize();
		byte[] buf = new byte[100+4+parameter_length];
		allocate(buf,parameter_length);
		
		// send/receive buffer to/from RPC server
		Socket s    =  CreateSocket(IP,port);
		SendPacket(s, buf, buf.length);
		RecvPacket(s, buf, buf.length);
		
		// set parameter according to the buffer
		time.setValue(Arrays.copyOfRange(buf,100,time.getSize()+99));
		valid.setValue(Arrays.copyOfRange(buf,time.getSize()+100,99+valid.getSize()+time.getSize()));
		return time.getValue(); // get the value of time
	};
	
	// method CreateSocket that return a TCP socket
	public Socket CreateSocket(String IP, int port)
	{
		Socket TCP_socket = null;
		try 
		{
			TCP_socket = new Socket(IP, port);
		} 
		catch (IOException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return TCP_socket;
	}
	
	// medthod to send buf using socket s
	public void SendPacket(Socket s, byte[] buf, int size)
	{
		// define an output steam to send
		DataOutputStream outToAgent = null;
		try 
		{
			outToAgent = new DataOutputStream(s.getOutputStream());
		} 
		catch (IOException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		// send the buf 
     try 
     {
			outToAgent.write(buf);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	// medthod to receive buf using socket s
	public void RecvPacket(Socket s, byte[] buf, int size)
	{
		buf = new byte[size]; // flush the thing for new info
		try 
     {
			InputStream stream = s.getInputStream();// get the input as array of byte 
			// get the info from inFromAgent into our buf
			int length         = stream.read(buf); // does this read as the format we want?
		} 
     catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
}


// class GetLocalOS
class GetLocalOS
{
	c_os   os;
	c_char valid;
	// helper function to allocate parameter , function id, parameter length into a given buf
	public void allocate(byte[] buf,int length)
	{
		// create a binary buffer
		byte[] length_to_byte = BigInteger.valueOf(length).toByteArray();
		// make a buf of this size
		// marshall parameter into buffer
		// name of our function
		String function_name = "GetLocalTime";
		byte[] function_name_to_byte = function_name.getBytes(Charset.forName("UTF-8"));
		// assign the function name byte value to our buf
		for (int i = 0; i<function_name.length();i++)
		{
			buf[i] = function_name_to_byte[i];
		}
		// assign the length of cmdbuf into our buf 
		for (int i = 100; i<length_to_byte.length;i++) // why here is .length but not .length() 
		{
			buf[i] = length_to_byte[i];
		}
		// offset that accounts for function name length and parameter length
		int offset     = 104; 
		// byte for time, and valid
		byte[] os_byte  = os.toByte();
		for (int i = offset; i<os.getSize();i++) // why here is .length but not .length() 
		{
			buf[i] = os_byte[i];
		}
		byte[] valid_byte = valid.toByte();
		offset+= os.getSize();
		for (int i = offset; i<valid.getSize();i++) // why here is .length but not .length() 
		{
			buf[i] = valid_byte[i];
		}
	}
	public String execute(String IP, int port) {
		int parameter_length = os.getSize() + valid.getSize();
		byte[] buf = new byte[100+4+parameter_length];
		allocate(buf,parameter_length);
		
		// send/receive buffer to/from RPC server
		Socket s    =  CreateSocket(IP,port);
		SendPacket(s, buf, buf.length);
		RecvPacket(s, buf, buf.length);
		
		// set parameter according to the buffer
		os.setValue(Arrays.copyOfRange(buf,100,os.getSize()+99));
		valid.setValue(Arrays.copyOfRange(buf,os.getSize()+100,99+valid.getSize()+os.getSize()));
		return os.getValue(); // get the value of time
	};
	
	// method CreateSocket that return a TCP socket
	public Socket CreateSocket(String IP, int port)
	{
		Socket TCP_socket = null;
		try 
		{
			TCP_socket = new Socket(IP, port);
		} 
		catch (IOException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return TCP_socket;
	}
	
	// medthod to send buf using socket s
	public void SendPacket(Socket s, byte[] buf, int size)
	{
		// define an output steam to send
		DataOutputStream outToAgent = null;
		try 
		{
			outToAgent = new DataOutputStream(s.getOutputStream());
		} 
		catch (IOException e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		// send the buf 
        try 
        {
			outToAgent.write(buf);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	// medthod to receive buf using socket s
	public void RecvPacket(Socket s, byte[] buf, int size)
	{
		buf = new byte[size]; // flush the thing for new info
		try 
        {
			InputStream stream = s.getInputStream();// get the input as array of byte 
			// get the info from inFromAgent into our buf
			int length         = stream.read(buf); // does this read as the format we want?
		} 
        catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
}

// class c_int
class c_int
{
    byte[] buf = new byte[4]; // little endian
    
    public int getSize()
    {
    	return buf.length;
    }
    public int getValue()
    {
    	return new BigInteger(buf).intValue(); // need to remember
    }
    public void setValue(byte[] buf)
    {
    	this.buf = buf;
    }
    public void setValue(int v)
    {
    	BigInteger bigInt = BigInteger.valueOf(v);
    	buf 			  = bigInt.toByteArray();
    }
    public byte[] toByte()
    {
    	return buf;
    }
}

//class c_char
class c_char
{
    byte[] buf = new byte[1]; // little endian
    public int getSize()
    {
    	System.out.println("295");
    	System.out.println(buf.length);
    	return buf.length;
    }
    public int getValue()
    {
    	return new BigInteger(buf).intValue(); // need to remember
    }
    public void setValue(byte[] buf)
    {
    	this.buf = buf;
    }
    public void setValue(int v)
    {
    	
    	BigInteger bigInt = BigInteger.valueOf(v);
    	System.out.println("value of v:"+v);
    	buf 			  = bigInt.toByteArray();
    }
    public byte[] toByte()
    {
    	return buf;
    }
}

//class c_os
class c_os
{
    byte[] buf = new byte[10]; // little endian
    
    public int getSize()
    {
    	return buf.length;
    }
    public String getValue()
    {
    	return new BigInteger(buf).toString(); // need to remember
    }
    public void setValue(byte[] buf)
    {
    	this.buf = buf;
    }
    public void setValue(int v)
    {
    	BigInteger bigInt = BigInteger.valueOf(v);
    	buf 			  = bigInt.toByteArray();
    }
    public byte[] toByte()
    {
    	return buf;
    }
}

