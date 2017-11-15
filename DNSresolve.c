#include<stdio.h> 	// printf
#include<string.h>	// strcpy
#include<sys/socket.h>	
#include<netdb.h>	// hostent
#include<arpa/inet.h>

int main(int argc, char *argv[])
{
	char *hostname =  "www.google.com";
	char ip[100];
	struct hostent *he;
	struct in_addr **addr_list;	// 2-D array in pointers

	if((he = gethostbyname(hostname)) == NULL)
	{
		// gethostbyname failed
		herror("gethostbyname");
		return 1;
	}

	// Cast the h_addr_list to in_addr, since h_addr_list also has the ip
	// address in long format only 
	addr_list = (struct in_addr **) he -> h_addr_list;

	for(int i = 0; addr_list[i] != NULL; i++)
	{
		// Return the first one
		strcpy(ip, inet_ntoa(*addr_list[i]));
	}	

	printf("%s resolved to : %si\n", hostname, ip);
	return 0;
}

// The function inet_ntoa will convert an IP address in long format to dotted
// format. This is just the opposite of inet_addr. So far we have seen some
// important structures that are used. Lets revise them:
//	1. sockaddr_in - Connection information. Used by connect, send, recv
//	etc.
//	2. in_addr - IP address in long format
// 	3. sockaddr
//	4. hostent - The IP addresses of a hostname. Used by gethostbyname

