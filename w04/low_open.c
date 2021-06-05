#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/fcntl.h>
#include <unistd.h>

void error_handling(char *message)
{
	fputs(message, stderr);
	fputs("\n", stderr);
	exit(1);
}

int main(void)
{
	int fd;
	char buf[] = "Let's go \n";
	fd = open("data.txt", O_CREAT | O_WRONLY | O_TRUNC);
	if (fd == -1)
		error_handling("open() error");
	printf("FILe descripter : %d \n ", fd);

	if (write(fd, buf, sizeof(buf)) == -1)
			error_handling("write() error!");
	close(fd);
	return (0);
}
