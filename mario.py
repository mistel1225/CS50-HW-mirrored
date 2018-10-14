from cs50 import get_int
def main():
    height = get_int("height: ")
    checkHeight(height)

def checkHeight(height):
    if height < 24 and height >= 0:
        mario(height)
    else:
        main()

def mario(height):
    for r in range(height):
        for i in range(0, height-r-1):
            print(" ", end="")
        for j in range(0, r+2):
            print('#', end="")
        print("")

if __name__ == "__main__":
    main()