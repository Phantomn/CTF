#include <stdio.h>
#include <errno.h>

int hint_count=0;
char hints[] = {"This time some exploitation has to take place", 
	"The flag file is not readable by your current user", 
	"You will need to become root to solve the challenge", 
	"There may be different ways, but we do not necessarily need to modify a $rip",
	"We might want to find something to override. What is it and how can we find it?",
	"Kernel header files may give you some hints about how to identify what we are looking for"};

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
	__int64 v1;
	__int64 v2;
	char v3;

	printf("Which file are we trying to read?\n> ");
	if(scanf("%255s", &v3) == 1){
		v1 = fopen(&v3, "r");
		if(v1){
			v2 = fread(&v3, 1, 256, v1);
			fclose(v1);
			printf("Here are your 0x%lx bytes contents: \n", v2);
			if(v2)
				fwrite(&v3, 1, v2, stdout);
			puts("");
		}
		else{
			puts("Could not open file for reading...");
		}
	}
}

__int64 do_hint(){
	__int64 result;
	++hint_count;
	printf("Okay, here is your next hint:\n'%s'\n", hints[hint_count]);
	result=hint_count%6;
	return result;
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
