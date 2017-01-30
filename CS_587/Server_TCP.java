import java.io.*;
import java.net.*;

class TCPServer
{
   public static void main(String argv[]) throws Exception
      {
         String clientSentence;
         String capitalizedSentence;
         ServerSocket welcomeSocket = new ServerSocket(8888);

         while(true)
         {
            Socket connectionSocket = welcomeSocket.accept();
            byte[] send = new byte[1024];
            BufferedReader inFromClient =
               new BufferedReader(new InputStreamReader(connectionSocket.getInputStream()));
            DataOutputStream outToClient = new DataOutputStream(connectionSocket.getOutputStream());
            clientSentence = inFromClient.readLine();
            System.out.println("Received: " + clientSentence);
            capitalizedSentence = clientSentence.toUpperCase() + '\n';
            System.out.println("Sent: " + capitalizedSentence);
            send = capitalizedSentence.getBytes();
            outToClient.write(send);
         }
      }
}
