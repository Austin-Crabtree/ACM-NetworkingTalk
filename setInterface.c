#include<stdio.h>
#include<sys/socket.h>

#define SERVERPORT 5555

int main (int argc, char *argv[])
{
	struct ifreq ifr;
	int sd = socket(AF_INET, SOCK_STREAM, 0);
	if(sd < 0)
	{
		printf("Couldn't create socket");
	}

	// Bind to selected interface only
	memset(&ifr, 0, sizeof(ifr));
	snprintf(ifr.ifr_name, sizeof(ifr.ifr_name), "en0"); // en0 is the interface name
	if((rc = set
