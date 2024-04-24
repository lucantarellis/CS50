#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Not proper usage. Only one command-line argument accepted.\n");
        return 1;
    }

    char *input = argv[1];
    FILE *file = fopen(input, "r");

    if (file == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    BYTE buffer[512];
    FILE *img_ptr = NULL;
    int i = 0;
    int block_size = 512;
    char filename[8];

    while (fread(buffer, 1, block_size, file) == block_size)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (i != 0)
            {
                fclose(img_ptr);
            }

            sprintf(filename, "%03i.jpg", i);
            img_ptr = fopen(filename, "w");
            i++;
        }
        if (i != 0)
        {
            fwrite(buffer, 1, block_size, img_ptr);
        }
    }
    fclose(file);
    fclose(img_ptr);
}