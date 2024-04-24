#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int start, end;

    do
    {
        start = get_int("Start size: ");
    }
    while (start <= 9);

    // TODO: Prompt for end size

    do
    {
        end = get_int("End size: ");
    }
    while (start > end);

    // TODO: Calculate number of years until we reach threshold
    int years = 0;

    while (start < end)
    {
        int born = start / 3;
        int dead = start / 4;
        start += born - dead;
        years++;
    }

    // TODO: Print number of years
    printf("Years: %i", years);
}
