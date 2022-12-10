import sys
from TokenType import Token, TokenType
from Stmt import Stmt
from typing import List

"""
Brd syntactic grammar:

---------------------------------------------------------------
program -> statement* EOF
declaration -> varDecl | statement
varDecl -> "var" IDENTIFIER ( "=" expression )? ";"
statement ->    exprStmt | 
                forStmt  |
                ifStmt   | 
                printStmt| 
                whileStmt|
                block
forStmt -> "for" "(" ( varDecl | exprStatement | ";" )
            expression? ";"
            expression? ")" statement
whileStmt -> "while" "(" expression ")" statement
ifStmt -> "if" "(" expression ")" statement ( "else" statement )?
block -> "{" declaration* "}"
exprStmt -> expression ";"
printStmt -> "print" expression ";"
expression -> assignment
assignment -> IDENTIFIER "=" assignment | equality
logic_or -> logic_and ( "or" logic_and )*
logic_and -> equality ( "and" equality )*
equality -> comparison(("!="|"==") comparison)*
comparison -> term((">"|">="|"<"|"<=")term)*
term -> factor(("-"|"+")factor)*
factor -> unary(("/"|"*")unary)*
unary -> ("!"|"-") unary | call
call -> primary ( "(" arguments? ")" )*
arguments -> expression ( "," expression )*
primary -> NUMBER | STRING | IDENTIFIER | "true" | "false" | "nil" | "(" expression ")"
"""


class RunTimeError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
        super().__init__(self.message)


class Brd:
    def runtimeError(self, error: RunTimeError):
        self.hadRunTimeError = True
        print(error)

    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        self.hadError = True

    def error(self, line: int = 0, message: str = "", token: Token | None = None):
        if not token:
            self.report(line, "", message)
        else:
            if token.type == TokenType.EOF:
                self.report(token.line, " at end", message)
            else:
                self.report(token.line, f"at '{token.lexeme}' ", message)

    def run(self, source: str) -> None:
        from Parser import Parser
        from Scanner import Scanner
        from Interpreter import Interpreter

        tokens = Scanner(source, self).scanTokens()
        parser: Parser = Parser(tokens, self)
        statements: List[Stmt] = parser.parse()
        Interpreter(self).interpret(statements)

    def runPrompt(self):
        # TODO: prevent environment from being wiped out on each input
        while True:
            line = input("> ")
            if not line:
                break
            self.run(line)

    def runFile(self, path: str) -> None:
        with open(path, "r") as f:
            prog = f.read()
            self.run(prog)

    def __init__(self) -> None:
        self.hadError = False

        # don't run for tests
        if __name__ == "__main__":
            if len(sys.argv) > 2:
                raise Exception("Usage:Brd.py [script]")
            elif len(sys.argv) == 2:
                self.runFile(sys.argv[1])
            else:
                self.runPrompt()


if __name__ == "__main__":
    Brd()
