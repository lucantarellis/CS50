#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");
    //printf("Text: %s\n", text);
    int totalLetters = count_letters(text);
    //printf("The number of letters in this text are: %i\n", totalLetters);
    int totalWords = count_words(text);
    //printf("The number of words in this text are: %i\n", totalWords);
    int totalSents = count_sentences(text);
    //printf("The number of sentences in this text are: %i\n", totalSents);

    float avgLetters = (float) totalLetters / totalWords * 100;
    //printf("%f avgLet\n", avgLetters);
    float avgSents = (float) totalSents / totalWords * 100;
    //printf("%f avgSents\n", avgSents);
    float index = 0.0588 * avgLetters - 0.296 * avgSents - 15.8;
    int indexRound = round(index);
    if (indexRound < 0)
    {
        printf("Before Grade 1\n");
    }
    else if (indexRound > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", indexRound);
    }
}

// Functions described below

int count_letters(string text)
{
    int letterCount = 0;
    long length = strlen(text);
    char countChar[strlen(text)];
    strcpy(countChar, text);

    for (long i = 0; i < length; i++)
    {
        if (isalpha(countChar[i]))
        {
            letterCount++;
        }
    }
    return letterCount;
}

int count_words(string text)
{
    int wordCount = 0;
    long length2 = strlen(text);
    char countChar2[strlen(text)];
    strcpy(countChar2, text);

    for (int i = 0; i < length2 + 1; i++)
    {
        if (isspace(countChar2[i]) || countChar2[i] == '\0')
        {
            wordCount++;
        }
    }
    return wordCount;
}


int count_sentences(string text)
{
    int sentCount = 0;
    long length3 = strlen(text);
    char countChar3[strlen(text)];
    strcpy(countChar3, text);

    if (isblank(countChar3[length3]))
    {
        sentCount++;
    }

    for (int i = 0; i < length3; i++)
    {
        if (countChar3[i] == '.' || countChar3[i] == '!' || countChar3[i] == '?')
        {
            sentCount++;
        }
    }
    return sentCount;
}