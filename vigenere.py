import cs50
import sys

#put a cypher key string in argv[1], which excepts to be a~z
def codecheck():
    if len(sys.argv)==2:
        cypherkey = sys.argv[1]
        for c in cypherkey:
            if c.isalpha() == 0:
                print("invalid key")
                return sys.exit(1)
        words = cs50.get_string("plaintext: ")
        cypher(cypherkey, words)
    else:
        print("usage: python vigenere.py key")
        return sys.exit(1)
def cypher(cypherkey, words):
    wordslen = len(words)
    cypherwords=''
    j = 0
    for i in range(wordslen):
        #repeat the key you parse into
        key = ord(cypherkey[j%len(cypherkey)].upper())-65

        if words[i].islower() == 1:
            cypherwords += chr((ord(words[i])-97+key)%26+97)
            j+=1
        elif words[i].isupper() == 1:
            cypherwords += chr((ord(words[i])-65+key)%26+65)
            j+=1
        else:
            cypherwords += words[i]
    print(f"ciphertext: {cypherwords}")


if __name__ == "__main__":
    codecheck()