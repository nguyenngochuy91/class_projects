import java.io.*;
import java.net.*;
import java.util.*;
public class Server_TCP {

	public static void main(String[] args) throws Exception {
		String port_string = args[0];
	    int port = Integer.parseInt(port_string);
	    ServerSocket socket = new ServerSocket(port); // initiate tcp socket
	    while(true)
        {
           Socket connectionSocket = socket.accept();
           BufferedReader inFromClient =
              new BufferedReader(new InputStreamReader(connectionSocket.getInputStream()));
           DataOutputStream outToClient = new DataOutputStream(connectionSocket.getOutputStream());
           String clientSentence = inFromClient.readLine();
           System.out.println("Received: " + clientSentence);
           String capitalizedSentence = clientSentence.toUpperCase() + '\n';
           outToClient.writeBytes(capitalizedSentence);
        }
	}

}
