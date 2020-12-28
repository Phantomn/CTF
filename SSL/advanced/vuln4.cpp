// gcc -o build/vuln4 vuln4.cpp -m32

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

typedef struct _ustr
{
    uint32_t size;
    union {
        struct {
            char str[0x28];
        };
        struct {
            char *ptr;
            char _padd[0x28-sizeof(char *)];
        };
    };
} __attribute__((packed)) ustr;

char store[0x1000];

ustr *passwd;
ustr *input;

void get_input(void)
{
    char tmp[0x1000];
    uint32_t size;

    printf("size: ");
    scanf("%u", &size);
    getchar();

    if (size > 0x1000)
        size = 0x1000;

    ustr *tmpstr = (ustr *)(calloc(sizeof(ustr), 1));
    if (!tmpstr)
        return;

    tmpstr->size = size;

    if (size < 0x28)
        fgets(tmpstr->str, size, stdin);
    else
    {
        fgets(tmp, size, stdin);
        tmpstr->ptr = tmp;
    }

    input = tmpstr;
}

void print_input(void)
{
    if (input->size < 0x28) {
        write(1, input->str, input->size);
    } else {
        write(1, input->ptr, input->size);
    }
    putchar(0x0a);
}

void get_passwd(void)
{
    int urandom;
    uint32_t size;
    char tmp[0x1000] = {0,};

    printf("size: ");
    scanf("%u", &size);
    getchar();

    if (size > 0x1000)
        size = 0x1000;

    strncpy(tmp, store, size);

    ustr *tmpstr = (ustr *)(calloc(sizeof(ustr), 1));
    if (!tmpstr)
        return;

    tmpstr->size = size;

    if (tmpstr->size < 0x28)
    {
        strncpy(tmpstr->str, tmp, tmpstr->size);
    }
    else
    {
        tmpstr->ptr = (char *)(calloc(tmpstr->size, sizeof(char)));
        if (!tmpstr->ptr)
        {
            free(tmpstr);
            return;
        }

        strncpy(tmpstr->ptr, tmp, tmpstr->size);
    }

    passwd = tmpstr;
}

void login(void)
{
    char s_input[0x1000] = {0, };
    char s_passwd[0x1000] = {0, };

    /* Copy input */
    if (input->size < 0x28)
        strncpy(s_input, input->str, sizeof(s_input));
    else
        strncpy(s_input, input->ptr, sizeof(s_input));

    /* Copy password */
    if (passwd->size < 0x28)
        strncpy(s_passwd, input->str, sizeof(s_passwd));
    else
        strncpy(s_passwd, input->ptr, sizeof(s_passwd));

    /* Compare */
    if (!strncmp(s_input, s_passwd, passwd->size))
        puts("Congraturations!");
    else
        puts("Nah...");
    
}

int main(void)
{
    setvbuf(stdin, NULL, 2, 0);
    setvbuf(stdout, NULL, 2, 0);
    setvbuf(stderr, NULL, 2, 0);

    /*
     * Get random password.
    */

    int urandom;

    if ((urandom = open("/dev/urandom", O_RDONLY)) < 0)
        return -1;

    for (int i=0; i < sizeof(store); i++)
    {
        read(urandom, store+i, 1);
        if (store[i] < 0x20 || store[i] > 0x7e) // is not ascii
            i--;
    }

    close(urandom);

    /*
     * Let's loop
    */

    uint32_t sel = 0;

    do {

        printf("Select: ");
        scanf("%u", &sel); getchar();

        switch (sel)
        {
            default:
            case 0:
                break;

            case 1:
                get_input();
                break;

            case 2:
                get_passwd();
                break;

            case 3:
                print_input();
                break;

            case 4:
                login();
                break;
        }

    } while (sel != 0);

    return 0;
}