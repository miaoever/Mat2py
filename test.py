#!/usr/bin/python
# -*- coding: utf-8 -*- 

from source.lexer import *
from source.token import *

def main():
    source = "test.m"
    lexer = Lexer(source)
    while True:
        token = lexer.getToken()
        if  token.tokenValue:
            print "<",token.lineno,",",token.tokenValue,",",token.tokenType,">"
        else:
            break

if __name__ == "__main__":
    main()
