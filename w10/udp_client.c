#include <netinet/in.h>
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
	int str_len;
	socklen_t adr_sz;

	struct sockaddr_in serv_adr, from_adr;

	if (argc != 3)
	{
		printf("Usage :%s <IP> <port>\n", argv[0]);
		exit(1);
	}

	sock = socket(PF_INET, SOCK_DGRAM, 0);

	if (sock == -1)
		error_handling("socket() error");
	
	memset(&serv_adr, 0, sizeof(serv_adr));
	serv_adr.sin_family = AF_INET;
	serv_adr.sin_addr.s_addr = inet_addr(argv[1]);
	serv_adr.sin_port = htons(atoi(argv[2]));

	while(1)
	{
		fputs("insert message(q to quit): ", stdout);
		fgets(message, sizeof(message), stdin);

		if (!strcmp(message, "q\n") || !strcmp(message, "Q\n"))
					break;
		sendto(sock, message, strlen(message), 0, (struct sockaddr*)&serv_adr, sizeof(serv_adr));
		adr_sz = sizeof(from_adr);
		str_len = recvfrom(sock, message, BUFSIZE, 0, (struct sockaddr*)&from_adr, &adr_sz);
		message[str_len] = 0;
		printf("서버로부터 정송된 메세지 : %s\n", message);
	}
	close(sock);
	return (0);
}
