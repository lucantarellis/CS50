#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long cardNum = get_long("Credit card's number: ");
    long cardTemp = cardNum;
    int cardCalc = 0, sum1 = 0, sum2 = 0;

    //Looping while the credit card number is greater than 0 to get sum1.
    while (cardTemp > 0)
    {
        //Using cardCalc to sum up every other number, starting with the number’s second-to-last digit. Note that cardCalc is an int.
        cardCalc = ((cardTemp / 10) % 10) * 2;
        //Store the sum of the numbers in sum1.
        if (cardCalc < 10)
        {
            sum1 += cardCalc;
        }
        //In case the number is greater than 10, because we need those products digits and numbers won't exceed 19,
        //we can substract 10 from the total and add 1 for the second digit.
        else
        {
            sum1 += (cardCalc - 10) + 1;
        }
        //Now that we have the numbers stored in sum1, we proceed to:
        //Divide cardNum so we move the decimal to the next number needed.
        cardTemp /= 100;
    }
    cardTemp = cardNum;
    cardCalc = 0;

    //Same as in sum1 but with sum2, the other digits
    while (cardTemp > 0)
    {
        cardCalc = cardTemp % 10;
        sum2 += cardCalc;
        cardTemp /= 100;
    }

    cardCalc = 0;
    cardCalc = (sum1 + sum2) % 10;

    //Now we check if the checksum equals 0, if so we proceed to evaluate whether is an AMEX, MASTERCARD or VISA.
    if (cardCalc != 0)
    {
        printf("INVALID\n");
        return 0;
    }
    else if (cardCalc == 0)
    {
        if ((cardNum / 10000000000000) == 37 || (cardNum / 10000000000000) == 34)
        {
            printf("AMEX\n");
            return 0;
        }
        if ((cardNum / 100000000000000) > 50 && (cardNum / 100000000000000) < 56)
        {
            printf("MASTERCARD\n");
            return 0;
        }
        if ((cardNum / 1000000000000) == 4 || (cardNum / 1000000000000000) == 4)
        {
            printf("VISA\n");
            return 0;
        }
        else
        {
            printf("INVALID\n");
            return 0;
        }
    }
}