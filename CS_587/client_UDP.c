#include<stdio.h>
#include<string.h>
#include<stdlib.h> //for exit(1), random
#include<arpa/inet.h>
#include<sys/socket.h>
#include <time.h>

#define SIZE 1024  //Max size of buffer
// struct BEACON
struct BEACON
{
	int	ID;  	     // randomly generated during startup
	int	StartUpTime; // the time when the client starts
	char 	IP[4];       // the IP address of this client
	int	CmdPort;     // the client listens to this port for manager cmd
};



int main(int argc, char *argv[])
{

    int cSock;
    int i;
    int PORT = atoi(argv[2]);
    char *SERVER = argv[1]; // server string, suposely 127.0.0.1 for local network

    char buffer_receive[SIZE] ; // variable to receive from server
    char buffer_send[SIZE] ; // variable to send to server

    // set a copy to split by '.' and pass it into our BEACON
    char *copy ;
    char *token;
    copy = malloc(sizeof(char) * strlen(argv[1])); // allocate memory for copy
    strcpy(copy,argv[1]); // copy the info from argv[1]

    // initiate a BEACON struct
    struct BEACON bacon;
    bacon.ID = rand(); // random ID
    bacon.StartUpTime = clock();
    token = strtok (copy,".");
    for (i =0;i<4;i++)
    {
    	bacon.IP[i] = atoi(token);
    	token = strtok (NULL,".");
    }
//
//    bacon.IP[0] = 127;
//    bacon.IP[1] = 0;
//    bacon.IP[2] = 0;
//    bacon.IP[3] = 1;
    bacon.CmdPort = PORT;

    if ( (cSock=socket(AF_INET, SOCK_DGRAM, 0)) == -1)
    {
    	printf("Fail to create socket\n");
    	abort();
    }

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

    while(1)
    {
    	memset(buffer_send,'\0', SIZE);
        // naively create a string from the struct BEACON
    	sprintf(buffer_send,"%i,%i,%i,%i,%i,%i,%i",bacon.ID,
    			bacon.StartUpTime,bacon.IP[0],bacon.IP[1],bacon.IP[2],bacon.IP[3],bacon.CmdPort);
        // send the message from buffer_send using sendto, could use sendmsg but too complicated
        if (sendto(cSock, buffer_send, strlen(buffer_send) , 0 , (struct sockaddr *) &sin, slen)==-1)
        {
        	printf("Fail to send message\n");
        	abort();
        }

        // waiting for the server to return a reply , expect the same thing back
        memset(buffer_receive,'\0', SIZE);
        // a blocking call, wait until receive the data
        if (recvfrom(cSock, buffer_receive, SIZE, 0, (struct sockaddr *) &sin, &slen) == -1)
        {
        	printf("Fail to receive message\n");
        	abort();
        }

        puts(buffer_receive); // display without caring too much about the type
        sleep(10);
    }

    close(cSock); // close the socket when done
    return 0;
}
