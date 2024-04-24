#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h;

    do
    {
        h = get_int("Height: ");
    }
    while (h <= 0 || h > 8);

    int m = 1;

    for (int i = 0; i < h + i; i++)
    {
        for (int j = h - 1; j != 0; j--)
        {
            printf(" ");
        }
        for (int k = 0; k < m; k++)
        {
            printf("#");
        }
        for (int l = 0; l < 2; l++)
        {
            printf(" ");
        }
        for (int n = 0; n < m; n++)
        {
            printf("#");
        }
        printf("\n");
        h--;
        m++;
    }
}