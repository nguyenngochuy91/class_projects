#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <stdlib.h>
int main(int argc, char *argv[]){
  int clientSocket;
  int PORT = atoi(argv[2]);
  char buffer[1024];
  struct sockaddr_in serverAddr;
  socklen_t addr_size;

  /*---- Create the socket. The three arguments are: ----*/
  /* 1) Internet domain 2) Stream socket 3) Default protocol (TCP in this case) */
  clientSocket = socket(PF_INET, SOCK_STREAM, 0);

  /*---- Configure settings of the server address struct ----*/
  /* Address family = Internet */
  serverAddr.sin_family = AF_INET;
  /* Set port number, using htons function to use proper byte order */
  serverAddr.sin_port = htons(PORT);
  /* Set IP address to localhost */
  serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
  /* Set all bits of the padding field to 0 */
  memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero);

  /*---- Connect the socket to the server using the address struct ----*/
  addr_size = sizeof serverAddr;
  connect(clientSocket, (struct sockaddr *) &serverAddr, addr_size);

  /*---- Send the message to the server into the buffer ----*/
  printf("Please enter a message for server: ");
  memset(buffer,'\0', 1024);
  fgets(buffer, 1024, stdin);
  send(clientSocket, buffer,1024,0);

  /*---- Read the message from the server into the buffer ----*/
  memset(buffer,'\0', 1024);
  recv(clientSocket, buffer, 1024, 0);

  /*---- Print the received message ----*/
  printf("Data received: %s",buffer);

  return 0;
}
