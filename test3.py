#!/usr/bin/python
# -*- coding: utf-8 -*- 

from source.codeGen import *
import pdb 
def main():
    source = "opt_NP3.m"
    output = "output.py"
    gen = CodeGen(source, output)
    #gen = CodeGen(source)
    gen.generate()
if __name__ == "__main__":
    main()
