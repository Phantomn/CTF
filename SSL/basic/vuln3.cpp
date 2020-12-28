// $ gcc -o vuln3 vuln3.cpp

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define ALLOC_SIZE 0x100

char *lists[0x10];
uint32_t pool;

int get_int(void)
{
    int ret;
    char buf[0x10];
    write(1, "> ", 2);
    buf[read(0, buf, 0xf)] = '\0';
    return atoi(buf);
}

void gen(const char *data)
{
    if (pool >= 0x10)
        return;

    char *g = (char *)(malloc(ALLOC_SIZE));
    if (!g)
    {
        fprintf(stderr, "malloc() failed.\n");
        return;
    }

    strcpy(g, data);
    lists[pool++] = g;
}

void del(void)
{
    uint32_t index;
    
    write(1, "idx", 3);
    index = (uint32_t)get_int();

    if (index > 0x10 || !lists[index])
        return;

    free(lists[index]);
}

void view(void)
{
    uint32_t index;

    write(1, "idx", 3);
    index = (uint32_t)get_int();

    if (index < 0x10 && lists[index] && index != 0)
        puts(lists[index]);
}

void pass(void)
{
    uint32_t index;

    write(1, "idx", 3);
    index = (uint32_t)get_int();

    if (index < 0x10 && lists[index] && index != 0) {
        if (!strncmp(lists[index], lists[0], strlen(lists[0])))
            puts("Congraturations!");
    }
}

int main(void)
{
    setvbuf(stdin, NULL, 2, 0);
    setvbuf(stdout, NULL, 2, 0);
    setvbuf(stderr, NULL, 2, 0);

    pool = 0;
    gen("thisispassword");

    while (true)
    {
        write(1, "sel", 3);
        switch (get_int())
        {
            default     : break;
            case 0      : return 0;
            case 1      : gen("Hello!"); break;
            case 2      : del(); break;
            case 3      : view(); break;
            case 4      : pass(); break;
        }
    }

    return 0;
}