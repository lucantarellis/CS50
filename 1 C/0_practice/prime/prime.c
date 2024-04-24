#include <cs50.h>
#include <stdio.h>

bool prime(int number);

int main(void)
{
    int min;
    do
    {
        min = get_int("Minimum: ");
    }
    while (min < 1);

    int max;
    do
    {
        max = get_int("Maximum: ");
    }
    while (min >= max);

    for (int i = min; i <= max; i++)
    {
        if (prime(i))
        {
            printf("%i\n", i);
        }
    }
}

bool prime(int number)
{
    // Checking if number is greater than 1 (1 is not prime).
    if (number <= 1)
    {
        return false;
    }

    // This loops checks if the integer number is divisible by the range 2 to number and returns true or false whether it's divisible or not.

    for (int i = 2; i < number; i++)
    {
        // If the modulus of number returns a value equal to 0, it means it's divisible so it is not prime, thus returning false.
        if (number % i == 0)
        {
            return false;
        }
    }
    return true;
}
