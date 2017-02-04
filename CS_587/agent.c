#include<stdio.h>
#include<string.h>
#include<stdlib.h> //for exit(1), random
#include<arpa/inet.h>
#include<sys/socket.h>
#include <time.h>
#define UDP_PORT 8888 // port for UDP client to connect to server
#define SIZE 1024  //Max size of buffer
#define LOWEST_PORT 1024
#define HIGHEST_PORT 65535

// for os info request
#include <stdio.h>

#if defined(_WIN32) || defined(_WIN64)
        const char* os = "Window";
#else
#ifdef __linux
        const char* os = "Linux";
#else
        const char* os = "Mac";
#endif
#endif
// global variable
char Operating_System[16];
int *execution_time;
// get os function


void GetLocalOS(char OS[16], int *valid)
{
	strcpy(OS,os);
}
// get time function
void GetLocalTime(int *system_time, int *valid)
{
	system_time = execution_time;
}

// struct BEACON

pthread_t beacon_sender;

struct BEACON
{
	int	ID;  	     // randomly generated during startup
	int	StartUpTime; // the time when the client starts
	char IP[4];       // the IP address of this client
	int	CmdPort;     // the client listens to this port for manager cmd
};

struct INFO
{
	int id;
	int port;
	int time;
};
void* BeaconSender(void *arg)
{

    int cSock;
    int i;
    char *SERVER = "127.0.0.1"; // server string, suposely 127.0.0.1 for local network
    struct INFO* info    = arg;
    int PORT = (*info).port;
    int id   = (*info).id; // id for our client
    char buffer_receive[SIZE] ; // variable to receive from server
    char buffer_send[SIZE] ; // variable to send to server

    // set a copy to split by '.' and pass it into our BEACON
    char *copy ;
    char *token;
    copy = malloc(sizeof(char) * strlen(SERVER)); // allocate memory for copy
    strcpy(copy,SERVER); // copy the info from argv[1]

    // initiate a BEACON struct
    struct BEACON bacon;
    bacon.StartUpTime = (*info).time;
//    srand(clock()); // set the seed by the time so everytime a client pop up, its different
    bacon.ID = id; // random ID
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
    sin.sin_port = htons(UDP_PORT);

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
//        memset(buffer_receive,'\0', SIZE);
//        // a blocking call, wait until receive the data
//        if (recvfrom(cSock, buffer_receive, SIZE, 0, (struct sockaddr *) &sin, &slen) == -1)
//        {
//        	printf("Fail to receive message\n");
//        	abort();
//        }
//
//        puts(buffer_receive); // display without caring too much about the type
        sleep(10);
    }

    close(cSock); // close the socket when done
}

void cmdAgent(id)
{
	char buffer[SIZE];
    int server_sockfd, client_sockfd;
    int server_len, client_len;
    struct sockaddr_in server_address;
    struct sockaddr_in client_address;
    int current_port = 1024;

    server_sockfd = socket( AF_INET, SOCK_STREAM, 0 );
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = inet_addr( "127.0.0.1" );
    server_address.sin_port = htons( current_port );

    server_len = sizeof( server_address );

        while ( bind( server_sockfd, ( struct sockaddr *)&server_address, server_len ) != 0 )
        {
        	current_port ++;
        	server_address.sin_port = htons( current_port );
        }
    struct INFO info;
    info.id = id;
    info.port = current_port;
    info.time = clock();
    /* When we hit an available port, we will create a thread to beacon sender and send it*/

    pthread_create(&beacon_sender, NULL, BeaconSender, &info);
    // this whole function wont stop until the beacon_sender is done

    listen( server_sockfd, 5 );


        printf( "Agent wait...\n" );

        client_len = sizeof( client_address );
        client_sockfd = accept( server_sockfd, ( struct sockaddr *)&client_address, &client_len );
		printf( "Manager connected \n" );
		memset(buffer,'\0', 1024);
		recv(client_sockfd, buffer, 1024, 0);

		/*---- Print the received message ----*/
		printf("Data received: %s",buffer);

        /* get the local os and time to send */
        memset(buffer,'\0', 1024);
        GetLocalOS(Operating_System,(int*)1);

//        GetLocalTime(local_time,(int*)1);
        sprintf(buffer,"OS: %s, System clock: %i",Operating_System,info.time);
        send(client_sockfd, buffer,1024,0);
        close( client_sockfd );
    pthread_join(beacon_sender,NULL);
}




int main(int argc, char *argv[])
{	/* create thread */
	int id = atoi(argv[1]);
	cmdAgent(id);
	return 0;
}
