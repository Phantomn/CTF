#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "bmp.h"

int parse_bmp(const char *filepath, bmp_t *out)
{
    bmphdr bh;
    bmpihdr bih;

    int fd = open(filepath, O_RDONLY);
    if (fd < 0)
        return -1;

    /*
     * parse bmp header.
    */

    if (read(fd, &bh, sizeof(bh)) != sizeof(bh))
        return -1;

    // header check.
    if (bh.bfType[0] != '\x42' || bh.bfType[1] != '\x4d')
    {
        fprintf(stderr, "incorrect bfType.\n");
        return -1;
    }

    /*
     * parse bmp information header.
    */

    if (read(fd, &bih, sizeof(bih)) != sizeof(bih))
        return -1;

    if (bih.biSize != sizeof(bih))
    {
        fprintf(stderr, "incorrect information header size.\n");
        return -1;
    }

    if (bih.biBitCount != 24 || bih.biCompression != 0)
    {
        fprintf(stderr, "unsupported feature(s) detected.\n");
        return -1;
    }

    /*
     * parse bitmaps
    */

    uint8_t *bitmap;
    uint32_t bitmap_size;

    bitmap_size = bh.bfSize - sizeof(bh) - sizeof(bih);
    bitmap = (uint8_t *)(calloc(bitmap_size, sizeof(uint8_t)));
    if (!bitmap)
    {
        fprintf(stderr, "memory allocation error.\n");
        return -1;
    }

    if (read(fd, bitmap, bitmap_size) != bitmap_size)
    {
        fprintf(stderr, "incorrect bitmap size.\n");
        return -1;
    }

    out->size   = bitmap_size;
    out->bitmap = bitmap;
    out->width  = bih.biWidth;
    out->height = bih.biHeight;

    close(fd);
    return 0;
}