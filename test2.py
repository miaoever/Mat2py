#!/usr/bin/python
# -*- coding: utf-8 -*- 

from source.parser import *

def main():
    source = "test3.m"
    #source = "test3.m"
    parser = Parser(source)
    t = parser.parse()
if __name__ == "__main__":
    main()
