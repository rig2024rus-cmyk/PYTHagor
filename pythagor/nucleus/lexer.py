"""Лексер PYTHagor. Фаза 1.3.

Токенизация текста на числа, операторы, скобки, имена, двоеточие, присваивание,
переносы строк. Отслеживание позиций для сообщений об ошибках.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()
    ID = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    EQ = auto()
    NE = auto()
    ASSIGN = auto()
    COLON = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    IF = auto()
    ELSE = auto()
    END = auto()
    PASS = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    NEWLINE = auto()
    ФУНКЦИЯ = auto()
    ВЕРНУТЬ = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    typ: TokenType
    value: str
    line: int
    column: int


KEYWORDS = {
    "и": TokenType.AND,
    "или": TokenType.OR,
    "не": TokenType.NOT,
    "функция": TokenType.ФУНКЦИЯ,
    "вернуть": TokenType.ВЕРНУТЬ,
    "если": TokenType.IF,
    "иначе": TokenType.ELSE,
    "конец": TokenType.END,
    "пропуск": TokenType.PASS,
}

SINGLE_CHAR_OPS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MUL,
    "<": TokenType.LT,
    ">": TokenType.GT,
    "=": TokenType.ASSIGN,
    ":": TokenType.COLON,
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
}

TWO_CHAR_OPS = {
    "<=": TokenType.LE,
    ">=": TokenType.GE,
    "==": TokenType.EQ,
    "!=": TokenType.NE,
}


class LexerError(SyntaxError):
    """Ошибка лексера с позицией."""

    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(f"строка {line}, колонка {column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    """Лексер: превращает текст в поток токенов."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.paren_depth = 0

    def _peek(self) -> str | None:
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def _advance(self) -> str:
        ch = self.text[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def _skip_whitespace(self) -> None:
        while self.pos < len(self.text) and self.text[self.pos] in (" ", "\t", "\r"):
            self._advance()

    def _read_number(self) -> str:
        start = self.pos
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            self._advance()
        return self.text[start : self.pos]

    def _read_identifier(self) -> str:
        start = self.pos
        while self.pos < len(self.text) and (
            self.text[self.pos].isalpha()
            or self.text[self.pos] == "_"
            or self.text[self.pos].isdigit()
        ):
            self._advance()
        return self.text[start : self.pos]

    def next_token(self) -> Token:
        self._skip_whitespace()
        if self.pos >= len(self.text):
            return Token(TokenType.EOF, "", self.line, self.column)

        line = self.line
        column = self.column
        ch = self._peek()

        if ch is None:
            return Token(TokenType.EOF, "", line, column)

        if ch == "\n":
            self._advance()
            if self.paren_depth > 0:
                return self.next_token()
            return Token(TokenType.NEWLINE, "\n", line, column)

        if ch.isdigit():
            value = self._read_number()
            return Token(TokenType.NUMBER, value, line, column)

        if ch.isalpha() or ch == "_":
            value = self._read_identifier()
            if value in KEYWORDS:
                return Token(KEYWORDS[value], value, line, column)
            return Token(TokenType.ID, value, line, column)

        two_char = self.text[self.pos : self.pos + 2]
        if two_char in TWO_CHAR_OPS:
            self._advance()
            self._advance()
            return Token(TWO_CHAR_OPS[two_char], two_char, line, column)

        if ch in SINGLE_CHAR_OPS:
            self._advance()
            token_type = SINGLE_CHAR_OPS[ch]
            if token_type == TokenType.LEFT_PAREN:
                self.paren_depth += 1
            elif token_type == TokenType.RIGHT_PAREN:
                self.paren_depth -= 1
            return Token(token_type, ch, line, column)

        raise LexerError(f"неожиданный символ {ch!r}", line, column)

    def tokenize(self) -> list[Token]:
        """Возвращает список всех токенов до EOF."""
        tokens = []
        while True:
            token = self.next_token()
            tokens.append(token)
            if token.typ == TokenType.EOF:
                break
        return tokens
