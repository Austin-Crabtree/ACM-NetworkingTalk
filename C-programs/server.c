#include<stdio.h>
#include<string.h>	// strlen
#include<sys/socket.h>
#include<arpa/inet.h>	// inet_addr
#include<unistd.h>	//write

int main(int argc, char *argv[])
{
	// Create socket
	int socket_desc = socket(AF_INET, SOCK_STREAM, 0);
	int new_socket, c;
	struct sockaddr_in server, client;
	char *message;

	if(socket_desc == -1)
		printf("Couldn't create socket");
	
	// Prepare the sockaddr_in structure
	server.sin_family = AF_INET;
	server.sin_addr.s_addr = INADDR_ANY;
	server.sin_port = htons(8888);

	// Bind 
	if(bind(socket_desc, (struct sockaddr *)&server, sizeof(server)) <  0)
	{
		puts("bind failed");
		return 1;
	}
	puts("bind done");

	// Listen 
	listen(socket_desc, 3);

	// Accept an incoming connection
	puts("Waiting for incomming connection...");
	new_socket = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c);
	if(new_socket < 0)
	{
		perror("accept failed");
		return 1;
	}
	puts("Connection accepted");

	// Reply to the client 
	message = "Hello client, I have received your connection. But I have to go now, bye\n";
	write(new_socket, message, strlen(message));
	
	return 0;
}
