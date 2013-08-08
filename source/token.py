#!/usr/bin/python
# -*- coding: utf-8 -*- 

from enum import *

class Token:
    def __init__(self,Value ,Type ,lineno = 0):
        self.tokenValue = Value
        self.tokenType  = Type
        self.lineno = lineno

    @staticmethod
    def getTokenTypeList():
        #token type list
        TypeList = Enum.enum(
                        "FUNCTION",
                        "IF",
                        "ELSE",
                        "END",
                        "FOR",
                        "WHILE",
                        "ID",
                        "RETURN",
                        "NUM",
                        "POW",
                        "ASSIGN",
                        "EQ",
                        "UNEQ" ,
                        "LT",
                        "PLUS",
                        "MINUS",
                        "TRANSPOSE",
                        "TIMES",
                        "SEMI",
                        "LPAREN",
                        "RPAREN",
                        "LBRACKET",
                        "RBRACKET",
                        "GT",
                        "GE",
                        "LE",
                        "DIV",
                        "COL",
                        "COMMA",
                        "DOT",
                        "STRING",
                        "AND",
                        "OR",
                        "LOGICAND",
                        "LOGICOR",
                        "LOGICNOT",
                        "ERROR",
                        "ENDFILE")
        return TypeList

    @staticmethod
    def getReservedWord():
        TokenType = Token.getTokenTypeList()
        ReservedWord = {
                    'if': TokenType.IF,
                    'else': TokenType.ELSE,
                    'end': TokenType.END,
                    'function': TokenType.FUNCTION,
                    'for': TokenType.FOR,
                    'while':TokenType.WHILE,
                    'return':TokenType.RETURN
                }
        return ReservedWord

    def  setToken(self,Value,Type,lineno):
        self.tokenValue = Value
        self.tokenType  = Type
        self.lineno = lineno
        return self

