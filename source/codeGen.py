#!/usr/bin/python
# -*- coding: utf-8 -*-
from parser import *
from lexer import *
from enum import *

class CodeGen:

    def __init(self):
        self.TokenType = Token.getTokenTypeList()
        self.NodeKind, self.StmtKind, self.ExpKind, self.DecKind = TreeNode.getKindList()

    def generate(self):
        source = "test_NP2.m"
        #source = "test3.m"
        parser = Parser(source)
        self.ast,self.FuncTable = parser.parse()
        self.__traverse()

    def __traverse(self,curNode):
        if curNode != None:
            if curNode.nodekind == self.NodeKind.STMT:
                self.__genStmt(curNode)
            elif curNode.nodeKind == self.NodeKind.EXP:
                self.__genExp(curNode)

            for i in xrange(0, len(curNode.sibling))
                self.__traverse(curNode.)

    def __genExp(self,curNode):
        if curNode.ExpKind == self.ExpKind.OP:
            self.__genExp(curNode.child[0])
            self.__emitCode(curNode.attr)
            self.__genExp(curNode.child[1])

        elif curNode.ExpKind == self.ExpKind.CONST:
            self.__emitCode(curNode.attr)

        elif curNode.ExpKind == self.ExpKind.ID:
            self.__emitCode(curNode.attr)

        elif curNode.ExpKind == self.ExpKind.STRING:
            self.__emitCode(curNode.attr + "'")

        elif curNode.ExpKind == self.ExpKid.ASSIGN:
            self.__genExp(curNode.child[0])
            self.__emitCode(" = ")
            self.__genExp(curNode.child[1])

        elif curNode.ExpKind == self.ExpKind.STEP:
            self.__genExp(curNode.child[0])
            self.__emitCode(":")
            self.__genExp(curNode.child[1])
            self.__emitCode(":")
            self.__genExp(curNode.child[2])

        elif curNode.ExpKind == self.ExpKind.FUNC_CALL:
            self.__emitCode(curNode.attr + "(")
            self.__genExp(curNode.child[0])
            self.__emitCode(")")

        elif curNode.ExpKind == self.ExpKind.RANGE:
            self.__genExp(curNode.child[0])
            for i in xrange(0, len(curNode.sibling))
                self.__traverse(curNode.)
            
