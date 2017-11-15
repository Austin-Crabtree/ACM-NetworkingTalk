#include<stdio.h>
#include<sys/socket.h>
#include<arpa/inet.h> // inet_addr

int main(int argc, char *argv[])
{
	int socket_desc = socket(AF_INET, SOCK_STREAM, 0); // Create socket

	struct sockaddr_in server;

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

	puts("connected");
	return 0;
}
// IPv4 AF_INET Sockets structure
/* 	struct sockaddr_in {
		short		sin_family;	// e.g. AF_INET, AF_INET6
		unsinged short	sin_port;	// e.g. htons(3490)
		struct in_addr	sin_addr;	// see struct in_addr, below
		char		sin_zero[8];	// zero this if you want
	};

	struct in_addr {
		unsinged long 	s_addr;		// load with inet_pton()
	};

	struct sockaddr {
		unsigned short	sa_family;	// address family, AF_XXX
		char		sa_data[14];	// 14 bytes of protocol address
	};

*/
