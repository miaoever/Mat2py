#!/usr/bin/python
# -*- coding: utf-8 -*-
from parser import *
from lexer import *
from enum import *
import sys

class CodeGen:

    def __init__(self, inPath, outPath = None):
        self.TokenType = Token.getTokenTypeList()
        self.NodeKind, self.StmtKind, self.ExpKind, self.DecKind = TreeNode.getKindList()
        self.incident = 0
        self.inPath = inPath
        self.outPath = outPath

    def generate(self):
        #source = "test_NP2.m"
        #source = "test3.m"
        parser = Parser(self.inPath)
        self.ast,self.FuncTable = parser.parse()
        self.__genHeader()
        self.__traverse(self.ast)

    def __genHeader(self):
        self.__emitCode("#!/usr/bin/python\n")
        self.__emitCode("# -*- coding: utf-8 -*-\n")
        self.__emitCode("import numpy as np\n")
        self.__emitCode("import copy\n")
        self.__emitCode("import os\n")
        self.__emitCode("import sys\n\n")

    def __emitCode(self, content):
        if not self.outPath:
            sys.stdout.write(content)
        else:
            f = open(output,'w')
            f.write(content + '\n')

    def __traverse(self,curNode):
        if curNode != None:
            if curNode.nodekind == self.NodeKind.STMT:
                self.__genStmt(curNode)
            elif curNode.nodekind == self.NodeKind.EXP:
                self.__genExp(curNode)
            self.__emitCode("\n")

            for i in xrange(0, len(curNode.sibling)):
                self.__traverse(curNode.sibling[i])

    def __genExp(self,curNode):
        if not curNode:
            return
        if curNode.subkind == self.ExpKind.OP:
            if curNode.attr == "*":
                self.__emitCode("np.dot(")
                self.__genExp(curNode.child[0])
                self.__emitCode(",")
                self.__genExp(curNode.child[1])
                self.__emitCode(")")
            elif curNode.attr == "'":
                self.__genExp(curNode.child[0])
                self.__emitCode(".conj().T")
            else:
                self.__genExp(curNode.child[0])
                if curNode.attr == '^':
                    self.__emitCode("**")
                else:
                    self.__emitCode(" " + curNode.attr + " ")
                self.__genExp(curNode.child[1])

        elif curNode.subkind == self.ExpKind.CONST:
            self.__emitCode(curNode.attr)

        elif curNode.subkind == self.ExpKind.ID:
            self.__emitCode(curNode.attr)

        elif curNode.subkind == self.ExpKind.STRING:
            self.__emitCode(curNode.attr + "'")

        elif curNode.subkind == self.ExpKind.ASSIGN:
            self.__genExp(curNode.child[0])
            self.__emitCode(" = copy.deepcopy(")
            self.__genExp(curNode.child[1])
            self.__emitCode(")")

        elif curNode.subkind == self.ExpKind.STEP:
            self.__genExp(curNode.child[0])
            self.__emitCode(":")
            self.__genExp(curNode.child[1])
            self.__emitCode(":")
            self.__genExp(curNode.child[2])

        elif curNode.subkind == self.ExpKind.FUNC_CALL:
            self.__emitCode(curNode.attr + "(")
            self.__genExp(curNode.child[0])
            self.__emitCode(")")

        elif curNode.subkind == self.ExpKind.RANGE:
            self.__genExp(curNode.child[0])
            for i in xrange(0, len(curNode.sibling)):
                self.__traverse(curNode.sibling[i])

