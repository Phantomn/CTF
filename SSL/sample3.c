struct heap_overflow_i {
    char buf[8];
    int drop_shell;
};

int main(void)
{
    char buf[] = "AAAAAAAAAA";

    struct heap_overflow_i *obj = malloc(sizeof(struct heap_overflow_i));
    if (!obj)
        return -1;

    strcpy(obj->buf, buf);

    if (obj->drop_shell)
        system("/bin/sh");

    return 0;
}