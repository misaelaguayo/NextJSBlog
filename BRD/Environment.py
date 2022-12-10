from typing import Dict
from TokenType import Token
from Brd import RunTimeError


class Environment:
    def __init__(self, enclosing=None):
        self.values: Dict[str, object] = {}
        self.enclosing: Environment = enclosing

    def get(self, name: Token) -> object:
        # return value of variable
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)
        raise RuntimeError(name, f"Undefined variable {name.lexeme}.")

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing:
            return self.enclosing.assign(name, value)
        raise RunTimeError(name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name: str, value: object) -> None:
        # define a variable, allows for redefinition
        self.values[name] = value
