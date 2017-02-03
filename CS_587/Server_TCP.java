import java.io.*;
import java.net.*;

class TCPServer
{
   public static void main(String argv[]) throws Exception
      {
         String capitalizedSentence;
         Socket socket = new Socket("127.0.0.1", 10000); // hard code for now, will receive info
         // from Beacon
         InetAddress my_address = socket.getInetAddress(); //address
         System.out.print("Connecting on : "+my_address.getHostAddress()+" with hostname : "+my_address.getHostName()+"\n" );

            byte[] send = new byte[1024];
            BufferedReader inFromAgent =
               new BufferedReader(new InputStreamReader(socket.getInputStream()));
            DataOutputStream outToAgent = new DataOutputStream(socket.getOutputStream());
            capitalizedSentence = "Hello friend!!! \n";
            System.out.println("Sent: " + capitalizedSentence);
            send = capitalizedSentence.getBytes();
            outToAgent.write(send);
         
      }
}
