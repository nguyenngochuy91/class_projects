#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <sys/un.h>
#include <unistd.h>
#include <netinet/in.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>
#define UDP_PORT 8888 // port for UDP client to connect to server
#define SIZE 1024  //Max size of buffer
void cmdAgent()
{
    int server_sockfd, client_sockfd;
    int server_len, client_len;
    struct sockaddr_in server_address;
    struct sockaddr_in client_address;


    server_sockfd = socket( AF_INET, SOCK_STREAM, 0 );
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = inet_addr( "127.0.0.1" );
    server_address.sin_port = htons( 10000 );

    server_len = sizeof( server_address );

        if( bind( server_sockfd, ( struct sockaddr *)&server_address, server_len ) != 0 )
        {
                perror("The port has been used ");
                exit( 1 );
        }

    listen( server_sockfd, 5 );

    signal( SIGCHLD, SIG_IGN );

        printf( "Agent wait...\n" );

        client_len = sizeof( client_address );
        client_sockfd = accept( server_sockfd, ( struct sockaddr *)&client_address, &client_len );
		printf( "Manager connected \n" );
		memset(buffer,'\0', 1024);
		recv(cltSock, buffer, 1024, 0);

		/*---- Print the received message ----*/
		printf("Data received: %s",buffer);
        close( client_sockfd );


}

int main()
{
	cmdAgent();
}
