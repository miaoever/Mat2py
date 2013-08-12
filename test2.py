#!/usr/bin/python
# -*- coding: utf-8 -*- 

from source.parser import *

def main():
    source = "test_NP2.m"
    #source = "test3.m"
    parser = Parser(source)
    t,FuncTable = parser.parse()
    print FuncTable
if __name__ == "__main__":
    main()
