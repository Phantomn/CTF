// gcc -o build/vuln1 vuln1.cpp

#include <unistd.h>
#include <stdbool.h>

struct user {
    char id[0x100];
    bool is_user;
};

int main(int argc, const char *argv[])
{
    struct user user;
    user.is_user = true;

    write(1, "ID: ", 4);
    ssize_t n = read(0, user.id, 0x100);
    user.id[n] = '\0';

    if (user.is_user)
        write(1, "failed.\n", 8);
    else
        write(1, "good.\n", 6);

    return 0;
}