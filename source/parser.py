#!/usr/bin/python
# -*- coding: utf-8 -*-
from lexer import *
from enum import *

class TreeNode:

    @staticmethod
    def getKindList():
        __NodeKindList = Enum.enum (
            "STMT", "EXP", "DEK"
        )

        __SmtKindList = Enum.enum (
            "IF", "FOR", "WHILE", "RETURN", "COMPOUND", "FUNC_DECLARE"
        )

        __ExpKindList = Enum.enum (
            "OP", "CONST", "ID", "STRING", "ASSIGN","RANGE", "STEP", "FUNC_CALL", "VECTOR"
        )

        __DecKindList = Enum.enum (
            "SCALARDEC", "FUNCDEC", "MATRIXDEC"
        )
        return __NodeKindList, __SmtKindList,  __ExpKindList, __DecKindList

    def __init__(self,nodeK ,subK,attr = None ,lineno = 0):
        self.lineno = lineno
        self.nodekind = nodeK   #node kind - statement or expression
        self.subkind = subK     # sub kind of node kind
        self.sibling = []
        self.child = []
        self.attr = ""

class Parser:
    def __init__(self,source):
        self.lexer = Lexer(source)
        self.TokenType = Token.getTokenTypeList()
        self.NodeKind, self.StmtKind, self.ExpKind, self.DecKind = TreeNode.getKindList()
        self.FuncTable = []

    def __syntaxError(self,err):
        print "\n>>> Syntax error at line %d: %s" %(self.token.lineno, err)

    def __match(self,expectType):
        if  self.token.tokenType == expectType :
            self.token = self.lexer.getToken()
        else:
            #self.__syntaxError("unexpected token -> " + self.TokenType.reverse_mapping[self.token.tokenType])
            self.__syntaxError("unexpected token -> " + self.token.tokenValue)
            print ">>> Expecting token -> ", self.TokenType.reverse_mapping[expectType]

    def __stmt_list(self):
        t = self.__statement()
        ptr = t

        while self.token.tokenType not in (self.TokenType.ENDFILE, self.TokenType.END, self.TokenType.ELSE):
            newNode = self.__statement()
            if ptr and newNode:
                ptr.sibling.append(newNode)
                ptr = newNode

        return t

    def __statement(self):
        if self.token.tokenType == self.TokenType.IF:
            t = self.__selection_stmt()
        elif self.token.tokenType == self.TokenType.FOR:
            t = self.__forLoop_stmt()
        elif self.token.tokenType == self.TokenType.WHILE:
            t = self.__whileLoop_stmt()
        elif self.token.tokenType == self.TokenType.ID or self.token.tokenType == self.TokenType.NUM or self.token.tokenType == self.TokenType.LBRACKET:
            t = self.__expression_stmt()
        elif self.token.tokenType == self.TokenType.FUNCTION:
            t = self.__func_declaration()
        elif self.token.tokenType == self.TokenType.RETURN:
            t = self.__return_stmt()
        else:
            self.__syntaxError("unexpected token -> " + self.token.tokenValue)
            #self.token = self.lexer.getToken()
            t = None

        return t

    def __return_stmt(self):
        t = TreeNode(
                    self.NodeKind.STMT,
                    self.StmtKind.RETURN,
                    self.token.TokenType,
                    self.token.lineno
                )
        self.__match(self.TokenType.RETURN)
        return t

    def __selection_stmt(self):
        self.__match(self.TokenType.IF)
        ifCond = self.__expression()
        #thenStmt = self.__statement()
        thenStmt = self.__stmt_list()

        elseStmt = None
        if self.token.tokenType == self.TokenType.ELSE:
            self.__match(self.TokenType.ELSE)
            #elseStmt = self.__statement()
            elseStmt = self.__stmt_list()

        t = TreeNode(
                    self.NodeKind.STMT,
                    self.StmtKind.IF
                )
        t.child.append(ifCond)
        t.child.append(thenStmt)
        t.child.append(elseStmt)
        self.__match(self.TokenType.END)

        return t

    def __forLoop_stmt(self):
        self.__match(self.TokenType.FOR)
        forCond = self.__for_cond()
        if self.token.tokenType == self.TokenType.COMMA:
            self.__match(self.TokenType.COMMA)
        forStmt = self.__stmt_list()
        t = TreeNode(
                    self.NodeKind.STMT,
                    self.StmtKind.FOR
                )
        t.child.append(forCond)
        t.child.append(forStmt)
        self.__match(self.TokenType.END)

        return t

    def __for_cond(self):
        lvalue = TreeNode(
                        self.NodeKind.EXP,
                        self.ExpKind.ID,
                        self.token.tokenValue,
                        self.token.lineno
                )
        #lvalue.attr = self.token.tokenValue
        self.__match(self.TokenType.ID)
        self.__match(self.TokenType.ASSIGN)
        rvalue = self.__loop_step()
        t = TreeNode(
                    self.NodeKind.EXP,
                    self.ExpKind.ASSIGN,
                    self.token.tokenValue,
                    self.token.lineno
            )
        t.child.append(lvalue)
        t.child.append(rvalue)

        return t

    # begin:step:end
    def __loop_step(self):
        begin = self.__factor(None)
        self.__match(self.TokenType.COL)
        temp = self.__factor(None)
        if self.token.tokenType == self.TokenType.COL:
            self.__match(self.TokenType.COL)
            step = temp
            end = self.__factor(None)
        else:
            step = None
            end = temp
        t = TreeNode(
                    self.NodeKind.EXP,
                    self.ExpKind.STEP,
                    self.token.tokenValue,
                    self.token.lineno
                )
        t.child.append(begin)
        t.child.append(step)
        t.child.append(end)

        return t

    def __whileLoop_stmt(self):
        self.__match(self.TokenType.WHILE)
        whileCond = self.__expression()
        whileStmt = self.__stmt_list()
        t = TreeNode(
                    self.NodeKind.STMT,
                    self.StmtKind.WHILE
                )
        t.child.append(whileCond)
        t.child.append(whileStmt)
        self.__match(self.TokenType.END)

    def __func_declaration(self):
        self.__match(self.TokenType.FUNCTION)
        if self.token.tokenType == self.TokenType.LBRACKET:
            self.__match(self.TokenType.LBRACKET)
            return_param = self.__col()
            self.__match(self.TokenType.RBRACKET)
        else:
            #return_param = self.__mat_range()
            return_param = self.__factor(None)
        self.__match(self.TokenType.ASSIGN)
        func_name  = self.token.tokenValue

        #add user-define function to function-table
        self.FuncTable.append(func_name)

        self.__match(self.TokenType.ID)
        self.__match(self.TokenType.LPAREN)
        arguments = self.__args()
        self.__match(self.TokenType.RPAREN)
        func_body = self.__stmt_list()
        self.__match(self.TokenType.END)

        t = TreeNode(
                    self.NodeKind.STMT,
                    self.StmtKind.FUNC_DECLARE,
                    func_name,
                    self.token.lineno
                )
        t.child.append(arguments)
        t.child.append(func_body)
        t.child.append(return_param)
        #t.attr = func_name

        return t

    def __expression_stmt(self):
        t = self.__expression()
        #end up with ; or empty
        if self.token.tokenType == self.TokenType.SEMI:
            self.__match(self.TokenType.SEMI)
        return t

    def __expression(self):
        gotlvalue = False
        lvalue = None
        if self.token.tokenType in (self.TokenType.ID, self.TokenType.LBRACKET,  self.TokenType.STRING):
            lvalue = self.__ident_statement()
            gotlvalue = True

        #Assignment ?
        if gotlvalue and self.token.tokenType == self.TokenType.ASSIGN:
            if  lvalue and lvalue.nodekind == self.NodeKind.EXP and (lvalue.subkind in (self.ExpKind.ID, self.ExpKind.RANGE, self.ExpKind.FUNC_CALL, self.ExpKind.VECTOR)):
                self.__match(self.TokenType.ASSIGN)
                rvalue = self.__expression()

                t = TreeNode(
                            self.NodeKind.EXP,
                            self.ExpKind.ASSIGN,
                            self.token.tokenType,
                            self.token.lineno
                        )
                t.child.append(lvalue)
                t.child.append(rvalue)
            else:
                self.__syntaxError("attemp to assign to something not an left-value. \n ")
                t = None
        else:
            t = self.__simple_expression(lvalue)

        return t

    def __simple_expression(self,passdown):
        lExpr = self.__additive_expression(passdown)

        if self.token.tokenType in (self.TokenType.GT, self.TokenType.LT, self.TokenType.LE, self.TokenType.GE, self.TokenType.EQ, self.TokenType.UNEQ, self.TokenType.LOGICAND, self.TokenType.LOGICOR):
            operator = self.token.tokenType

            t = TreeNode(
                        self.NodeKind.EXP,
                        self.ExpKind.OP,
                        self.token.tokenValue,
                        self.token.lineno
            )

            self.__match(operator)
            rExpr = self.__additive_expression(None)
            t.child.append(lExpr)
            t.child.append(rExpr)
        elif self.token.tokenType in (self.TokenType.LOGICAND, self.TokenType.LOGICOR):
            #dosth
            a = 1
        else:
            t = lExpr

        return t;

    def __additive_expression(self,passdown):
        t = self.__term(passdown)

        while self.token.tokenType == self.TokenType.PLUS or self.token.tokenType == self.TokenType.MINUS:

            newNode = TreeNode(
                        self.NodeKind.EXP,
                        self.ExpKind.OP,
                        self.token.tokenValue,
                        self.token.lineno
            )
            newNode.child.append(t)
            t = newNode
            self.__match(self.token.tokenType)
            t.child.append(self.__term(None))

        return t

    # * , /
    def __term(self,passdown):
        #t = self.__factor(passdown)
        t = self.__transpose(passdown)
        while self.token.tokenType == self.TokenType.TIMES or self.token.tokenType == self.TokenType.DIV:
            newNode = TreeNode(
                        self.NodeKind.EXP,
                        self.ExpKind.OP,
                        self.token.tokenValue,
                        self.token.lineno
            )
            newNode.child.append(t)
            t = newNode
            self.__match(self.token.tokenType)
            #t.child.append(self.__factor(None))
            t.child.append(self.__transpose(None))
        return t

    #handle transpose
    def __transpose(self,passdown):
        t = self.__elem(passdown)
        if self.token.tokenType == self.TokenType.TRANSPOSE:
            newNode = TreeNode(
                    self.NodeKind.EXP,
                    self.ExpKind.OP,
                    self.token.tokenValue,
                    self.token.lineno
            )
            #newNode.attr = self.token.tokenValue
            newNode.child.append(t)
            t = newNode
            self.__match(self.TokenType.TRANSPOSE)

    #handle power
    def __elem(self,passdown):
        t = self.__factor(passdown)
        if self.token.tokenType == self.TokenType.POW:
            newNode = TreeNode(
                        self.NodeKind.EXP,
                        self.ExpKind.OP,
                        self.token.tokenValue,
                        self.token.lineno
            )
            newNode.child.append(t)
            t = newNode
            self.__match(self.TokenType.POW)
            t.child.append(self.__factor(None))

        return t

    #factor -> (expression) | identifier | NUM | [Matric] | STRING
    def __factor(self,passdown):
        if passdown:
            return passdown

        if self.token.tokenType == self.TokenType.ID or self.token.tokenType == self.TokenType.LBRACKET:
            t = self.__ident_statement()
        elif self.token.tokenType == self.TokenType.LPAREN:
            self.__match(self.TokenType.LPAREN)
            t = self.__expression()
            self.__match(self.TokenType.RPAREN)
        elif self.token.tokenType == self.TokenType.NUM:
            t = TreeNode(
                        self.NodeKind.EXP,
                        self.ExpKind.CONST,
                        self.token.tokenValue,
                        self.token.lineno
            )
            self.__match(self.TokenType.NUM)
        elif self.token.tokenType == self.TokenType.STRING:
            t = TreeNode(
                        self.NodeKind.EXP,
                        self.ExpKind.STRING,
                        self.token.tokenValue,
                        self.token.lineno
                    )
            self.__match(self.TokenType.STRING)

        else:
            #self.__syntaxError("unexpected token -> " + self.token.tokenValue)
            #self.token = self.lexer.getToken()
            t = None
        return t

    #identifier ---- everything which could be left-value
    def __ident_statement(self):
        if  self.token.tokenType == self.TokenType.ID:
            identifier = self.token.tokenValue
            self.__match(self.TokenType.ID)
             #function call ------- ID(arguments)
            if  self.token.tokenType == self.TokenType.LPAREN:
                self.__match(self.TokenType.LPAREN)
                #arguments = self.__args()
                arguments = self.__col()
                self.__match(self.TokenType.RPAREN)

                t = TreeNode(
                            self.NodeKind.EXP,
                            self.ExpKind.FUNC_CALL,
                            identifier,
                            self.token.lineno
                )
                t.child.append(arguments)
                #t.attr = identifier
            else:
                t = TreeNode(
                    self.NodeKind.EXP,
                    self.ExpKind.ID,
                    identifier,
                    self.token.lineno
                )
                #t.attr = identifier
            #[row]
        elif self.token.tokenType == self.TokenType.LBRACKET:
                self.__match(self.TokenType.LBRACKET)
                t = TreeNode(
                        self.NodeKind.EXP,
                        self.ExpKind.VECTOR,
                        self.token.tokenValue,
                        self.token.lineno
                    )
                mat_range = self.__row()
                t.child.append(mat_range)
                self.__match(self.TokenType.RBRACKET)
        return t

    def __args(self):
        t = None
        if self.token.tokenType != self.TokenType.RPAREN:
            t = self.__arg_list()
        return t

    def __arg_list(self):
        if self.token.tokenType == self.TokenType.STRING:
            t = TreeNode(
                        self.NodeKind.EXP,
                        self.ExpKind.STRING,
                        self.token.tokenValue,
                        self.token.lineno
                    )
            #t.attr = self.token.tokenValue
            self.__match(self.TokenType.STRING)
        else:
            t = self.__expression()
        ptr = t

        while self.token.tokenType == self.TokenType.COMMA:
            self.__match(self.TokenType.COMMA)
            newNode = self.__expression()
            if ptr and t:
                ptr.sibling.append(newNode)
                ptr = newNode

        return t

    def __row(self):
        t = self.__col()
        while self.token.tokenType == self.TokenType.SEMI:
            self.__match(self.TokenType.SEMI)
            newNode = self.__col()
            if t:
                t.sibling.append(newNode)
            else:
                t = newNode
        return t

    def __col(self):
        newNode = self.__simple_expression(None)
        # [mat_range:mat_range]
        if self.token.tokenType == self.TokenType.COL:
            self.__match(self.TokenType.COL)
            t = TreeNode(
                        self.NodeKind.EXP,
                        self.ExpKind.RANGE,
                        self.token.tokenType,
                        self.token.lineno
            )
            t.child.append(newNode)
            t.child.append(self.__simple_expression(None))
        #[mat_range,mat_range]
        else:
            t = newNode
        while self.token.tokenType == self.TokenType.COMMA:
            self.__match(self.TokenType.COMMA)
            newNode2 = self.__col()
            if t:
                t.sibling.append(newNode2)
            else:
                t = newNode2

        return t

    def parse(self):
        self.token = self.lexer.getToken()
        t = self.__stmt_list()
        if self.token.tokenType != self.TokenType.ENDFILE:
            self.__syntaxError("Unexpected symbol at end of file\n")
        return t, self.FuncTable
