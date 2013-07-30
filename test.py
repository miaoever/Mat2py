from lexer import *

def main():
    source = "test.m"
    token = Token(source)
    tokenString = ""
    while True:
        tokenString,tokenType = token.getToken()
        if  tokenString:
            print tokenString
        else:
            break

if __name__ == "__main__":
    main()
