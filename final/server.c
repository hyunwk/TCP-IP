#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <arpa/inet.h>
#include <sys/wait.h>

#define BUF_SIZE 30

void error_handling(char *message)
{
	fputs(message, stderr);
	fputc('\n',stderr);
	exit(1);
}

void read_childproc(int sig)
{
	pid_t pid;
	int status;

	pid = waitpid(-1, &status, WNOHANG);
	printf("Removed proc id : %d\n", pid);
}

int main(int argc, char **argv)
{
	int	serv_sock, clnt_sock;
	struct sockaddr_in serv_adr, clnt_adr;

	pid_t pid;
	struct sigaction act;
	socklen_t	adr_sz;
	int	strlen, state;
	char buf[BUF_SIZE];
	
	//numbers of connected clients, maxinum 30
	int clientList[30] = { 0, };
	int	client_cnt = 0;

	// port 번호 들어오지 않을 경우
	if (argc != 2)
	{
		printf("Usage : %s <port>\n", argv[0]);
		exit(1);
	}

	//sigaction 설정
	act.sa_handler = read_childproc;
	sigemptyset(&act.sa_mask);
	act.sa_flags = 0;
	state = sigaction(SIGCHLD, &act, 0);
	
	//server socket 설정
	serv_sock = socket(PF_INET, SOCK_STREAM, 0);
	memset(&serv_adr, 0, sizeof(serv_adr));
	serv_adr.sin_family = AF_INET;
	serv_adr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_adr.sin_port = htons(atoi(argv[1]));


	if (bind(serv_sock, (struct sockaddr*)&serv_adr, sizeof(serv_adr)) == -1)
		error_handling("bind error");
	if (listen(serv_sock, 6) == -1)
		error_handling("listen error");

	while(1)
	{
		// client accept
		adr_sz = sizeof(clnt_adr);
		clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_adr, &adr_sz);
		if (clnt_sock == -1)
			continue;
		else
			printf("client connected num :");
		
		pid = fork();
		
		printf("num :%d server pid : %d\n", client_cnt, pid);

		if (pid == -1)
		{
			close(clnt_sock);
			continue;
		}
		else if (!pid)
		{
			close(serv_sock);
			clientList[client_cnt] = pid;
			client_cnt++;
			while (strlen = read(clnt_sock, buf, BUF_SIZE))
				write(clnt_sock, buf, strlen);

			close(clnt_sock);
			client_cnt--;
			puts("client disconnected...");
			return (0);
		}
		else
			close(clnt_sock);
	}
	close(serv_sock);
	return (0);
}
