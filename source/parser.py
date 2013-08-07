#!/usr/bin/python
# -*- coding: utf-8 -*- 
from lexer import *
from enum import *

class TreeNode:
    __NodeKindList = Enum.enum {
        "STMT", "EXP", "DEK"
    }

    __SmtKindList = Enum.enum {
        "IF", "FOR", "RETURN", "COMPOUND", "FUNC_CALL", "FUNC_DECLARE"
    }

    __ExpKindList = Enum.enum {
        "OP", "CONST", "ID", "ASSIGN","RANGE"
    }

    __DecKindList = Enum.enum {
        "SCALARDEC", "FUNCDEC", "MATRIXDEC"
    }

    @staticmethod
    def getKindLIst():
        return __NodeKindList, __SmtKindList,  __ExpKindList, __DecKindList

    @staticmethod
    def getNodeKindList(self):
        return self.__NodeKindList

    def __init__(self,nodeK ,subK,attr,lineno):
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
        self.NodeKind, self.SmtKind, self.ExpKind, self.DecKind = TreeNode.getKindList()

    def __syntaxError(self,err):
        print "\n>>> Syntax error at line %d: %s" %(self.token.lineno, err)

    def __match(selfexpectType):
        if  self.token.tokenType == expectType :
            self.token = self.lexer.getToken()
        else:
            __syntaxError("unexpected token ->")
            print self.TokenType.reverse_mapping[self.token],"       "

    def __stmt_sequence(self):
        t = self.__statement()
        p = t

        while self.token.tokenType != self.TokenType.ENDFILE and  self.token.tokenType != self.TokenType.END and self.token.tokenType != self.TokenType.ELSE :
            self.__match(self.TokenType.SEMI)
            q = self.__statement()
            if q :
                if not t:
                    t = p = q
                else:
                    p.sibling = q
                    p = q
        return t

    def __statement(self):

        if self.token.tokenType == self.TokenType.ID:
            t = self.__expression_smt()

        return t

    def __expression_smt(self):
        t = self.__expression()
        self.__match(self.TokenType.SEMI)
        return t

    def __expression(self):
        if self.token.tokenType == self.TokenType.ID:
            lvalue = self.__ident_statement()
            gotlvalue = True

        #Assignment ?
        if gotlvalue and self.token.tokenType == self.TokenType.ASSIGN:
            if  lvalue and lvalue.nodeKind == self.NodeKind.EXP and lvalue.subkind = self.ExpKind.ID:
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
        else:
            t = self.__simple_expression(lvalue)

        return t



    def __simple_expression(self,passdown):
        lExpr = self.__additive_expression(passdown)

        if self.token.tokenType in (self.TokeyType.GT, self.TokenType.LT, self.TokeyType.LE, self.TokeyType.GE, self.TokeyType.EQ, self.TokeyType.UNEQ):
            operator = token.tokenType

            t = TreeNode(
                        self.NodeKind.EXP,
                        self.ExpKind.OP,
                        self.token.tokenType,
                        self.token.lineno
            )

            match(operator)
            rExpr = self.__additive_expression()
            t.child.append(lExpr)
            t.child.append(rExpr)
        else:
            t = lExpr

        return t;
    }

    def __additive_expression(self,passdown):
        t = self.__term(passdown)
        while self.token.tokenType == self.TokenType.PLUS or self.token.tokenType == self.TokenType.MINUS:

            newNode = TreeNode(
                        self.NodeKind.EXP,
                        self.ExpKind.OP,
                        self.token.tokenType,
                        self.token.lineno
            )
            newNode.child.append(t)
            t = newNode
            self.__match(self.token.tokenType)
            t.child.append(self.__term(None))

        return t

    # * or /
    def __term(self,passdown):
        t = self.__factor(passdown)
        while self.token.tokenType == self.TokenType.TIMES or self.token.tokenType == self.TokenType.DIV:
            newNode = TreeNode(
                        self.NodeKind.EXP,
                        self.ExpKind.OP,
                        self.token.tokenType,
                        self.token.lineno
            )
            newNode.child.append(t)
            t = newNode
            self.__match(self.token.tokenType)
            t.child.append(self.__factor(None))

        return t

    def __factor(self,passdonw):
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
                        self.token.tokenType,
                        self.token.lineno
            )
            t.attr = self.token.tokenValue
            self.__match(self.TokenType.NUM)
        else
            self.__syntaxError("unexpected token")
            self.token = self.lexer.getToken()
        return t

    def __ident_statement(self):
        if  self.token.tokenType == self.TokenType.ID:
            identifier = self.token.tokenValue
            self.__match(self.TokenType.ID)
             #function call ------- ID(arguments)
            if  self.token.tokenType == self.TokenType.LPAREN:
                self.__match(self.TokenType.LPAREN)
                arguments = self.__args()
                self.__match(self.TokenType.RPAREN)

                t = TreeNode(
                            self.NodeKind.STMT,
                            self.StmtKind.CALL,
                            self.token.tokenType,
                            self.token.lineno
                )
                t.child.append(arguments)
                t.attr = indentifier
            else:
                t = TreeNode(
                    self.NodeKind.EXP,
                    self.EXPKind.ID,
                    self.token.tokenType,
                    self.token.lineno
                )
                t.attr = identifier
        else:
            #[row] 
            if self.token.tokenType == self.TokenType.LBRACKET:
                self.__match(self.TokenType.LBRACKET)
                mat_range = sefl.__row()
                self.__match(self.TokenType.RBRACKET)

               # t = TreeNode(
               #             self.NodeKind.EXP,
               #             self.EXPKind.RANGE,
               #             self.token.tokenType,
               #             self.token.lineno
               # )
               # t.child.append(mat_range)
               t = mat_range
        return t

    def __args(self):
        t = None
        if self.token.tokenType == self.TokenType.RPAREN:
            t = self.__arg_list()
        return t

    def __arg_list(self):
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
            t.sibling.append(self.__col())
        return t

    def __col(self):
        t = TreeNode(
                    self.NodeKind.EXP,
                    self.EXPKind.RANGE,
                    self.token.tokenType,
                    self.token.lineno
        )
        t.child.append(self.__mat_range())
        self.__match(self.TokenType.COL)
        t.child.append(self.__mat_range())
        return t

    def __mat_range(self):
        if self.token.tokenType == self.TokenType.ID:
            t = TreeNode(
                    self.NodeKind.EXP,
                    self.EXPKind.ID,
                    self.token.tokenType,
                    self.token.lineno
            )
            t.attr = self.token.tokenValue
            self.__match(self.TokenType.ID)
        elif self.token.tokenType == self.TokenType.NUM:
            t = TreeNode(
                    self.NodeKind.EXP,
                    self.EXPKind.CONST,
                    self.token.tokenType,
                    self.token.lineno
            )
            t.attr = self.token.tokenValue
            self.__match(self.TokenType.NUM)
        elif self.token.tokenType == self.TokenType.COL
            t = None
        else
            self.__syntaxError("unexpected token")
            self.token = self.lexer.getToken()
            t = None
        return t

