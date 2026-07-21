from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from .keywords import is_keyword, normalize_word


class TokenType(Enum):
    NUMBER = auto()
    STRING = auto()
    IDENT = auto()
    KEYWORD = auto()
    COMMA = auto()
    NEWLINE = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: str
    line: int


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    line_no = 1
    i = 0
    length = len(source)

    while i < length:
        ch = source[i]

        if ch in " \t\r":
            i += 1
            continue

        if ch == "\n":
            tokens.append(Token(TokenType.NEWLINE, "\n", line_no))
            line_no += 1
            i += 1
            continue

        if ch == "#":
            while i < length and source[i] != "\n":
                i += 1
            continue

        if ch == ",":
            tokens.append(Token(TokenType.COMMA, ",", line_no))
            i += 1
            continue

        if ch == '"':
            i += 1
            start = i
            while i < length and source[i] != '"':
                if source[i] == "\\" and i + 1 < length:
                    i += 2
                else:
                    i += 1
            if i >= length:
                raise ValueError(f"Line {line_no}: Oops! You opened a quote \" but forgot to close it.")
            value = source[start:i]
            tokens.append(Token(TokenType.STRING, value, line_no))
            i += 1
            continue

        if ch.isdigit() or (ch == "." and i + 1 < length and source[i + 1].isdigit()):
            start = i
            while i < length and (source[i].isdigit() or source[i] == "."):
                i += 1
            tokens.append(Token(TokenType.NUMBER, source[start:i], line_no))
            continue

        if ch.isalpha() or ch == "_":
            start = i
            while i < length and (source[i].isalnum() or source[i] == "_"):
                i += 1
            word = source[start:i]
            lower = word.lower()
            if is_keyword(lower):
                tokens.append(Token(TokenType.KEYWORD, normalize_word(lower), line_no))
            else:
                tokens.append(Token(TokenType.IDENT, word, line_no))
            continue

        if ch == ":":
            if i + 1 < length and source[i + 1] == " ":
                while i < length and source[i] != "\n":
                    i += 1
                continue
            raise ValueError(f"Line {line_no}: Unexpected character ':'")

        raise ValueError(f"Line {line_no}: Unexpected character {ch!r}")

    tokens.append(Token(TokenType.EOF, "", line_no))
    return tokens


def strip_newlines(tokens: list[Token]) -> list[Token]:
    cleaned: list[Token] = []
    for token in tokens:
        if token.type == TokenType.NEWLINE:
            continue
        cleaned.append(token)
    return cleaned
