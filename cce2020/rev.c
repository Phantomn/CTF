#include <stdio.h>

int main(){
	char buf[25]="llj=?=?tfknPf|PbvPi}fjakr";
	int i;
	for(i=0;i<25;i++)
		printf("%c", buf[i] ^ 15);
}
