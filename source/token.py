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
                        "ELSEIF",
                        "END",
                        "FOR",
                        "WHILE",
                        "ID",
                        "RETURN",
                        "BREAK",
                        "CONTINUE",
                        "NARGIN",
                        "VARARGIN",
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
                        "LBRACE",
                        "RBRACE",
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
                        "DOTRDIV",
                        "DOTLDIV",
                        "DOTTIMES",
                        "DOTPOW",
                        "DOTTRANSPOSE",
                        "ERROR",
                        "ENDFILE")
        return TypeList

    @staticmethod
    def getReservedWord():
        TokenType = Token.getTokenTypeList()
        ReservedWord = {
                    'if': TokenType.IF,
                    'else': TokenType.ELSE,
                    'elseif': TokenType.ELSEIF,
                    'end': TokenType.END,
                    'function': TokenType.FUNCTION,
                    'for': TokenType.FOR,
                    'while':TokenType.WHILE,
                    'return':TokenType.RETURN,
                    'break' : TokenType.BREAK,
                    'continue': TokenType.CONTINUE,
                    'varargin': TokenType.VARARGIN,
                    'nargin': TokenType.NARGIN
                }
        return ReservedWord

    def  setToken(self,Value,Type,lineno):
        self.tokenValue = Value
        self.tokenType  = Type
        self.lineno = lineno
        return self

