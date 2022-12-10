from Expr import Expr, Literal, Unary, Binary, Visitor, Grouping
from TokenType import Token, TokenType
from typing import List


class AstPrinter(Visitor):
    def print(self, expr):
        return expr.accept(self)

    def parenthesize(self, name: str, exprs: List[Expr]) -> str:
        ret = ""
        ret += f"({name}"
        for expr in exprs:
            ret += " "
            ret += expr.accept(self)
        ret += ")"
        return ret

    def visitBinaryExpr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, [expr.left, expr.right])

    def visitGroupingExpr(self, expr) -> str:
        return self.parenthesize("group", [expr.expression])

    def visitLiteralExpr(self, expr: Literal) -> str:
        return "nil" if not expr.value else str(expr.value)

    def visitUnaryExpr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, [expr.right])


if __name__ == "__main__":
    literal123: Literal = Literal(123)
    literal4567: Literal = Literal(45.67)

    MINUS: Token = Token(TokenType.MINUS, "-", None, 1)
    STAR: Token = Token(TokenType.STAR, "*", None, 1)

    unary: Unary = Unary(MINUS, literal123)
    grouping: Grouping = Grouping(literal4567)
    binary: Binary = Binary(unary, STAR, grouping)

    print(AstPrinter().print(binary))
