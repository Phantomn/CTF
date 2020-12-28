struct heap_overflow_i {
    char buf[256];
    int drop_shell;
};

int main(void)
{
    char buf[0x1000] = {0, };

    memset(buf, 0x41, sizeof(buf)-1);

    struct heap_overflow_i *obj = malloc(sizeof(struct heap_overflow_i));
    if (!obj)
        return -1;

    strcpy(obj->buf, buf);

    if (obj->drop_shell)
        system("/bin/sh");

    return 0;
}