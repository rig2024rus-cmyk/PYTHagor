"""Парсер PYTHagor. Фаза 1.4.

Рекурсивный спуск с приоритетами операций,
от низшего к высшему: или, и, сравнения, + и -, *, унарные - и не, первичные.
Программа - последовательность операторов, разделённых переносами строк:
объявлений (имя : тип = значение), присваиваний (имя = значение),
выражений, условий (если условие: ... иначе: ... конец) и пропусков.
"""

from __future__ import annotations

from pythagor.nucleus.ast import (
    Atomos,
    Cosmos,
    Expr,
    Harmonia,
    Horos,
    Kenosis,
    Krisis,
    Onoma,
    Thesis,
    Tropos,
)
from pythagor.nucleus.lexer import Lexer, Token, TokenType
from pythagor.nucleus.types import Arithmos, Dilemma
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

TYPE_NAMES = {"Целое": Arithmos, "Булево": Dilemma}


class Parser:
    """Парсер: превращает поток токенов в Cosmos."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def _current(self) -> Token:
        return self.tokens[self.pos]

    def _peek_type(self) -> TokenType:
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1].typ
        return TokenType.EOF

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

    def _skip_newlines(self) -> None:
        while self._current().typ == TokenType.NEWLINE:
            self._advance()

    def parse(self) -> Cosmos:
        statements: list = []
        self._skip_newlines()
        while self._current().typ != TokenType.EOF:
            statements.append(self.parse_statement())
            if self._current().typ == TokenType.NEWLINE:
                self._advance()
                self._skip_newlines()
            elif self._current().typ == TokenType.EOF:
                break
            else:
                token = self._current()
                raise ParserError(
                    "ожидался перенос строки или конец программы",
                    token.line,
                    token.column,
                )
        if not statements:
            token = self._current()
            raise ParserError("пустая программа", token.line, token.column)
        return Cosmos(tuple(statements))

    def parse_statement(self):
        """Оператор: условие, пропуск, объявление, присваивание или выражение."""
        if self._current().typ == TokenType.IF:
            return self.parse_krisis()
        if self._current().typ == TokenType.PASS:
            self._advance()
            return Kenosis()
        if self._current().typ == TokenType.ID:
            if self._peek_type() == TokenType.COLON:
                return self.parse_declaration()
            if self._peek_type() == TokenType.ASSIGN:
                return self.parse_assignment()
        return self.parse_or()

    def parse_declaration(self) -> Horos:
        """Объявление: имя : тип = значение."""
        name_token = self._advance()
        self._expect(TokenType.COLON, "двоеточие :")
        type_token = self._expect(TokenType.ID, "имя типа")
        if type_token.value not in TYPE_NAMES:
            raise ParserError(
                f"неизвестный тип {type_token.value!r}",
                type_token.line,
                type_token.column,
            )
        self._expect(TokenType.ASSIGN, "знак присваивания =")
        value = self.parse_or()
        return Horos(name_token.value, TYPE_NAMES[type_token.value](), value)

    def parse_assignment(self) -> Thesis:
        """Присваивание: имя = значение."""
        name_token = self._advance()
        self._expect(TokenType.ASSIGN, "знак присваивания =")
        value = self.parse_or()
        return Thesis(name_token.value, value)

    def parse_statement_block(self, terminators) -> tuple:
        """Последовательность операторов до токена-терминатора."""
        statements = []
        self._skip_newlines()
        while (
            self._current().typ not in terminators
            and self._current().typ != TokenType.EOF
        ):
            statements.append(self.parse_statement())
            if self._current().typ == TokenType.NEWLINE:
                self._advance()
                self._skip_newlines()
            elif (
                self._current().typ in terminators
                or self._current().typ == TokenType.EOF
            ):
                break
            else:
                token = self._current()
                raise ParserError(
                    "ожидался перенос строки или конец блока",
                    token.line,
                    token.column,
                )
        if not statements:
            token = self._current()
            raise ParserError(
                "пустой блок: ожидался оператор или 'пропуск'",
                token.line,
                token.column,
            )
        return tuple(statements)

    def parse_krisis(self) -> Krisis:
        """Условие: если условие: блок [иначе: блок] конец."""
        self._expect(TokenType.IF, "ключевое слово 'если'")
        condition = self.parse_or()
        self._expect(TokenType.COLON, "двоеточие : после условия")
        then_branch = self.parse_statement_block({TokenType.ELSE, TokenType.END})
        else_branch = None
        if self._current().typ == TokenType.ELSE:
            self._advance()
            self._expect(TokenType.COLON, "двоеточие : после 'иначе'")
            else_branch = self.parse_statement_block({TokenType.END})
        self._expect(TokenType.END, "'конец', закрывающее блок")
        return Krisis(condition, then_branch, else_branch)

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
        if token.typ == TokenType.ID:
            self._advance()
            return Onoma(token.value)
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
