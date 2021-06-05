#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>

#define BUFSIZE 30

void error_handling(char *message)
{
	fputs(message, stderr);
	fputc('\n', stderr);
	exit(1);
}
int main(int argc, char **argv)
{
	int sock;
	char message[BUFSIZ];
	int str_len, addr_size, i;
	char msg1[] = "Hi!";
	char msg2[] = "I'm another udp host!";
	char msg3[] = "nice to meet you!";

	struct sockaddr_in your_adr;
	socklen_t your_adr_sz;

	if (argc != 3)
	{
		printf("usage : %s", argv[0]);
		exit(1);
	}

	sock = socket(PF_INET, SOCK_DGRAM, 0);
	if (sock == -1)
		error_handling("socket() error");
	memset(&your_adr, 0, sizeof(your_adr));
	your_adr.sin_family = AF_INET;
	your_adr.sin_addr.s_addr = inet_addr(argv[1]);
	your_adr.sin_port = htons(atoi(argv[2]));

	sendto(sock, msg1, strlen(msg1), 0, (struct sockaddr*)&your_adr, sizeof(your_adr));
	sendto(sock, msg2, strlen(msg2), 0, (struct sockaddr*)&your_adr, sizeof(your_adr));
	sendto(sock, msg3, strlen(msg3), 0, (struct sockaddr*)&your_adr, sizeof(your_adr));

	close(sock);
	return (0);
}
