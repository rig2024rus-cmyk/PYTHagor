"""Парсер PYTHagor. Фаза 1.2.

Рекурсивный спуск с приоритетами операций,
от низшего к высшему: или, и, сравнения, + и -, *, унарные - и не, первичные.
"""

from __future__ import annotations

from pythagor.nucleus.ast import Atomos, Cosmos, Expr, Harmonia, Tropos
from pythagor.nucleus.lexer import Lexer, Token, TokenType
from pythagor.nucleus.types import Arithmos
from pythagor.nucleus.values import Monada


class ParserError(SyntaxError):
    """Ошибка разбора с позицией."""

    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(f"строка {line}, колонка {column}: {message}")
        self.line = line
        self.column = column


COMPARISON_TOKENS = {
    TokenType.LT: "<",
    TokenType.GT: ">",
    TokenType.LE: "<=",
    TokenType.GE: ">=",
    TokenType.EQ: "==",
    TokenType.NE: "!=",
}

ADDITIVE_TOKENS = {TokenType.PLUS: "+", TokenType.MINUS: "-"}


class Parser:
    """Парсер: превращает поток токенов в Cosmos."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def _current(self) -> Token:
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        token = self.tokens[self.pos]
        if token.typ != TokenType.EOF:
            self.pos += 1
        return token

    def _expect(self, typ: TokenType, what: str) -> Token:
        token = self._current()
        if token.typ != typ:
            raise ParserError(f"ожидалось {what}", token.line, token.column)
        return self._advance()

    def parse(self) -> Cosmos:
        expr = self.parse_or()
        self._expect(TokenType.EOF, "конец выражения")
        return Cosmos(expr)

    def parse_or(self) -> Expr:
        left = self.parse_and()
        while self._current().typ == TokenType.OR:
            self._advance()
            left = Harmonia(left, "или", self.parse_and())
        return left

    def parse_and(self) -> Expr:
        left = self.parse_comparison()
        while self._current().typ == TokenType.AND:
            self._advance()
            left = Harmonia(left, "и", self.parse_comparison())
        return left

    def parse_comparison(self) -> Expr:
        left = self.parse_additive()
        while self._current().typ in COMPARISON_TOKENS:
            op = COMPARISON_TOKENS[self._advance().typ]
            left = Harmonia(left, op, self.parse_additive())
        return left

    def parse_additive(self) -> Expr:
        left = self.parse_multiplicative()
        while self._current().typ in ADDITIVE_TOKENS:
            op = ADDITIVE_TOKENS[self._advance().typ]
            left = Harmonia(left, op, self.parse_multiplicative())
        return left

    def parse_multiplicative(self) -> Expr:
        left = self.parse_unary()
        while self._current().typ == TokenType.MUL:
            self._advance()
            left = Harmonia(left, "*", self.parse_unary())
        return left

    def parse_unary(self) -> Expr:
        token = self._current()
        if token.typ == TokenType.MINUS:
            self._advance()
            return Tropos("-", self.parse_unary())
        if token.typ == TokenType.NOT:
            self._advance()
            return Tropos("не", self.parse_unary())
        return self.parse_primary()

    def parse_primary(self) -> Expr:
        token = self._current()
        if token.typ == TokenType.NUMBER:
            self._advance()
            return Atomos(Monada(int(token.value)), Arithmos())
        if token.typ == TokenType.LEFT_PAREN:
            self._advance()
            expr = self.parse_or()
            self._expect(TokenType.RIGHT_PAREN, "закрывающая скобка )")
            return expr
        raise ParserError(
            f"неожиданный токен {token.value!r}", token.line, token.column
        )


def parse(text: str) -> Cosmos:
    """Разбирает текст в Cosmos: лексер, затем парсер."""
    return Parser(Lexer(text).tokenize()).parse()
