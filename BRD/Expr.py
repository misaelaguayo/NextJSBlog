# Automatically generated using tool/GeneratedAst.py
# ['Assign-name: Token,value: Expr', 'Binary- left: Expr,operator: Token,right: Expr', 'Call- callee: Expr,paren: Token,arguments: List[Expr]', 'Grouping- expression: Expr', 'Literal- value: object', 'Logical- left: Expr,operator: Token,right: Expr', 'Unary- operator: Token,right: Expr', 'Variable-name: Token']

from TokenType import *
from abc import ABC, abstractmethod
from typing import List


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor):
        ...


class Visitor(ABC):
    @abstractmethod
    def visitAssignExpr(self, expr):
        ...

    @abstractmethod
    def visitBinaryExpr(self, expr):
        ...

    @abstractmethod
    def visitCallExpr(self, expr):
        ...

    @abstractmethod
    def visitGroupingExpr(self, expr):
        ...

    @abstractmethod
    def visitLiteralExpr(self, expr):
        ...

    @abstractmethod
    def visitLogicalExpr(self, expr):
        ...

    @abstractmethod
    def visitUnaryExpr(self, expr):
        ...

    @abstractmethod
    def visitVariableExpr(self, expr):
        ...


class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visitAssignExpr(self)


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)


class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: List[Expr]):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visitCallExpr(self)


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)


class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)


class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitLogicalExpr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)


class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor):
        return visitor.visitVariableExpr(self)
