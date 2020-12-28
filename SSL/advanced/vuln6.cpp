// gcc -o build/vuln6 vuln6.cpp

#include <stdint.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, const char *argv[])
{
    char buf[256];
    int16_t size;
    int16_t do_count, gae_count, gul_count, yut_count, mo_count;

    setvbuf(stdin, NULL, 2, 0);
    setvbuf(stdout, NULL, 2, 0);
    setvbuf(stderr, NULL, 2, 0);

    puts("== Yut nori calculator ==");

    printf("Count of DO: ");
    scanf("%hd", &do_count);
    getchar();

    printf("Count of GAE: ");
    scanf("%hd", &gae_count);
    getchar();

    printf("Count of GUL: ");
    scanf("%hd", &gul_count);
    getchar();

    printf("Count of YUT: ");
    scanf("%hd", &yut_count);
    getchar();

    printf("Count of MO: ");
    scanf("%hd", &mo_count);
    getchar();

    puts("[*] Calculating...");

    size = (do_count * 1) + (gae_count * 2) + (gul_count * 3) + (yut_count * 4) + (mo_count * 5);

    if (size < 256)
        puts("[?] What is your name?");
        printf(": ");
        for (uint32_t i=0; i<size; i++)
        {
            read(0, buf+i, 1);
            if (buf[i] == '\n')
                break;
        }

    printf("[+] Total size is %hu!\n", size);
    return 0;
}