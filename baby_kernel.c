#include <stdio.h>
#include <errno.h>


filename = "/dev/flux_baby_2";

void menu(){
	return printf("----- Menu -----\n"
			"1. Read\n"
			"2. Write\n"
			"3. Show me my uid\n"
			"4. Read File\n"
			"5. Any hint?\n"
			"6. Bye!\n"
			"> ");
}

int read_num(){
	__int64 v1;
	unsigned __int64 v2;

	v1 = 0xDEADBEEFDEADBEEF;
	if(scanf("%llx", &v2) != 1)
		exit(-1);

	return v1;
}

void do_read(int fd){
	__int64 v3;
	__int64 v2;
	v2 = 0xDEADBEEFDEADBEEF;

	puts("I need an address to read from. Choose wisely\n> ");
	v3 = read_num();

	puts("Got everything I need. Let's do it!");
	ioctl_read(fd, v3, &v2);
	printf("We're back. Our scouter says the power level is : %016lx\n", v2);
}

__int64 do_write(int fd){
	__int64 v2;
	__int64 v3;

	puts("I need an offset to write to. Choose wisely - seriously now...\n> ");
	v2 = read_num();
	if(v2 <= 0x3FFF)
		return puts("We are really plaing with fire here. Let's not do that...");
	puts("What about a value?\n> ");
	v3 = read_num();
	puts("Thanks, boss. I can't believe we are' doing this!");
	ioctl_write(fd, v2, v3);
	return puts("Amazingly, we're back again.");
}

void do_readfile(){

}

int main(int argc, char* argv[], char* env[]){
	int fd;
	int result;
	fd = open(0, "/dev/flux_baby_2", env);
	if(fd == -1){
		_errno_location();
		printf("Failed test for opening file ret val: %d\nexpected errno val: %d, got: %d\n");
	}

	while(1){
		menu();
		switch(read_num()){
			case 1:
				do_read(fd);
				continue;
			case 2:
				do_write(fd);
				continue;
			case 3:
				system("id");
				continue;
			case 4:
				do_readfile();
				continue;
			case 5:
				do_hint();
				continue;
			case 6:
				close(fd);
				puts("bye!");
				result = 0;
				break;
			default:
				puts("Did not understand your input...");
				result = 0;
				break;
		}
		break;
	}
	return result;
}
