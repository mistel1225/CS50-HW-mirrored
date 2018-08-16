#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    int k;
    string plaintext;
    int i;
    if (argc != 2)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }
    if (argc == 2)
    {
        k = atoi(argv[1]);

        if (k < 0)
        {
            printf("Usage: ./caesar k\n");
            return 1;
        }
        else
        {
            plaintext = get_string("plaintext: ");
            printf("ciphertext: ");

            for (i = 0; i < strlen(plaintext); i++)
            if islower(plaintext[i])
                {
                    printf("%c", (((plaintext[i] + k) - 97) % 26) + 97);
                }
            else if isupper(plaintext[i])
                {
                    printf("%c", (((plaintext[i] + k) - 65) % 26) + 65);
                }
            else printf("%c", plaintext[i]);
        }
        printf("\n");
        return 0;
    }
}
