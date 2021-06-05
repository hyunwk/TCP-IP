#include <stdio.h>
#include <unistd.h>

int main(int argc, char **argv)
{
	pid_t pid = fork();

	if (pid)
	{
		printf("child process id : %d\n", pid);
		sleep(30);
	}
	else 
		puts("hi i'm a child process");
	
	if (pid)
		puts("end parent process");
	else
		puts("end child process");
	return (0);
}
