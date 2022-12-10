from Environment import Environment
from Expr import (
    Logical,
    Variable,
    Visitor as ExprVisitor,
    Literal,
    Grouping,
    Expr,
    Unary,
    Binary,
    Assign,
)
from Stmt import (
    Block,
    If,
    Var,
    Visitor as StmtVisitor,
    Expression,
    Print,
    Stmt,
    While,
)
from TokenType import TokenType, Token
from Brd import RunTimeError, Brd
from typing import List


class Interpreter(ExprVisitor, StmtVisitor):  # type: ignore (pyright confused by two visitor classes)
    def __init__(self, brd: Brd):
        self.brdSingleton = brd
        self.environment: Environment = Environment()

    @staticmethod
    def stringify(object: object) -> str:
        if not object:
            return "nil"
        if isinstance(object, float):
            text: str = str(object)
            if text[-2:] == ".0":
                text = text[0:-2]
            return text
        return str(object)

    def checkNumberOperands(self, operator: Token, left: object, right: object) -> None:
        if (isinstance(left, float) or isinstance(left, int)) and (
            isinstance(right, float) or isinstance(right, int)
        ):
            return
        raise RunTimeError(operator, "Operands must be numbers")

    def checkNumberOperand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, float) or isinstance(operand, int):
            return
        raise RunTimeError(operator, "Operand must be a number")

    def isTruthy(self, object: object) -> bool:
        if not object:
            return False
        if isinstance(object, bool):
            return bool(object)
        return True

    @staticmethod
    def isEqual(a: object, b: object):
        if not a and not b:
            return True
        if not a:
            return False
        return a == b

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def executeBlock(self, statements: List[Stmt], environment: Environment):
        previous: Environment = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    # stmt visitors starts #
    def visitWhileStmt(self, stmt: While) -> None:
        while self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visitLogicalExpr(self, expr: Logical):
        left: object = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self.isTruthy(left):
                return left
        else:
            if not self.isTruthy(left):
                return left
        return self.evaluate(expr.right)

    def visitIfStmt(self, stmt: If) -> None:
        if self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch:
            self.execute(stmt.elseBranch)
        return None

    def visitBlockStmt(self, stmt: Block) -> None:
        self.executeBlock(stmt.statements, Environment(self.environment))
        return None

    def visitExpressionStmt(self, stmt: Expression) -> None:
        self.evaluate(stmt.expression)
        return None

    def visitPrintStmt(self, stmt: Print) -> None:
        value: object = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visitVarStmt(self, stmt: Var) -> None:
        value: object = None
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None

    def visitVariableExpr(self, expr: Variable):
        return self.environment.get(expr.name)

    # stmt visitors ends

    # expr visitors starts
    def visitCallExpr(self, expr: Expr):
        # callee: object = self.evaluate(expr.callee)
        # arguments: List[object] = []
        # for argument in arguments:
        #     arguments.append(self.evaluate(argument))

        # function: BrdCallable = callee
        # return function.call(self, arguments)
        raise NotImplementedError("Not yet implemented")

    def visitAssignExpr(self, expr: Assign):
        value: object = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    @staticmethod
    def visitLiteralExpr(expr: Literal) -> object:
        return expr.value

    def visitGroupingExpr(self, expr: Grouping) -> object:
        return self.evaluate(expr.expression)

    def visitUnaryExpr(self, expr: Unary) -> object:
        right: object = self.evaluate(expr.right)
        assert right is not None, "right somehow none"

        match expr.operator.type:
            case TokenType.BANG:
                return not self.isTruthy(right)
            case TokenType.MINUS:
                self.checkNumberOperand(expr.operator, right)
                return -float(right)
        return None

    def visitBinaryExpr(self, expr: Binary) -> object:
        left: object = self.evaluate(expr.left)
        right: object = self.evaluate(expr.right)

        assert left is not None and right is not None, "left or right are somehow none"

        match expr.operator.type:
            case TokenType.MINUS:
                self.checkNumberOperand(expr.operator, right)
                return float(left) - float(right)
            case TokenType.SLASH:
                self.checkNumberOperands(expr.operator, left, right)
                if not float(right):
                    raise RunTimeError(expr.operator, "Division by zero error")
                return float(left) / float(right)
            case TokenType.STAR:
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.PLUS:
                if (isinstance(left, float) or isinstance(left, int)) and (
                    isinstance(right, float) or isinstance(right, int)
                ):
                    return float(left) + float(right)
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                raise RunTimeError(
                    expr.operator, "Operands must be two numbers or two strings"
                )
            case TokenType.GREATER:
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.checkNumberOperands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return not self.isEqual(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.isEqual(left, right)
        return None

    # expr visitor ends

    def execute(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def interpret(self, statements: List[Stmt]) -> None:
        try:
            for statement in statements:
                self.execute(statement)
        except RunTimeError as e:
            self.brdSingleton.runtimeError(e)
