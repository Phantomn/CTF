#ifndef _BMP_H_
#define _BMP_H_

#include <stdint.h>

typedef struct BITMAPFILEHEADER {

    uint8_t bfType[2];
    uint32_t bfSize;
    uint16_t reserved1;
    uint16_t reserved2;
    uint32_t bfOffBits;

} __attribute__((packed)) bmphdr;

typedef struct BITMAPINFOHEADER {

    uint32_t biSize;            // header size
    uint32_t biWidth;
    uint32_t biHeight;
    uint16_t biPlanes;          // always 0
    uint16_t biBitCount;        // always 24
    uint32_t biCompression;     // always 0
    uint32_t biSizeImage;       // pure image size
    uint32_t biXPelsPerMeter;
    uint32_t biYPelsPerMeter;
    uint32_t biClrUsed;
    uint32_t biClrImportant;

} __attribute__((packed)) bmpihdr;

typedef struct _bmp_file {

    uint32_t size;
    uint32_t width;
    uint32_t height;
    uint8_t *bitmap;

} bmp_t;

int parse_bmp(const char *filepath, bmp_t *out);

#endif