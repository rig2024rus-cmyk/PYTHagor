import pytest

from pythagor.nucleus.lexer import Lexer, LexerError, TokenType


def test_basic_tokenization() -> None:
    tokens = Lexer("2 + 3").tokenize()
    assert len(tokens) == 4
    assert tokens[0].typ == TokenType.NUMBER
    assert tokens[0].value == "2"
    assert tokens[1].typ == TokenType.PLUS
    assert tokens[2].typ == TokenType.NUMBER
    assert tokens[2].value == "3"
    assert tokens[3].typ == TokenType.EOF


def test_all_operators() -> None:
    tokens = Lexer("+ - * < > <= >= == !=").tokenize()
    assert [t.typ for t in tokens[:-1]] == [
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.MUL,
        TokenType.LT,
        TokenType.GT,
        TokenType.LE,
        TokenType.GE,
        TokenType.EQ,
        TokenType.NE,
    ]


def test_russian_keywords() -> None:
    tokens = Lexer("и или не").tokenize()
    assert [t.typ for t in tokens[:-1]] == [
        TokenType.AND,
        TokenType.OR,
        TokenType.NOT,
    ]


def test_parentheses() -> None:
    tokens = Lexer("(2 + 3)").tokenize()
    assert tokens[0].typ == TokenType.LEFT_PAREN
    assert tokens[-2].typ == TokenType.RIGHT_PAREN


def test_position_tracking() -> None:
    tokens = Lexer("2 + 3").tokenize()
    assert tokens[0].line == 1
    assert tokens[0].column == 1
    assert tokens[1].column == 3
    assert tokens[2].column == 5


def test_multiline() -> None:
    text = "2\n+ 3"
    tokens = Lexer(text).tokenize()
    assert tokens[0].line == 1
    assert tokens[1].typ == TokenType.NEWLINE
    assert tokens[2].line == 2
    assert tokens[2].column == 1
    assert tokens[3].line == 2
    assert tokens[3].column == 3


def test_unknown_word_is_identifier() -> None:
    tokens = Lexer("xyz").tokenize()
    assert tokens[0].typ == TokenType.ID
    assert tokens[0].value == "xyz"


def test_unknown_char_raises() -> None:
    with pytest.raises(LexerError) as exc_info:
        Lexer("@").tokenize()
    assert "@" in str(exc_info.value)


def test_empty_input() -> None:
    tokens = Lexer("").tokenize()
    assert len(tokens) == 1
    assert tokens[0].typ == TokenType.EOF


def test_whitespace_only() -> None:
    tokens = Lexer("   \n  \t  ").tokenize()
    assert [t.typ for t in tokens] == [TokenType.NEWLINE, TokenType.EOF]


def test_identifier_token() -> None:
    tokens = Lexer("x").tokenize()
    assert tokens[0].typ == TokenType.ID
    assert tokens[0].value == "x"


def test_cyrillic_identifier() -> None:
    tokens = Lexer("Целое").tokenize()
    assert tokens[0].typ == TokenType.ID
    assert tokens[0].value == "Целое"


def test_assign_versus_eq() -> None:
    tokens = Lexer("= ==").tokenize()
    assert tokens[0].typ == TokenType.ASSIGN
    assert tokens[1].typ == TokenType.EQ


def test_colon_token() -> None:
    tokens = Lexer(":").tokenize()
    assert tokens[0].typ == TokenType.COLON


def test_newline_token() -> None:
    tokens = Lexer("1\n2").tokenize()
    assert [t.typ for t in tokens] == [
        TokenType.NUMBER,
        TokenType.NEWLINE,
        TokenType.NUMBER,
        TokenType.EOF,
    ]


def test_declaration_line_tokens() -> None:
    tokens = Lexer("x: Целое = 5").tokenize()
    assert [t.typ for t in tokens[:-1]] == [
        TokenType.ID,
        TokenType.COLON,
        TokenType.ID,
        TokenType.ASSIGN,
        TokenType.NUMBER,
    ]


def test_consecutive_newlines_kept() -> None:
    tokens = Lexer("1\n\n2").tokenize()
    assert [t.typ for t in tokens] == [
        TokenType.NUMBER,
        TokenType.NEWLINE,
        TokenType.NEWLINE,
        TokenType.NUMBER,
        TokenType.EOF,
    ]
