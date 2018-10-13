import cs50
import sys
def main():
    ccNumber = cs50.get_int("What's your credit card number? ")
    validation = ccNumber
    countDigit = 0

    while(validation > 0):
        validation = validation//10
        countDigit+=1
    if countDigit != 13 and countDigit !=15 and countDigit != 16:
        print("INVALID")
        return sys.exit()
    #open a digit array to save digit
    digit=[]
    #open a check value to determine if the check =60
    check = 0
    for i in range(1,9):
        digit.append((ccNumber%(100**i))//(10**(2*i-1))*2)
    for k in range(0, 8):
        digit.append(ccNumber%(10**(2*k+1))//(100**k))
    for j in range(0,16):
        if digit[j] >= 10:
            check += (digit[j]%10+digit[j]%100//10)
        else:
            check += digit[j]
    if (int(check) % 10) != 0:
        print("INVALID")
        return 0
    amex = ccNumber // (10**13)
    if countDigit == 15:
        if amex != 34 and amex != 37:
            print("INVALID")
        else:
            print("AMEX")

    if countDigit == 16:
        if (digit[7]//2) == 4:
            print("VISA")
        else:
            mastercard = ccNumber // (10**14)
            if mastercard != 51 and mastercard != 52 and mastercard != 53 and mastercard != 54 and mastercard != 55:
                print("INVALID")
            else:
                print("MASTERCARD")


if __name__ == "__main__":
    main()