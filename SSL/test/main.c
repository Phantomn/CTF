// gcc -o bmp_editor main.c bmp.c -m32 -fno-stack-protector -no-pie -z execstack

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>
#include "bmp.h"

bmp_t bmp;

void print_bit(void)
{
    uint32_t x, y;

    printf("x: ");
    scanf("%u", &x); getchar();

    printf("y: ");
    scanf("%u", &y); getchar();

    if (x > bmp.width || y > bmp.height)
    {
        fprintf(stderr, "out of boundary.\n");
        return;
    }

    uint32_t idx = (x + (y * bmp.width)) * 3;
    printf("%u %u %u", bmp.bitmap[idx], bmp.bitmap[idx+1], bmp.bitmap[idx+2]);

    return;
}

void edit_bit(void)
{
    uint32_t x, y;

    printf("x: ");
    scanf("%u", &x); getchar();

    printf("y: ");
    scanf("%u", &y); getchar();

    if (x > bmp.width || y > bmp.height)
    {
        fprintf(stderr, "out of boundary.\n");
        return;
    }

    uint32_t r, g, b;
    uint32_t m;

    printf("r: ");
    scanf("%u", &r); getchar();

    printf("g: ");
    scanf("%u", &g); getchar();

    printf("b: ");
    scanf("%u", &b); getchar();

    uint32_t idx = (x + (y * bmp.width)) * 3;

    bmp.bitmap[idx]   = b;
    bmp.bitmap[idx+1] = g;
    bmp.bitmap[idx+2] = r;

    return;
}

int main(int argc, const char *argv[])
{
    int sel;

    if (argc != 2)
    {
        printf("usage: %s [bitmap file path]\n", argv[0]);
        return -1;
    }

    if (parse_bmp(argv[1], &bmp))
    {
        puts("Error occured while parsing bmp.");
        return -1;
    }

    while (true)
    {
        puts("== BMP Editor 0.1 ==");
        puts("1. print bit");
        puts("2. edit bit");
        puts("3. exit");
        printf("> ");
        scanf("%d", &sel);
        getchar();

        switch (sel)
        {
            case 1:
                print_bit();
                break;

            case 2:
                edit_bit();
                break;

            case 3:
                exit(0);
        }

        system("clear");
    }

    return 0;
}