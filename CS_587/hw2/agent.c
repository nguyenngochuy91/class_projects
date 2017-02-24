#include<stdio.h>
#include<string.h>
#include<stdlib.h> //for exit(1), random
#include<arpa/inet.h>
#include<sys/socket.h>
#include <time.h>

// code to figure the local os
#if defined(_WIN32) || defined(_WIN64)
        const char* os = "Window";
#else
#ifdef __linux
        const char* os = "Linux";
#else
        const char* os = "Mac";
#endif
#endif

typedef struct
{
	int *time;
	char *valid;
} GET_LOCAL_TIME;

void GetLocalTime(GET_LOCAL_TIME *ds)
{
	time_t now = time(0);
	ds->time  = &now;
	char val[] = "1";
	ds->valid = &val;
}

typedef struct
{
	int *OS;
	char *valid;
} GET_LOCAL_OS;

void GetLocalOs(GET_LOCAL_OS *ds)
{

}


void cmdAgent(id)
{
    int server_sockfd, client_sockfd;
    int server_len, client_len;
    struct sockaddr_in server_address;
    struct sockaddr_in client_address;
    int current_port = 8888;

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

    /* When we hit an available port, we will create a thread to beacon sender and send it*/


    // this whole function wont stop until the beacon_sender is done

    listen( server_sockfd, 5 );
    while(1)
    {
        printf( "Agent started \n" );

        client_len = sizeof( client_address );
        client_sockfd = accept( server_sockfd, ( struct sockaddr *)&client_address, &client_len );
		printf( "Manager connected \n" );
		// receive the command
		char header[104]; // this is the header
		memset(header,'\0', 104);
		recv(client_sockfd, header, 104, 0); // receive from the manager 104 bytes, store into header
		// need to check the function name
		/*---- Print the received message ----*/

		char function_name[100];
		char GetLocalTime_check[100] = "GetLocalTime";
		char parameter_lenth[4];
		strncpy(function_name,header,100); // copy the first 100 byte
		strncpy(parameter_lenth,header+100,4); // copy the next 4 bytes
		printf("Function name received: %s \n",function_name);

		int length = atoi(parameter_lenth);
		// buffer to store parameters
		char buf[length];
		memset(buf,'\0', length);
		recv(client_sockfd, buf, length, 0); // receive from the manager length bytes, store into buf

		// Execute the command

		int error = strcmp(GetLocalTime_check,function_name);
		printf("error: %i",error);
			printf("GetLocalTime");
			GET_LOCAL_TIME *ds;
			ds       = malloc(sizeof(GET_LOCAL_TIME));
			(*ds).time  = &buf[0];
			(*ds).valid = &buf[4];
			GetLocalTime(&ds);
			free(ds);


//
//        /* get the local os and time to send */
//        memset(buffer,'\0', 1024);
//        GetLocalOS(Operating_System,(int*)1);
//
//        GetLocalTime(execution_time,(int*)1);
//        sprintf(buffer,"OS: %s, System clock: %i",Operating_System,info.time);
//        send(client_sockfd, buffer,1024,0);
//        close( client_sockfd );

    }
}


int main(int argc, char *argv[])
{
	int id = atoi(argv[1]);
	cmdAgent(id);
	return 0;
}
