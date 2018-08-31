# Questions

## What's `stdint.h`?

TODO
stdint.h is a header from C standard, which defined specified width of integer.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

TODO
unsigned integer(unit) didn't include negative integer and used in the type that would never less than 0. RGB, bfsize, for example.
integer, in other case, was signed to those value would less than 0 in sometimes such as biWidth.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

TODO
BYTE 1bytes DWORD 4bytes LONG 4bytes WORD 2bytes

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

TODO
bfType

## What's the difference between `bfSize` and `biSize`?

TODO
the bfSize is the BMP file size contained in FILEHEADER but the bisize is the number of bytes required by the INFOHEADER.

## What does it mean if `biHeight` is negative?

TODO
it would be a top-down DIB in the case of biHeight is negative.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

TODO
biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

TODO
When the case the file should be open doesn't exist in this directory.

## Why is the third argument to `fread` always `1` in our code?

TODO
Because we just need to read info and file header for 1 time to ensure what format it is.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

TODO
0x00

## What does `fseek` do?

TODO
to change the pointer to the location you want such as fseek(inptr, padding, SEEK_CUR); means set ptr to "padding" bytes from current position.

## What is `SEEK_CUR`?

TODO
current position in file

## Whodunit?

TODO
Professor Plum.
