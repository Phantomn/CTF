#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

char* fname="./this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong";
int main(int argc, char* argv[]){
	int fd;
	char buf[256]={0,};

	fd = open(fname, O_RDONLY);
	read(fd, buf, sizeof(buf));
	write(fd, buf, strlen(buf));
	exit(0);
}
