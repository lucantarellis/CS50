#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int convert(string input);

int main(void)
{
    string input = get_string("Enter a positive integer: ");

    for (int i = 0, n = strlen(input); i < n; i++)
    {
        if (!isdigit(input[i]))
        {
            printf("Invalid Input!\n");
            return 1;
        }
    }

    // Convert string to int
    printf("%i\n", convert(input));
}

int convert(string input)
{
    // TODO
    int num = 0, counter = 0, n = strlen(input);
    char cInput[n];
    strcpy(cInput, input);

    if(counter == n)
    {
        return num;
    }

    convert(input);

    if (cInput[counter] >= '0' && cInput[counter] <= '9')
    {
        num = num * 10 + (cInput[counter] - '0');
        counter++;
    }
    return num;
}