import os
import sys

#enum type for python
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

#state list
State = enum("START", "INASSIGN", "EQORASSIGN", "INEQ" ,"INLE" ,
            "LTORLE", "INLT" ,"INLE","GTORGE" ,"INGT" ,"INGE",
            "INUNEQ" , "INCOMMENT", "INNUM", "INID", "DONE")
#token type list
TokenType = enum("FUNCTION", "IF", "ELSE", "END", "FOR",
                "ID", "NUM",
                "ASSIGN", "EQ","UNEQ" ,"LT", "PLUS", "MINUS",
                "TIMES", "SEMI", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET",
                "GE", "LE", "DIV", "COL", "COMMA", "DOT","SQUOTE"  ,"ERROR")

source =""          #source file
pos = 0             #current position in current line
curline = ""        #current line buffer
currenToken = -1    #current TokenType
curstate = -1       #current state

def loadSource(filename):
    source = open(filename, 'r')

def getNextChar():
    if pos >= len(curline):
        curline = source.readline()
        pos = 0
        return curline[pos++]
    else: return curline[pos++]

def ungetNextChar():
    pos --

def getTokenType(c)
    token = {
                #'=': TokenType.ASSIGN,
                #'<': TokenType.LT,
                #'>': TokenType.GT,
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.TIME,
                '/': TokenType.DIV,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                ';': TokenType.SEMI,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ',': TokenType.COMMA,
                '.': TokenType.DOT,
                "'": TokenType.SQUOTE
            }
    if c in token.keys():
        return result[c]
    else:
        return TokenType.ERROR

def state_START(c):
    save = True
    if c.isdigit():
        curstate = State.INNUM
    elif c.isalpha():
        curstate = State.INID
    #elif c == '=':
    #    curstate = State.INASSIGN
    elif c == ' ' || c == '\t' || c == '\n' || c == '\r' :
        save = False
    elif c == "%":
        save = False
        curstate = State.INCOMMENT
    elif c == "!":
        save = True
        curstate = State.INUNEQ
    elif c == "=":
        save = True
        curstate = State.EQORASSIGN
    elif c == "<":
        save = True
        curstate = State.LTORLE
    elif c == ">":
        save = True
        curstate = State.GTORGE
    else:
        curstate = State.DONE
        currentToken = getTokenType(c)

def state_EQORASSIGN(c):
    if c == '='
        currentToken = TokenType.EQ
    else:
        curstate = State.INASSIGN
        ungetNextChar();
    curstate = State.DONE

def state_LTORLE(c):
    if c == '=':
        currentToken = TokenType.LE
    else:
        ungetNextChar()
        currentToken = TokenType.LT
    curstate = State.DONE

def state_GTORGE(c):
    if c == '=':
        currentToken = TokenType.GE
    else:
        ungetNextChar()
        currentToken = TokenType.GT
    curstate = State.DONE

def state_INUNEQ(c):
    if c == '=':
        currentToken = TokenType.UNEQ
    else:
        currentToken = TokenType.ERROR
        save = False
    curstate = State.DONE

def state_INCOMMENT(c):
    save = False
    if c == '\r' || c == '\n':
        curstate = State.START

def state_INNUM(c):
    if !c.isdigit():
        ungetNextChar()
        save = False
        curstate = State.DONE
        currentToken = TokenType.NUM

def state_INID(c):
    if !c.isalpha():
        ungetNextChar()
        sava = False
        currentToken = TokenType.ID

def getToken():
    tokenStringIndex = 0
    curstate = State.START

    while (curState != State.DONE):
        c = getNextChar()
        save = True

        stateMachine = {
                        State.START: lambda x: state_START(x),
                        State.INCOMMENT: lambda x: state_INCOMMENT(x),
                        State.EQORASSIGN: lambda x: state_EQORASSIGN(x),
                        State.LTORLE: lambda x: state_LTORLE(x),
                        State.GTORGE: lambda x: state_GTORGE(x),
                        State.INUNEQ: lambda x: state_INUNEQ(x),
                        State.INNUM: lambda x: state_INNUM(x),
                        State.INID: lambda x: state_INID(x)
        }[curstate](c)
