// gcc -o build/vuln2 vuln2.cpp

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

char *data;
char password[] = "PASSWORD";

uint32_t get_uint(const char *prompt)
{
    char buf[0x10];
    printf("%s", prompt);
    read(0, buf, 0xf);
    return (uint32_t)(atoi(buf));
}

int main(int argc, const char *argv[])
{
    int urandom;
    uint32_t sel=0, idx=0;

    setvbuf(stdin, NULL, 2, 0);
    setvbuf(stdout, NULL, 2, 0);
    setvbuf(stderr, NULL, 2, 0);

    data = (char *)(malloc(0x1000));
    if (!data)
        return -1;

    urandom = open("/dev/urandom", O_RDONLY);
    if (urandom < 0)
        return -1;
    
    read(urandom, data, 0x1000);

    do {
        puts("1: print buffer");
        puts("2: exit");
        sel = get_uint("sel> ");

        switch (sel)
        {
            default:
            case 0:
                break;

            case 1:
                idx = get_uint("idx> ");
                puts(data+idx); // arbitrary read.
                break;

            case 2:

                if (data)
                {
                    free(data);
                    data = NULL;
                }

                idx = get_uint("exit? (0/1)> ");
                if (idx == 1)
                    sel = 0;
        }
    } while (sel != 0);

    return 0;
}