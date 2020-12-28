// gcc -o build/vuln5 vuln5.cpp

#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void init_heap(void)
{
    int fd;
    void *ptr[1000];
    char rnd;

    for (int i=0; i<1000; i++)
    {
        ptr[i] = malloc(0x1f0);
    }

    if ((fd = open("/dev/urandom", O_RDONLY)) < 0)
        exit(-1);

    for (int i=999; i>=0; i--)
    {
        read(fd, &rnd, 1);
        if (rnd % 2)
            free(ptr[i]);
    }

    close(fd);
}

bool is_triggered;
char *p;

void trigger(void)
{
    char *overflow, *pass;

    if (is_triggered)
        return;

    if (!(overflow = (char *)(malloc(0x1f0))))
        return;
    if (!(pass = (char *)(malloc(0x1f0))))
        return;

    strcpy(pass, "th15_5tr1n9_0n1y_p455");
    memset(overflow, '\x41', 0x250);

    is_triggered = true;
    p = pass;
}

int main(int argc, const char *argv[])
{
    int sel, idx=0, iidx=0;
    void *ptr[0x1000] = {NULL, };

    init_heap();

    do {

        printf("> ");
        scanf("%d", &sel);
        getchar();

        switch (sel)
        {
            default:
            case 0:
                break;

            case 1:
                ptr[idx] = malloc(0x1f0);
                printf("%p\n", ptr[idx++]);
                break;

            case 2:
                printf("idx> ");
                scanf("%d", &iidx);
                if (iidx >= 0 && iidx < 0x1000){
                    free(ptr[iidx]);
                    ptr[iidx] = NULL;
                }
                break;

            case 3:
                trigger();
                break;
        }

    } while (sel != 0);

    if (!strcmp(p, "th15_5tr1n9_0n1y_p455"))
        puts("failed.");
    else
        puts("success.");

    return 0;
}