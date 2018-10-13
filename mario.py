from cs50 import get_int
def main():
    height = get_int("height: ")
    if height < 23 and height > 0:
        mario(height)
    else:
        print("number should be heigher than 0 and less than 23")

def mario(height):
    for r in range(height):
        for i in range(0, height-r-1):
            print(" ", end="")
        for j in range(0, r+2):
            print('#', end="")
        print("")

if __name__ == "__main__":
    main()