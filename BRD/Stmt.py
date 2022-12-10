# Automatically generated using tool/GeneratedAst.py
# ['Block- statements: List[Stmt]', 'Expression- expression: Expr', 'If- condition: Expr,thenBranch: Stmt,elseBranch: Stmt|None', 'Print- expression: Expr', 'While- condition: Expr,body: Stmt', 'Var- name: Token,initializer: Expr']

from Expr import *
from TokenType import *
from abc import ABC, abstractmethod
from typing import List


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor):
        ...


class Visitor(ABC):
    @abstractmethod
    def visitBlockStmt(self, stmt):
        ...

    @abstractmethod
    def visitExpressionStmt(self, stmt):
        ...

    @abstractmethod
    def visitIfStmt(self, stmt):
        ...

    @abstractmethod
    def visitPrintStmt(self, stmt):
        ...

    @abstractmethod
    def visitWhileStmt(self, stmt):
        ...

    @abstractmethod
    def visitVarStmt(self, stmt):
        ...


class Block(Stmt):
    def __init__(self, statements: List[Stmt]):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visitBlockStmt(self)


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)


class If(Stmt):
    def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt | None):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def accept(self, visitor):
        return visitor.visitIfStmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitPrintStmt(self)


class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visitWhileStmt(self)


class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visitVarStmt(self)
