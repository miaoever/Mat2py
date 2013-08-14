#!/usr/bin/python
# -*- coding: utf-8 -*-
from parser import *
from lexer import *
from enum import *
import sys
import os
import imp

class CodeGen:

    def __init__(self, inPath, outPath = None):
        self.TokenType = Token.getTokenTypeList()
        self.NodeKind, self.StmtKind, self.ExpKind, self.DecKind = TreeNode.getKindList()
        self.incident = 0
        self.libPath = os.path.dirname(os.path.abspath(__file__))+"/lib/"
        self.LibFunc = []
        self.__loadLibFunc()
        self.inPath = inPath
        self.outPath = outPath
        if outPath:
            self.out = open(self.outPath,'w')

    def __loadLibFunc(self):
        for filename in os.listdir(self.libPath):
            if os.path.splitext(filename)[1].lower() == ".py":
                self.LibFunc.append(os.path.splitext(filename)[0])


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

    def __emitIncident(self):
        if not self.outPath:
            sys.stdout.write(" " * 4 * self.incident)
        else:
            self.out.write(" " * 4 * self.incident)

    def __emitCode(self, content):
        if not self.outPath:
            #sys.stdout.write(" " * 4 * self.incident)
            sys.stdout.write(content)
            #sys.stdout.flush()
        else:
            self.out.write(content)

    def __traverse(self,curNode):
        if curNode != None:
            if curNode.nodekind == self.NodeKind.STMT:
                self.__genStmt(curNode)
            elif curNode.nodekind == self.NodeKind.EXP:
                self.__genExp(curNode)
            sibling = curNode.sibling
            while sibling:
                self.__traverse(sibling)
                sibling = sibling.sibling
            sys.stdout.flush()

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

        elif curNode.subkind == self.ExpKind.FUNC_CALL:
            if curNode.attr in self.FuncTable:
                self.__emitCode(curNode.attr + "(")
                self.__genExp(curNode.child[0])
                sibling = curNode.child[0].sibling
                while sibling != None :
                    self.__emitCode(", ")
                    self.__genExp(sibling)
                    sibling = sibling.sibling
                self.__emitCode(")")
            elif curNode.attr in self.LibFunc:
                #dynamic load lib function
                try:
                    lib_func_name = curNode.attr
                    lib_mod = imp.load_source(lib_func_name, self.libPath + lib_func_name + ".py")
                    result = getattr(lib_mod, lib_func_name.lower())()
                    self.__emitCode(result)
                except:
                    print "\n>> Error to load lib function : " + lib_func_name + "() <<\n"
            else:
                self.__emitCode(curNode.attr + "[")
                col = curNode.child[0]
                self.__genExp(col)
                self.__emitCode("]")

        #elif curNode.subkind == self.ExpKind.LIST:




        elif curNode.subkind == self.ExpKind.RANGE:
            self.__genExp(curNode.child[0])
            if curNode.child[1]:
                self.__emitCode(":")
                self.__genExp(curNode.child[1])

            sibling = curNode.sibling
            while sibling:
                self.__emitCode(", ")
                self.__genExp(sibling)
                sibling = sibling.sibling

    def __genStmt(self, curNode):
        if not curNode:
            return

        if curNode.subkind == self.StmtKind.IF:
            self.__emitIncident()
            self.__emitCode("if ")
            self.__genExp(curNode.child[0])
            self.__emitCode(":\n")
            self.incident += 1
            #self.__emitIncident()
            #Then statement
            thenStmt = curNode.child[1]
            self.__genStmt(thenStmt)
            sibling = thenStmt.sibling
            while sibling:
                self.__genStmt(sibling)
                sibling = sibling.sibling

            #Else statement
            if curNode.child[2]:
                self.incident -= 1
                self.__emitIncident()
                self.__emitCode("else:\n")
                self.incident += 1
                #self.__emitIncident()
                elseStmt = curNode.child[2]
                self.__genStmt(elseStmt)
                sibling = elseStmt.sibling
                while sibling:
                    self.__genStmt(sibling)
                    sibling = sibling.sibling
            self.incident -= 1

        elif curNode.subkind == self.StmtKind.FOR:
            self.__emitIncident()
            self.__emitCode("for ")
            forCond = curNode.child[0]
            self.__genExp(forCond.child[0])
            self.__emitCode(" = xrange(")
            forCond.child[1].attr = str(int(forCond.child[1].attr) - 1) #convert base 1 to base 0
            self.__genExp(forCond.child[1] )
            step = forCond.child[1].sibling
            #while sibling:
            self.__emitCode(",")
               # sibling.attr = int(sibling.attr) - 1 #convert base 1 to base 0
            self.__genExp(step)
            self.__emitCode(",")
            end = step.sibling
            end.attr = str(int(end.attr) - 1)
            self.__genExp(end)
            self.__emitCode("):\n")

            forStmt = curNode.child[1]
            self.incident +=1
            self.__genStmt(forStmt)
            sibling = forStmt.sibling
            while sibling:
                self.__genStmt(sibling)
                sibling = sibling.sibling

            self.incident -= 1

        elif curNode.subkind == self.StmtKind.WHILE:
            self.__emitIncident()
            self.__emitCode("while ")
            whileCond = curNode.child[0]
            self.__genExp(whileCond)
            self.__emitCode(":\n")
            self.incident += 1
            whileStmt = curNode.child[1]
            self.__genStmt(whileStmt)
            self.incident -= 1

        elif curNode.subkind == self.StmtKind.FUNC_DECLARE:
            self.__emitIncident()
            self.__emitCode("\ndef ")
            func_name = curNode.attr
            self.__emitCode(func_name+"(")

            #emit arguments
            arguments = curNode.child[0]
            self.__genExp(arguments)
            sibling = arguments.sibling
            while sibling:
                self.__emitCode(",")
                self.__genExp(sibling)
                sibling = sibling.sibling
            self.__emitCode("):\n")

            #emit function body
            self.incident += 1
            func_body = curNode.child[1]
            self.__genStmt(func_body)
            sibling = func_body.sibling
            while sibling:
                self.__genStmt(sibling)
                sibling = sibling.sibling

            #emit return parameters
            return_param = curNode.child[2]
            self.__emitIncident()
            self.__emitCode("return ")
            self.__genExp(return_param)
            sibling = return_param.sibling
            while sibling:
                self.__emitCode(",")
                self.__genExp(sibling)
                sibling = sibling.sibling

            self.incident -= 1

        else:
            self.__emitIncident()
            self.__genExp(curNode)
            self.__emitCode("\n")


