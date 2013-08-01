#!/usr/bin/python
# -*- coding: utf-8 -*- 

from enum import *

class Token:
    def __init__(self,Value = None,Type = ""):
        self.tokenValue = Value
        self.tokenType  = Type

    @staticmethod
    def getTokenTypeList():
        #token type list
        TypeList = Enum.enum(
                        "FUNCTION",
                        "IF",
                        "ELSE",
                        "END",
                        "FOR",
                        "ID",
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
                        "ERROR",
                        "ENDFILE")
        return TypeList


    def  setToken(self,Value,Type):
        self.tokenValue = Value
        self.tokenType  = Type
        return self

    
