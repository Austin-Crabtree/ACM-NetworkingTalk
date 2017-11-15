#include<stdio.h>
#include<string.h> // strlen
#include<sys/socket.h>
#include<arpa/inet.h> // inet_addr

int main(int argc, char *argv[])
{
	int socket_desc = socket(AF_INET, SOCK_STREAM, 0); // Create socket
	struct sockaddr_in server;
	char *message;

	if(socket_desc == -1)
	{
		printf("Couldn't create a socket");
	}

	server.sin_addr.s_addr = inet_addr("172.217.8.174");
	server.sin_family = AF_INET;
	server.sin_port = htons(80);

	// Connect to remote server
	if(connect(socket_desc, (struct sockaddr *)&server, sizeof(server)) < 0)
	{
		puts("connect error");
		return 1;
	}

	puts("connected\n");
	
	// Send some data
	message = "GET / HTTP/1.1\r\n\r\n";
	if(send(socket_desc, message, strlen(message), 0) < 0)
	{
		puts("send failed");
		return 1;
	}
	
	puts("data sent\n");

	return 0;
}
