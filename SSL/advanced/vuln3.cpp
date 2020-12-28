// gcc -o build/vuln3 vuln3.cpp

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define ADMIN "ADMINISTRATOR"
#define SEARCH_ERROR 0xffffffff
#define DEBUG

char *names[0x10];
bool admins[0x10];

uint32_t search_empty_namespace(void)
{
    uint32_t idx = 0;
    char *name = NULL;

    for (idx = 0; idx < 0x10; idx++)
    {
        if (names[idx] == NULL)
            return idx;
    }

    return SEARCH_ERROR;
}

void create_admin(void)
{
    char *admin = (char *)(calloc(0x200, sizeof(char)));
    if (!admin)
        return;

    uint32_t idx = search_empty_namespace();
    if (idx == SEARCH_ERROR) {
        free(admin);
        return;
    }

    strcpy(admin, ADMIN);
    names[idx] = admin;
    admins[idx] = true;

    printf("Created => %u\n", idx);
#ifdef DEBUG
    printf("%p\n", admin);
#endif
}

void create_user(void)
{
    char *user = (char *)(calloc(0x200, sizeof(char)));
    if (!user)
        return;

    uint32_t idx = search_empty_namespace();
    if (idx == SEARCH_ERROR) {
        free(user);
        return;
    }

    printf("user name: ");
    fgets(user, 0x100, stdin);
    user[strlen(user)-1] = '\0';

    if (!strcmp(user, ADMIN)) {
        printf("You can't name your account to %s.\n", user);
        free(user);
        return;
    }

    names[idx] = user;
    admins[idx] = false;

    printf("Created => %u\n", idx);
#ifdef DEBUG
    printf("%p\n", user);
#endif
}

void edit_user(void)
{
    char *user;
    uint32_t idx, size;

    printf("index: ");
    scanf("%u", &idx); getchar();
    if (idx >= 0x10 || !names[idx] || admins[idx])
        return;

    user = names[idx];

    printf("size: ");
    scanf("%u", &size); getchar();
    if (size > 0x1000)
        size = 0x1000;
        
    if (realloc(names[idx], size) == NULL)
        return;

    printf("new user name: ");
    fgets(user, size, stdin);
    user[strlen(user)-1] = '\0';

    if (!strcmp(user, ADMIN)) {
        printf("You can't name your account to %s.\n", user);
        free(user);
        return;
    }

    puts("Changed!");

#ifdef DEBUG
    printf("%p\n", user);
#endif
}

void free_user(void)
{
    uint32_t idx;

    printf("index: ");
    scanf("%u", &idx); getchar();
    if (idx >= 0x10 || !names[idx])
        return;

    free(names[idx]);
    names[idx] = NULL;
    admins[idx] = false;

    puts("Deleted!");
}

void view_user(void)
{
    uint32_t idx;

    printf("index: ");
    scanf("%u", &idx); getchar();
    if (idx >= 0x10 || !names[idx])
        return;

    puts(names[idx]);
#ifdef DEBUG
    printf("%p\n", names[idx]);
#endif
}

void login(void)
{
    uint32_t idx;
    
    printf("index: ");
    scanf("%u", &idx); getchar();
    if (idx >= 0x10 || !names[idx] || admins[idx])
        return;

    if (!strncmp(names[idx], ADMIN, strlen(ADMIN)) || admins[idx])
        puts("Hello administrator.");
    else
        puts("Permission denied.");
}

int main(int argc, const char *argv[])
{
    uint32_t sel;

    while (true) {
        
        printf("Select: ");
        scanf("%u", &sel);
        getchar();
        
        switch (sel)
        {
            case 0:
                create_admin();
                break;

            case 1:
                create_user();
                break;

            case 2:
                edit_user();
                break;

            case 3:
                view_user();
                break;

            case 4:
                free_user();
                break;

            case 5:
                login();
                break;

            case 6:
                return 0;
        }
    }
}