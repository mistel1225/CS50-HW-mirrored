#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    string k;
    string plaintext;
    if (argc != 2)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }
    else
    {
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if (!isalpha(argv[1][i]))
            {
                printf("invalid key\n");
                return 1;
            }
        }
    }

    k = argv[1];

    plaintext = get_string("plaintext: ");

    printf("ciphertext: ");
    int klen = strlen(k);

    for (int j = 0, i = 0;  i < strlen(plaintext) ; i++)
    {
        int key = toupper(k[j % klen]) - 'A';
        if (islower(plaintext[i]))
            {
                printf("%c", (plaintext[i] - 'a' + key) % 26 + 'a');
                j++;
            }
        else if (isupper(plaintext[i]))
            {
                printf("%c", (plaintext[i] - 'A' + key) % 26 + 'A');
                j++;
            }
        else printf("%c", plaintext[i]);
    }
    printf("\n");
    return 0;
}
