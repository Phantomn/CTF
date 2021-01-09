#include <stdio.h>

int main(int argc, char **argv)
{
	long shell;
	shell = 0x80485b0; 
	while(memcmp((void*)shell,"/bin/sh",8)) shell++;
	printf("\"/bin/sh\" is at [ %#x ]\n",shell);
}
