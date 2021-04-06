#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){
	int flag;
	srand(time(0));
	flag = rand();
	printf("%d\n",flag);
}
