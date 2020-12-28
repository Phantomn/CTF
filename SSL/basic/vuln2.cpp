// $ gcc -o build/vuln2 vuln2.cpp

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>

typedef struct
{
    uint32_t size;
    char data[256];
} __attribute__((packed)) FileFormat;

FileFormat ff;
char *data;

int get_file(const char *filepath)
{
    int fd = open(filepath, O_RDONLY);
    if (fd < 0)
    {
        perror("open");
        return -1;
    }

    ssize_t n = read(fd, &ff, sizeof(ff));
    if (n < 0)
    {
        perror("read");
        return -1;
    }

    if (ff.size != (n - sizeof(ff.size)))
    {
        fprintf(stderr, "File size incorrect.\n");
        return -1;
    }

    data = (char *)(malloc(ff.size));
    if (!data)
    {
        fprintf(stderr, "malloc() failed.\n");
        return -1;
    }

    memcpy(data, ff.data, ff.size);
    return 0;
}

void alloc_password(void)
{
    char *ptr = (char *)(malloc(0x100));
    if (ptr)
        strcpy(ptr, "this is password.");
}

int get_int(void)
{
    int ret;
    char buf[0x10];
    write(1, "> ", 2);
    buf[read(0, buf, 0xf)] = '\0';
    return atoi(buf);
}

void view_data(void)
{
    int offset = get_int();
    int size = ff.size;

    if (offset < size)
        fprintf(stdout, "%s", data+offset);
    else
        fprintf(stderr, "Invalid offset.\n");
}

void usage(const char *argv[])
{
    fprintf(stderr, "%s [filepath]\n", argv[0]);
    exit(-1);
}

int main(int argc, const char *argv[])
{
    setvbuf(stdin, NULL, 2, 0);
    setvbuf(stdout, NULL, 2, 0);
    setvbuf(stderr, NULL, 2, 0);

    if (argc != 2)
        usage(argv);

    alloc_password();
    
    if (get_file(argv[1]) < 0)
        return -1;

    view_data();

    return 0;
}