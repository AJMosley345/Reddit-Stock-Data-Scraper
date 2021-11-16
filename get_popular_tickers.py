from slowprint.slowprint import slowprint
from get_crypto import runCrypto
from get_stocks import runStocks
from get_wsb_stocks import runWSB

def main():
    w = True
    slowprint("Enter 1, 2 or 3.", .3)
    o_t = input()
    while w:
        if o_t == "1":
            runWSB()
            print('\n')
            w = False
        elif o_t == "2":
            runStocks()
            print('\n')
            w = False
        elif o_t == "3":
            runCrypto()
            w = False
        else:
            slowprint("Please enter 1, 2 or 3.", .3)
            
if __name__ == '__main__':
    main()