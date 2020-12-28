// $ gcc -o build/vuln1_lev1 vuln1.cpp -m32 -no-pie -fno-stack-protector -z execstack
// $ gcc -o build/vuln1_lev2 vuln1.cpp -no-pie -fno-stack-protector

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>

int get_buf(const char *filepath, char *buf)
{
    struct stat sb;
    if (stat(filepath, &sb))
    {
        fprintf(stderr, "invalid file: %s\n", filepath);
        return -1;
    }

    int fd = open(filepath, O_RDONLY);
    if (fd < 0)
        return -1;

    read(fd, buf, sb.st_size);
    write(1, "Done.\n", 6);

    return 0; // Success
}

int func(const char *filepath)
{
    char buf[256];
    return get_buf(filepath, buf);
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

    return func(argv[1]);
}