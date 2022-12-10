from TokenType import *
from typing import List
from Brd import Brd


class Scanner:
    def __init__(self, source: str, brd: Brd):
        self.tokens = []
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }
        self.brdSingleton = brd

    def addToken(self, _type: TokenType, literal: object = None) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(_type, text, literal, self.line))

    def isAtEnd(self):
        return self.current >= len(self.source)

    @staticmethod
    def isDigit(c: str) -> bool:
        return c >= "0" and c <= "9"

    @staticmethod
    def isAlpha(c: str) -> bool:
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    @staticmethod
    def isAlphaNumeric(c: str) -> bool:
        return Scanner.isAlpha(c) or Scanner.isDigit(c)

    def identifier(self) -> None:
        while Scanner.isAlphaNumeric(self.peek()):
            self.advance()
        text: str = self.source[self.start : self.current]
        if text in self.keywords:
            type: TokenType = self.keywords[text]
        else:
            type = TokenType.IDENTIFIER
        self.addToken(type)

    def number(self) -> None:
        while Scanner.isDigit(self.peek()):
            self.advance()
        if self.peek() == "." and Scanner.isDigit(self.peekNext()):
            # consume the "."
            self.advance()
            while Scanner.isDigit(self.peek()):
                self.advance()
        self.addToken(TokenType.NUMBER, int(self.source[self.start : self.current]))

    def string(self) -> None:
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.isAtEnd():
            self.brdSingleton.error(self.line, "Unterminated string")
            return
        self.advance()
        value: str = self.source[self.start + 1 : self.current - 1]
        self.addToken(TokenType.STRING, value)

    def match(self, expected: str) -> bool:
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.isAtEnd():
            return "\0"
        return self.source[self.current]

    def peekNext(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current]

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def scanToken(self) -> None:
        c = self.advance()
        match c:
            case "(":
                self.addToken(TokenType.LEFT_PAREN)
            case ")":
                self.addToken(TokenType.RIGHT_PAREN)
            case "{":
                self.addToken(TokenType.LEFT_BRACE)
            case "}":
                self.addToken(TokenType.RIGHT_BRACE)
            case ",":
                self.addToken(TokenType.COMMA)
            case ".":
                self.addToken(TokenType.DOT)
            case "-":
                self.addToken(TokenType.MINUS)
            case "+":
                self.addToken(TokenType.PLUS)
            case ";":
                self.addToken(TokenType.SEMICOLON)
            case "*":
                self.addToken(TokenType.STAR)

            # Two-char tokens
            case "!":
                self.addToken(
                    TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                )
            case "=":
                self.addToken(
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case "<":
                self.addToken(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                )
            case ">":
                self.addToken(
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
            # comments
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.isAtEnd():
                        self.advance()
                elif self.match("*"):
                    while (
                        self.peek() != "*"
                        and self.peekNext() != "/"
                        and not self.isAtEnd()
                    ):
                        if self.peek() == "\n":
                            self.line += 1
                        self.advance()
                else:
                    self.addToken(TokenType.SLASH)
            # whitespace
            case " " | "\r" | "\t":
                ...
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case _:
                if Scanner.isDigit(c):
                    self.number()
                elif Scanner.isAlpha(c):
                    self.identifier()
                else:
                    self.brdSingleton.error(self.line, "Unexpected character.")

    def scanTokens(self) -> List[Token]:
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        # we've finished scanning. Append an EOF token
        self.tokens.append(Token(TokenType.EOF, "", {}, self.line))
        return self.tokens
