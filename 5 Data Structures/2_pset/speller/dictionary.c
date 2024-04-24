// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

int counter = 0;
int error = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Recursively frees all the nodes
void freeTable(node *hasht);

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int index = hash(word);
    node *cursor = table[index];

    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    // Original function: return toupper(word[0]) - 'A';
    // My attemp to create this hash code is to scan the first 3 words, sum their equivalent ASCII value and then return the modulo of N just in case the answer does not fall into the 0 to 26 range
    int n = 0;

    // Loop through the first 3 letters and checking in case the word has less than 3 letters
    for (int i = 0; i < 3 && word[i] != '\0'; i++)
    {
        n += (toupper(word[i]) - 'A');
    }

    // Make sure the result is in N range
    return n % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *input = fopen(dictionary, "r");
    if (input == NULL)
    {
        printf("Couldn't open dictionary.\n");
        return false;
        error = 1;
    }

    //Initialize hash table
    for (int i = 0; i <= N; i++)
    {
        table[i] = NULL;
    }

    //Read words from dictionary
    char word[LENGTH + 1];
    while (fscanf(input, "%s", word) != EOF)
    {
        //Calculate table index
        int index = hash(word);

        //Allocate memory for the new node
        node *tmp = malloc(sizeof(node));

        //Check if there's enough memory
        if (tmp == NULL)
        {
            fclose(input);
            return false;
        }

        //Copy current word to the new node
        strcpy(tmp->word, word);

        //Insert new node into the table
        if (table[index] == NULL)
        {
            table[index] = tmp;
            tmp->next = NULL;
            counter++;
        }
        else
        {
            tmp->next = table[index];
            table[index] = tmp;
            counter++;
        }
    }
    size();
    fclose(input);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (error == 1)
    {
        return 0;
    }
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        freeTable(table[i]);
    }
    return true;
}

// Recursively frees all the nodes
void freeTable(node *hasht)
{
    if (hasht == NULL)
    {
        return;
    }
    else if (hasht->next == NULL)
    {
        free(hasht);
        return;
    }
    freeTable(hasht->next);
    free(hasht);
}