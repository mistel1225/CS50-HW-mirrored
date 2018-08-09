#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    int r;
    int i;
    do
    {
        height = get_int("height: ");
        for (r = 0; r < height; r++)
        {
            for (i=height-r-1; i > 0; i--)
            {
                printf(" ");
            }
            for (i=0; i < r+2; i++)
            {
                printf("%c", '#');
            }
        printf("\n");
        }
    }while (height > 23 || height < 0);
}