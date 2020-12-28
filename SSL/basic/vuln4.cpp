// gcc -o build/vuln4 vuln4.cpp

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main(void)
{
    char passwd[9] = {0, };
    char input[9] = {0, };

    // generate password
    srand(time(NULL));
    for (int i=0; i<8; i++)
        passwd[i] = (rand() % 0x5e) + 0x20;

    // input
    printf("> ");
    scanf("%8s", input);
    getchar();
    
    // check
    if (strncmp(input, passwd, sizeof(passwd)))
    {
        printf("password was '%s'\n", passwd);
        return -1;
    }
    else
    {
        puts("passed!"); // <-- goal
        return 0;
    }
}