// Check that a password has at least one lowercase letter, uppercase letter, number and symbol
// Practice iterating through a string
// Practice using the ctype library

#include <cs50.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

bool valid(string password);

int main(void)
{
    string password = get_string("Enter your password: ");
    if (valid(password))
    {
        printf("Your password is valid!\n");
    }
    else
    {
        printf("Your password needs at least one uppercase letter, lowercase letter, number and symbol\n");
    }
}

// TODO: Complete the Boolean function below
bool valid(string password)
{
    //Create a array of characters that has the length of the string "password".
    char passChar[strlen(password)];
    //Copy the contents of the string "password" into the character array.
    strcpy(passChar, password);
    //Create an int that stores the lenght of the password.
    int lenght = strlen(passChar);
    //Set boolean values to false.
    bool hasLower = false, hasUpper = false, hasDigit = false, hasSymbol = false;

    //Scan for every letter in the password and set the boolean to true if the condition is met.
    for (int i = 0; i < lenght; i++)
    {
        if (islower(passChar[i]))
        {
            hasLower = true;
        }
        else if (isupper(passChar[i]))
        {
            hasUpper = true;
        }
        else if (isdigit(passChar[i]))
        {
            hasDigit = true;
        }
        else if (ispunct(passChar[i]))
        {
            hasSymbol = true;
        }
    }
    //Return the boolean values, if at least one of them is false, the function valid will be false.
    return hasLower && hasUpper && hasDigit && hasSymbol;
}
