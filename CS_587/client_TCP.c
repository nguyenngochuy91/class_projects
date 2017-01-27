#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h> // socket library
#include <netinet/in.h> // netinet library
#include <time.h>  // to time

#define SIZE 1024  //Max size of buffer
int main(int argc, char *argv[])
{

    int cSock;
    int PORT = atoi(argv[2]);
    char *SERVER = argv[1]; // server string, suposely 127.0.0.1 for local network

    char buffer_receive[SIZE] ; // variable to receive from server
    char buffer_send[SIZE] ; // variable to send to server

    // intializing the socket
    if ((cSock = socket(AF_INET, SOCK_STREAM, 0)) <0)
    {
    	perror("socket");
    	printf("Failed to create socket \n");
    	abort();
    }
    // variable for address
    struct sockaddr_in sin;
	int slen=sizeof(sin);
	memset((char *) &sin, 0, sizeof(sin)); // allocate memory
	sin.sin_family = AF_INET;
	sin.sin_port = htons(PORT);

	if (inet_aton(SERVER, &sin.sin_addr) == 0)
	{
		printf("Fail to get to server\n");
		abort();
	}

	// send packet
	int send_packets(char *buffer_send, int buffer_len)
	{
		int sent_bytes = send(cSock, buffer_send,buffer_len,0);
		printf("message send: %s",buffer_send);
		if (sent_bytes <0)
		{
			printf("cannot send.\n");
		}
		return 0;
	}

	// receive packet
	int receive_packets(char *buffer_receive, int bytes)
	{
		int received =0;
		int total =0 ;
		while (bytes !=0)
		{
			received = recv(cSock, &buffer_receive[total], bytes, 0);
			if (received == -1) return -1;
			if (received ==0) return total;
			bytes = bytes - received;
			total = total + received;
		}
		return total;
	}

	// talk to the server
	while (1)
	{
		printf("Please enter a message for server: ");
		memset(buffer_send,'\0', SIZE);
		fgets(buffer_send, SIZE, stdin); // get the message to send
		// send message
		int send_mess = send_packets(buffer_send, sizeof(buffer_send));

		// receive message
		memset(buffer_receive,'\0', SIZE);
		int receive_mess = receive_packets(buffer_receive, SIZE);
		printf("capitalize string from server: %s", buffer_receive);
	}
	close(cSock);
	return 0;
}
