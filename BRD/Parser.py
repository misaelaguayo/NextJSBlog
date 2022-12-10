from typing import List
from TokenType import Token, TokenType
from Expr import Call, Expr, Binary, Logical, Unary, Literal, Grouping, Variable, Assign
from Stmt import Block, Stmt, Print, Expression, Var, If, While
from Brd import Brd


class ParseError(Exception):
    def __init__(self, token: Token, message: str, brd: Brd):
        self.token = token
        self.message = message
        brd.error(token=token, message=message)


class Parser:
    def __init__(self, tokens: List[Token], brd: Brd):
        self.tokens: List[Token] = tokens
        self.current: int = 0
        self.brdSingleton = brd

    def expressionStatement(self) -> Stmt:
        expr: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)

    def forStatement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        initializer: Stmt
        if self.match([TokenType.SEMICOLON]):
            initializer = None
        elif self.match([TokenType.VAR]):
            initializer = self.varDeclaration()
        else:
            initializer = self.expressionStatement()

        condition: Expr = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment: Expr = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body: Stmt = self.statement()

        if increment != None:
            body = Block([body, Expression(increment)])

        if condition == None:
            condition = Literal(True)
        body = While(condition, body)

        if initializer != None:
            body = Block([initializer, body])

        return body

    def ifStatement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after if.")
        condition: Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        thenBranch: Stmt = self.statement()
        elseBranch: Stmt | None = None
        if self.match([TokenType.ELSE]):
            elseBranch = self.statement()
        return If(condition, thenBranch, elseBranch)

    def whileStatement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition: Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body: Stmt = self.statement()

        return While(condition, body)

    def printStatement(self) -> Stmt:
        value: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def block(self) -> List[Stmt]:
        statements: List[Stmt] = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def statement(self) -> Stmt:
        if self.match([TokenType.FOR]):
            return self.forStatement()
        if self.match([TokenType.IF]):
            return self.ifStatement()
        if self.match([TokenType.PRINT]):
            return self.printStatement()
        if self.match([TokenType.WHILE]):
            return self.whileStatement()
        if self.match([TokenType.LEFT_BRACE]):
            return Block(self.block())
        return self.expressionStatement()

    def varDeclaration(self) -> Stmt | None:
        name: Token = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None

        if self.match([TokenType.EQUAL]):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        if initializer:
            return Var(name, initializer)
        return None

    def declaration(self) -> Stmt | None:
        try:
            if self.match([TokenType.VAR]):
                return self.varDeclaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def parse(self) -> List[Stmt]:
        statements: List[Stmt] = []
        while not self.isAtEnd():
            dec = self.declaration()
            if dec:
                statements.append(dec)
        return statements

    def synchronize(self) -> None:
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return
            match self.peek().type:
                case TokenType.CLASS | TokenType.FOR | TokenType.FUN | TokenType.IF | TokenType.PRINT | TokenType.RETURN | TokenType.VAR | TokenType.WHILE:
                    return
            self.advance()

    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        raise ParseError(self.peek(), message, self.brdSingleton)

    def finishCall(self, callee: Expr) -> Expr:
        arguments: List[Expr] = []
        if not self.check(TokenType.RIGHT_PAREN):
            # do while implemented in python
            while True:
                if len(arguments) >= 255:
                    self.brdSingleton.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
                if not self.match([TokenType.COMMA]):
                    break
        paren: Token = self.consume(
            TokenType.RIGHT_PAREN, "Expect ')' after arguments."
        )
        return Call(callee, paren, arguments)

    def call(self) -> Expr:
        expr: Expr = self.primary()
        while True:
            if self.match([TokenType.LEFT_PAREN]):
                expr = self.finishCall(expr)
            else:
                break
        return expr

    def primary(self) -> Expr:
        if self.match([TokenType.FALSE]):
            return Literal(TokenType.FALSE)
        if self.match([TokenType.TRUE]):
            return Literal(TokenType.TRUE)
        if self.match([TokenType.NIL]):
            return Literal(None)
        if self.match([TokenType.NUMBER, TokenType.STRING]):
            return Literal(self.previous().literal)
        if self.match([TokenType.IDENTIFIER]):
            return Variable(self.previous())
        if self.match([TokenType.LEFT_PAREN]):
            expr: Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        else:
            raise ParseError(self.peek(), "Expect expression.", self.brdSingleton)

    def unary(self) -> Expr:
        if self.match([TokenType.BANG, TokenType.MINUS]):
            operator: Token = self.previous()
            right: Expr = self.unary()
            return Unary(operator, right)
        return self.call()

    def factor(self) -> Expr:
        expr: Expr = self.unary()

        while self.match([TokenType.SLASH, TokenType.STAR]):
            operator: Token = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr: Expr = self.factor()
        while self.match([TokenType.MINUS, TokenType.PLUS]):
            operator: Token = self.previous()
            right: Expr = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr: Expr = self.term()
        while self.match(
            [
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
            ]
        ):
            operator: Token = self.previous()
            right: Expr = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def previous(self):
        return self.tokens[self.current - 1]

    def peek(self) -> Token:
        return self.tokens[self.current]

    def isAtEnd(self):
        return self.peek().type == TokenType.EOF

    def advance(self) -> Token:
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def check(self, type: TokenType) -> bool:
        if self.isAtEnd():
            return False
        return self.peek().type == type

    def match(self, types: List[TokenType]) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def equality(self) -> Expr:
        expr: Expr = self.comparison()
        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def _and(self) -> Expr:
        expr: Expr = self.equality()
        while self.match([TokenType.AND]):
            operator: Token = self.previous()
            right: Expr = self.equality()
            expr = Logical(expr, operator, right)
        return expr

    def _or(self) -> Expr:
        expr: Expr = self._and()
        while self.match([TokenType.OR]):
            operator: Token = self.previous()
            right: Expr = self._and()
            expr = Logical(expr, operator, right)
        return expr

    def assignment(self) -> Expr:
        expr: Expr = self._or()
        if self.match([TokenType.EQUAL]):
            equals: Token = self.previous()
            value: Expr = self.assignment()
            if isinstance(expr, Variable):
                name: Token = expr.name
                return Assign(name, value)
            self.brdSingleton.error(token=equals, message="Invalid assignment target.")
        return expr

    def expression(self) -> Expr:
        return self.assignment()
