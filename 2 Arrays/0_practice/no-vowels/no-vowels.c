// Write a function to replace vowels with numbers
// Get practice with strings
// Get practice with command line
// Get practice with switch

#include <cs50.h>
#include <stdio.h>
#include <string.h>

void replace(string argv[1]);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Only one string allowed.\n");
        return 1;
    }
    else
    {
        replace(argv);
        printf("\n");
        return 0;
    }
}


void replace(string argv[1])
{
    int lenght = strlen(argv[1]);
    for (int i = 0; i < lenght; i++)
    {
        switch (argv[1][i])
        {
            case 97:
                printf("6");
                break;

            case 101:
                printf("3");
                break;

            case 105:
                printf("1");
                break;

            case 111:
                printf("0");
                break;

            default:
                printf("%c", argv [1][i]);
                break;
        }
    }
}