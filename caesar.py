import cs50
import sys

def checklen():
    if len(sys.argv) == 2:
        k = int(sys.argv[1])
        if k >= 0:
            plaintext = cs50.get_string("plaintext: ")
            main(plaintext, k)
        else:
            print("input a positive number")
    else:
        print("usage:python caesar.py number")

def main(plaintext, k):
    cyphertext = ''
    for i in plaintext:
        if i.isalpha():
            if i.isupper():
                cyphertext += chr((ord(i)+k-65)%26+65)
            if i.islower():
                cyphertext += chr((ord(i)+k-97)%26+97)
        else:
            cyphertext += ' '
    print(cyphertext, end="")
    print("\n", end="")

if __name__ == "__main__":
    checklen()