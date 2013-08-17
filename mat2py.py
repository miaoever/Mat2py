#!/usr/bin/python
# -*- coding: utf-8 -*-

from source.codeGen import *
import sys

def main(args):
    if len(args) == 1:
        source = args[0]
        gen = CodeGen(source)
    elif len(args) == 2:
        source = args[0]
        output = args[1]
        gen = CodeGen(source, output)
    else:
        print ">> Please input the source file ."
        exit()
    gen.generate()
if __name__ == "__main__":
    main(sys.argv[1:])
