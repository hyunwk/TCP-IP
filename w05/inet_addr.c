#include <netinet/in.h>
#include <stdio.h>
#include <arpa/inet.h>

int main(int argc, char **argv)
{
	char *addr1 = "127.212.124.78";
	char *addr2 = "127.212.124.255";

	unsigned long conv_addr = inet_addr(addr1);

	if (conv_addr == INADDR_NONE)
		printf("Error \n");
	else
		printf("Network orderd integer addr : %#lx\n",conv_addr);

	conv_addr = inet_addr(addr2);
	if (conv_addr == INADDR_NONE)
		printf("Error \n");
	else
		printf("Network orderd integer addr : %#lx\n",conv_addr);

	return (0);
}
