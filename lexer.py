
class Token:

    #enum type for python
    def enum(*sequential, **named):
        enums = dict(zip(sequential, range(len(sequential))), **named)
        reverse = dict((value, key) for key, value in enums.iteritems())
        enums['reverse_mapping'] = reverse
        return type('Enum', (), enums)

    def __init__(self, path):
        #state list
        self.State = self.enum(
                    "START",
                    "EQORASSIGN",       #equal or assign
                    "LTORLE",           #less than or less equal
                    "GTORGE" ,
                    "INUNEQ" ,
                    "INCOMMENT",
                    "INNUM",
                    "INPLUS",
                    "INMINUS",
                    "INID",
                    "INASSIGN",
                    "QUOTEORSTR",       #just single quote or begin of string
                    "DOTORNUM",         #just dot or a float number
                    "STRING",
                    "DONE")

        #token type list
        self.TokenType = self.enum(
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
                        "ERROR",
                        "ENDFILE")

        self.path = path        #self.source file
        self.pos = 0             #current self.position in current line
        self.curline = ""        #current line buffer
        self.currenToken = -1    #current self.TokenType
        self.curstate = -1       #current state
        self.tokenString = ""
        self.loadSource(self.path)

    def loadSource(self,filename):
        self.source = open(filename, 'r')

    def getNextChar(self):
        if self.pos >= len(self.curline):
            self.curline = self.source.readline()
            if not self.curline:
                return ""
            self.pos = 0
            self.pos += 1
            return self.curline[self.pos - 1]
        else:
            self.pos += 1
            return self.curline[self.pos - 1]

    def ungetNextChar(self):
        self.pos -= 1

    def lookbackChar(self):
        return self.curline[self.pos - 2]

    def getTokenType(self,c):
        token = {
                    #'=': self.TokenType.ASSIGN,
                    #'<': self.TokenType.LT,
                    #'>': self.TokenType.GT,
                    #"'": self.TokenType.SQUOTE
                    '.': self.TokenType.DOT,
                    ',': self.TokenType.COMMA,
                    '+': self.TokenType.PLUS,
                    '-': self.TokenType.MINUS,
                    '*': self.TokenType.TIMES,
                    '/': self.TokenType.DIV,
                    '(': self.TokenType.LPAREN,
                    ')': self.TokenType.RPAREN,
                    ';': self.TokenType.SEMI,
                    '[': self.TokenType.LBRACKET,
                    ']': self.TokenType.RBRACKET,
                    '^': self.TokenType.POW
                }
        if c in token.keys():
            return token[c]
        else:
            return self.TokenType.ERROR

    def state_START(self,c):
        self.save = True
        if c.isdigit():
            self.curstate = self.State.INNUM
        elif c.isalpha():
            self.curstate = self.State.INID
        #elif c == '=':
        #    self.curstate = self.State.INASSIGN
        elif c == ' ' or  c == '\t' or c == '\n' or c == '\r' :
            self.save = False
        elif c == "%":
            self.save = False
            self.curstate = self.State.INCOMMENT
        elif c == "!":
            self.save = True
            self.curstate = self.State.INUNEQ
        elif c == "=":
            self.save = True
            self.curstate = self.State.EQORASSIGN
        elif c == "<":
            self.save = True
            self.curstate = self.State.LTORLE
        elif c == ">":
            self.save = True
            self.curstate = self.State.GTORGE
        #elif c == "^":
        #    self.save = True
        #    self.curstate = self.State.POWER
        elif c == "'":
            self.save =True
            self.curstate = self.State.QUOTEORSTR
        elif c == "+":
            self.save = True
            self.curstate = self.State.INPLUS
        elif c == "-":
            self.save = True
            self.curstate = self.State.INMINUS
        else:
            self.curstate = self.State.DONE
            self.currentToken = self.getTokenType(c)

    def state_EQORASSIGN(self,c):
        if c == '=':
            self.currentToken = self.TokenType.EQ
        else:
            self.curstate = self.State.INASSIGN
            self.currentToken = self.TokenType.ASSIGN
            self.ungetNextChar();
        self.curstate = self.State.DONE

    def state_LTORLE(self,c):
        if c == '=':
            self.currentToken = self.TokenType.LE
        else:
            self.ungetNextChar()
            self.currentToken = self.TokenType.LT
        self.curstate = self.State.DONE

    def state_GTORGE(self,c):
        if c == '=':
            self.currentToken = self.TokenType.GE
        else:
            self.ungetNextChar()
            self.currentToken = self.TokenType.GT
        self.curstate = self.State.DONE

    def state_INUNEQ(self,c):
        if c == '=':
            self.currentToken = self.TokenType.UNEQ
        else:
            self.currentToken = self.TokenType.ERROR
            self.save = False
        self.curstate = self.State.DONE

    def state_INCOMMENT(self,c):
        self.save = False
        if c == '\r' or c == '\n':
            self.curstate = self.State.START

    def state_INNUM(self,c):
        if not c.isdigit() and c != '.' and c != 'e' and c != '+' and c != '-':
            self.ungetNextChar()
            self.save = False
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.NUM

    def state_INID(self,c):
        if (not c.isalpha()) and (not c.isdigit()) and (c != '_'):
            self.ungetNextChar()
            self.save = False
            self.currentToken = self.TokenType.ID
            self.curstate = self.State.DONE

    def state_INPLUS(self,c):
        i = 3 ;
        LastNonEmptyChar = self.curline[self.pos - i]   # last non-empty character before plus

        while LastNonEmptyChar == ' ':
            i += 1
            LastNonEmptyChar =  self.curline[self.pos - i]

        if not c.isdigit() or LastNonEmptyChar.isalpha() or LastNonEmptyChar.isdigit() or ( LastNonEmptyChar == "_"):
            self.ungetNextChar()
            self.save = False
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.PLUS
        else:
            self.save = True
            self.curstate = self.State.INNUM

    def state_INMINUS(self,c):
        i = 3 ;
        LastNonEmptyChar = self.curline[self.pos - i]   # last non-empty character before plus

        while LastNonEmptyChar == ' ':
            i += 1
            LastNonEmptyChar =  self.curline[self.pos - i]

        if not c.isdigit() or LastNonEmptyChar.isalpha() or LastNonEmptyChar.isdigit() or ( LastNonEmptyChar == "_"):
            self.ungetNextChar()
            self.save = False
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.MINUS
        else:
            self.save = True
            self.curstate = self.State.INNUM


    #def state_POWER(self,c):
    #    if c.isdigit():
    #        self.currentToken = self.TokenType.POWNUM
    #        self.save = True
    #    else:
    #        self.ungetNextChar()
    #        self.currentToken = self.TokenType.ERROR
    #        self.save = False
    #    self.curstate = self.State.DONE

    def state_QUOTEORSTR(self,c):
        self.ungetNextChar()
        lookback = self.lookbackChar()
        if lookback.isalpha():
            self.currentToken = self.TokenType.TRANSPOSE
            self.save = False
            self.curstate = self.State.DONE
        else:
            self.save = False
            self.curstate = self.State.STRING

    def state_STRING(self,c):
        if c == "'":
            self.save = False
            self.curstate = self.State.DONE
            self.currentToken = self.TokenType.STRING
        else:
            self.save = True

    def getToken(self):
        self.tokenStringIndex = 0
        self.tokenString = ''
        self.curstate = self.State.START

        while (self.curstate != self.State.DONE):
            c = self.getNextChar()
            if not c :
                self.curstate = self.State.DONE
                self.save = False
                self.currentToken = self.TokenType.ENDFILE
                self.tokenString = ""
                break
            self.save = True

            stateMachine = {
                            self.State.START: lambda x: self.state_START(x),
                            self.State.INCOMMENT: lambda x: self.state_INCOMMENT(x),
                            self.State.EQORASSIGN: lambda x: self.state_EQORASSIGN(x),
                            self.State.LTORLE: lambda x: self.state_LTORLE(x),
                            self.State.GTORGE: lambda x: self.state_GTORGE(x),
                            self.State.INUNEQ: lambda x: self.state_INUNEQ(x),
                            self.State.INNUM: lambda x: self.state_INNUM(x),
                            self.State.INID: lambda x: self.state_INID(x),
                            self.State.QUOTEORSTR: lambda x: self.state_QUOTEORSTR(x),
                            self.State.STRING: lambda x: self.state_STRING(x),
                            self.State.INPLUS: lambda x: self.state_INPLUS(x),
                            self.State.INMINUS: lambda x: self.state_INMINUS(x),
                            #self.State.POWER: lambda x: self.state_POWER(x),
            }[self.curstate](c)
            if self.save :
                self.tokenString += c;

        if self.curstate == self.State.DONE:
            #self.tokenString += '\0'
            #print self.tokenString
            return (self.tokenString, self.TokenType.reverse_mapping[self.currentToken])
