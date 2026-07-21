from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from .errors import EppSyntaxError
from .lexer import Token, TokenType, strip_newlines, tokenize


class NodeKind(Enum):
    PROGRAM = auto()
    ASSIGN = auto()
    SAY = auto()
    SHOW = auto()
    IF = auto()
    REPEAT = auto()
    WHILE = auto()
    UNTIL = auto()
    FOR_EACH = auto()
    ASK = auto()
    WAIT = auto()
    FUNCTION = auto()
    CALL = auto()
    IMPORT = auto()
    SHARE = auto()
    RETURN = auto()
    NOOP = auto()
    BINOP = auto()
    UNOP = auto()
    LITERAL = auto()
    VAR = auto()
    LIST = auto()
    OBJECT = auto()
    MEMBER = auto()
    INDEX = auto()


@dataclass
class Node:
    kind: NodeKind
    value: Any = None
    left: Node | None = None
    right: Node | None = None
    children: list[Node] | None = None
    line: int | None = None


BLOCK_STARTERS = {
    "say",
    "show",
    "if",
    "repeat",
    "while",
    "until",
    "for",
    "to",
    "run",
    "ask",
    "wait",
    "let",
    "make",
    "set",
    "note",
    "end",
    "else",
    "use",
    "bring",
    "import",
    "share",
    "give",
}


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        token = self.current()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token

    def match_keyword(self, word: str) -> bool:
        token = self.current()
        if token.type == TokenType.KEYWORD and token.value == word:
            self.advance()
            return True
        return False

    def expect_keyword(self, word: str) -> Token:
        token = self.current()
        if token.type != TokenType.KEYWORD or token.value != word:
            raise EppSyntaxError(
                f"I expected the word '{word}' here, but found '{token.value}' instead.",
                token.line,
            )
        return self.advance()

    def skip_the(self) -> None:
        while self.match_keyword("the"):
            pass

    def parse(self) -> Node:
        statements: list[Node] = []
        while self.current().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return Node(NodeKind.PROGRAM, children=statements)

    def parse_statement(self) -> Node:
        self.skip_the()
        token = self.current()
        line = token.line

        if token.type == TokenType.KEYWORD:
            kw = token.value
            if kw in {"say", "tell", "speak", "print"}:
                return self.parse_say()
            if kw == "show":
                return self.parse_show()
            if kw == "if":
                return self.parse_if()
            if kw == "repeat":
                return self.parse_repeat()
            if kw == "while":
                return self.parse_while()
            if kw == "until":
                return self.parse_until()
            if kw == "for":
                return self.parse_for_each()
            if kw == "to":
                return self.parse_function()
            if kw == "run":
                return self.parse_call()
            if kw == "use":
                return self.parse_import()
            if kw == "import":
                return self.parse_import()
            if kw == "bring":
                return self.parse_import()
            if kw == "share":
                return self.parse_share()
            if kw == "give":
                return self.parse_return()
            if kw == "ask":
                return self.parse_ask()
            if kw == "wait":
                return self.parse_wait()
            if kw == "let":
                return self.parse_let_assign()
            if kw == "make":
                return self.parse_make_assign()
            if kw == "set":
                return self.parse_set_assign()
            if kw == "note":
                self.skip_note()
                return Node(NodeKind.NOOP, line=line)
            if kw == "end":
                raise EppSyntaxError("'end' / 'done' appeared outside of a block. Did you forget to open one?", line)
            if kw == "else":
                raise EppSyntaxError("'else' / 'otherwise' appeared outside of an if block.", line)
            if kw == "keep":
                return self.parse_keep_while()

        if token.type == TokenType.IDENT:
            return self.parse_assign_or_object()

        raise EppSyntaxError(f"I don't understand '{token.value}' here.", line)

    def skip_note(self) -> None:
        self.expect_keyword("note")
        while self.current().type != TokenType.EOF:
            token = self.current()
            if token.type == TokenType.KEYWORD and token.value in BLOCK_STARTERS:
                break
            if token.type == TokenType.IDENT:
                break
            self.advance()

    def parse_assign_or_object(self) -> Node:
        name_token = self.advance()
        name = name_token.value
        line = name_token.line

        if self.match_keyword("has"):
            return self.parse_object_fields(name, line)

        self.expect_keyword("is")

        if self.match_keyword("called"):
            value = self.parse_value()
            return Node(NodeKind.ASSIGN, value={"name": name, "expr": value}, line=line)

        if self.current().type == TokenType.STRING and self._peek_type(1) == TokenType.COMMA:
            expr = self.parse_list_or_single()
            return Node(NodeKind.ASSIGN, value={"name": name, "expr": expr}, line=line)

        expr = self.parse_expression()
        return Node(NodeKind.ASSIGN, value={"name": name, "expr": expr}, line=line)

    def _peek_type(self, offset: int) -> TokenType | None:
        idx = self.pos + offset
        if idx >= len(self.tokens):
            return None
        return self.tokens[idx].type

    def parse_list_or_single(self) -> Node:
        items = [self.parse_value()]
        line = items[0].line
        while self.current().type == TokenType.COMMA:
            self.advance()
            items.append(self.parse_value())
        if len(items) == 1:
            return items[0]
        return Node(NodeKind.LIST, value=items, line=line)

    def parse_object_fields(self, name: str, line: int) -> Node:
        fields: dict[str, Node] = {}
        while True:
            self.skip_the()
            key_token = self.current()
            if key_token.type != TokenType.IDENT:
                break
            key = self.advance().value
            if self.match_keyword("called"):
                fields[key] = self.parse_value()
            elif self.match_keyword("is"):
                fields[key] = self.parse_expression()
            else:
                fields[key] = self.parse_primary()
            if not self.match_keyword("and"):
                break
        return Node(NodeKind.OBJECT, value={"name": name, "fields": fields}, line=line)

    def parse_let_assign(self) -> Node:
        line = self.current().line
        self.expect_keyword("let")
        self.skip_the()
        name = self.advance().value
        self.expect_keyword("is")  # "be" normalizes to "is"
        expr = self.parse_expression()
        return Node(NodeKind.ASSIGN, value={"name": name, "expr": expr}, line=line)

    def parse_make_assign(self) -> Node:
        line = self.current().line
        self.expect_keyword("make")
        self.skip_the()
        name = self.advance().value
        self.expect_keyword("equal")
        self.expect_keyword("to")
        expr = self.parse_expression()
        return Node(NodeKind.ASSIGN, value={"name": name, "expr": expr}, line=line)

    def parse_set_assign(self) -> Node:
        line = self.current().line
        self.expect_keyword("set")
        self.skip_the()
        name = self.advance().value
        self.expect_keyword("to")
        expr = self.parse_expression()
        return Node(NodeKind.ASSIGN, value={"name": name, "expr": expr}, line=line)

    def parse_say(self) -> Node:
        line = self.current().line
        self.expect_keyword("say")
        expr = self.parse_expression()
        return Node(NodeKind.SAY, value=expr, line=line)

    def parse_show(self) -> Node:
        line = self.current().line
        self.expect_keyword("show")
        expr = self.parse_expression()
        return Node(NodeKind.SHOW, value=expr, line=line)

    def parse_ask(self) -> Node:
        line = self.current().line
        self.expect_keyword("ask")
        self.skip_the()
        name = self.advance().value
        if self.match_keyword("with"):
            prompt = self.parse_expression()
        else:
            prompt = Node(NodeKind.LITERAL, value="", line=line)
        return Node(NodeKind.ASK, value={"name": name, "prompt": prompt}, line=line)

    def parse_wait(self) -> Node:
        line = self.current().line
        self.expect_keyword("wait")
        amount = self.parse_expression()
        unit = "second"
        if self.match_keyword("second"):
            unit = "second"
        elif self.match_keyword("minute"):
            unit = "minute"
        return Node(NodeKind.WAIT, value={"amount": amount, "unit": unit}, line=line)

    def parse_if(self) -> Node:
        line = self.current().line
        self.expect_keyword("if")
        condition = self.parse_expression()
        self.expect_keyword("then")
        body = self.parse_block(stop_on_else=True)
        else_body: list[Node] | None = None
        if self.current().type == TokenType.KEYWORD and self.current().value == "else":
            self.advance()
            else_body = self.parse_block()
        self.expect_keyword("end")
        return Node(NodeKind.IF, value={"condition": condition, "else": else_body}, children=body, line=line)

    def parse_repeat(self) -> Node:
        line = self.current().line
        self.expect_keyword("repeat")
        count = self.parse_repeat_count()
        self.expect_keyword("times")
        body = self.parse_block()
        self.expect_keyword("end")
        return Node(NodeKind.REPEAT, value=count, children=body, line=line)

    def parse_keep_while(self) -> Node:
        line = self.current().line
        self.expect_keyword("keep")
        self.expect_keyword("going")
        self.expect_keyword("while")
        condition = self.parse_expression()
        self.expect_keyword("do")
        body = self.parse_block()
        self.expect_keyword("end")
        return Node(NodeKind.WHILE, value=condition, children=body, line=line)

    def parse_while(self) -> Node:
        line = self.current().line
        self.expect_keyword("while")
        condition = self.parse_expression()
        self.expect_keyword("do")
        body = self.parse_block()
        self.expect_keyword("end")
        return Node(NodeKind.WHILE, value=condition, children=body, line=line)

    def parse_until(self) -> Node:
        line = self.current().line
        self.expect_keyword("until")
        condition = self.parse_expression()
        self.expect_keyword("do")
        body = self.parse_block()
        self.expect_keyword("end")
        return Node(NodeKind.UNTIL, value=condition, children=body, line=line)

    def parse_for_each(self) -> Node:
        line = self.current().line
        self.expect_keyword("for")
        self.expect_keyword("each")
        self.skip_the()
        var = self.advance().value
        self.expect_keyword("in")
        self.skip_the()
        iterable = self.parse_expression()
        self.expect_keyword("do")
        body = self.parse_block()
        self.expect_keyword("end")
        return Node(NodeKind.FOR_EACH, value={"var": var, "iterable": iterable}, children=body, line=line)

    def parse_function(self) -> Node:
        line = self.current().line
        self.expect_keyword("to")
        name = self.advance().value
        params: list[str] = []
        while self.current().type == TokenType.IDENT:
            params.append(self.advance().value)
            if not self.match_keyword("and"):
                break
        self.expect_keyword("do")
        body = self.parse_block()
        self.expect_keyword("end")
        return Node(NodeKind.FUNCTION, value={"name": name, "params": params}, children=body, line=line)

    def parse_import(self) -> Node:
        line = self.current().line
        keyword = self.advance().value

        if keyword == "bring":
            self.expect_keyword("in")
        elif keyword == "use":
            if self.current().type == TokenType.IDENT and self.current().value.lower() == "script":
                self.advance()
                self.expect_keyword("from")

        path_token = self.current()
        if path_token.type != TokenType.STRING:
            raise EppSyntaxError(
                "I need a file path in quotes, like use \"helpers.epp\".",
                path_token.line,
            )
        self.advance()
        return Node(NodeKind.IMPORT, value=path_token.value, line=line)

    def parse_share(self) -> Node:
        line = self.current().line
        self.expect_keyword("share")
        names = [self._expect_ident()]
        while self.match_keyword("and"):
            names.append(self._expect_ident())
        return Node(NodeKind.SHARE, value=names, line=line)

    def parse_return(self) -> Node:
        line = self.current().line
        self.expect_keyword("give")
        self.expect_keyword("back")
        expr = self.parse_expression()
        return Node(NodeKind.RETURN, value=expr, line=line)

    def _expect_ident(self) -> str:
        token = self.current()
        if token.type != TokenType.IDENT:
            raise EppSyntaxError("I need a name here.", token.line)
        return self.advance().value

    def parse_call(self) -> Node:
        return self._parse_call()

    def _parse_call(self) -> Node:
        line = self.current().line
        self.expect_keyword("run")
        name = self.advance().value
        args: list[Node] = []
        if self.match_keyword("with"):
            args.append(self.parse_call_arg())
            while self.match_keyword("and"):
                args.append(self.parse_call_arg())
        return Node(NodeKind.CALL, value={"name": name, "args": args}, line=line)

    def parse_call_arg(self) -> Node:
        return self.parse_comparison()

    def parse_repeat_count(self) -> Node:
        node = self.parse_primary()
        while True:
            token = self.current()
            if token.type == TokenType.KEYWORD and token.value == "plus":
                self.advance()
                right = self.parse_primary()
                node = Node(NodeKind.BINOP, value="+", left=node, right=right, line=token.line)
            elif token.type == TokenType.KEYWORD and token.value == "minus":
                self.advance()
                right = self.parse_primary()
                node = Node(NodeKind.BINOP, value="-", left=node, right=right, line=token.line)
            else:
                break
        return node

    def parse_block(self, stop_on_else: bool = False) -> list[Node]:
        body: list[Node] = []
        while self.current().type != TokenType.EOF:
            token = self.current()
            if token.type == TokenType.KEYWORD:
                if token.value == "end":
                    break
                if stop_on_else and token.value == "else":
                    break
            body.append(self.parse_statement())
        return body

    def parse_value(self) -> Node:
        token = self.current()
        if token.type == TokenType.STRING:
            self.advance()
            return Node(NodeKind.LITERAL, value=token.value, line=token.line)
        if token.type == TokenType.NUMBER:
            self.advance()
            return Node(NodeKind.LITERAL, value=float(token.value) if "." in token.value else int(token.value), line=token.line)
        if token.type == TokenType.IDENT:
            self.advance()
            return Node(NodeKind.VAR, value=token.value, line=token.line)
        raise EppSyntaxError("I need a value here (text in quotes, a number, or a name).", token.line)

    def parse_expression(self) -> Node:
        return self.parse_or()

    def parse_or(self) -> Node:
        node = self.parse_and()
        while self.match_keyword("or"):
            right = self.parse_and()
            node = Node(NodeKind.BINOP, value="or", left=node, right=right, line=node.line)
        return node

    def parse_and(self) -> Node:
        node = self.parse_comparison()
        while self.match_keyword("and"):
            right = self.parse_comparison()
            node = Node(NodeKind.BINOP, value="and", left=node, right=right, line=node.line)
        return node

    def parse_comparison(self) -> Node:
        node = self.parse_addition()
        while True:
            token = self.current()
            if token.type != TokenType.KEYWORD:
                break
            op: str | None = None
            if token.value == "is":
                op = self._parse_is_comparison()
            elif token.value == "greater":
                self.advance()
                self.expect_keyword("than")
                op = ">"
            elif token.value == "less":
                self.advance()
                self.expect_keyword("than")
                op = "<"
            elif token.value == "equal":
                self.advance()
                self.expect_keyword("to")
                op = "=="
            elif token.value == "not":
                self.advance()
                self.expect_keyword("equal")
                self.expect_keyword("to")
                op = "!="
            else:
                break
            if op is None:
                break
            right = self.parse_addition()
            node = Node(NodeKind.BINOP, value=op, left=node, right=right, line=token.line)
        return node

    def _parse_is_comparison(self) -> str | None:
        line = self.current().line
        self.advance()
        if self.match_keyword("not"):
            self.expect_keyword("equal")
            self.expect_keyword("to")
            return "!="
        if self.match_keyword("equal"):
            self.expect_keyword("to")
            return "=="
        if self.match_keyword("greater"):
            self.expect_keyword("than")
            return ">"
        if self.match_keyword("less"):
            self.expect_keyword("than")
            return "<"
        if self.match_keyword("called"):
            raise EppSyntaxError("'is called' is only for making variables, not for comparing.", line)
        return "=="

    def parse_addition(self) -> Node:
        node = self.parse_multiplication()
        while True:
            token = self.current()
            if token.type == TokenType.KEYWORD and token.value == "plus":
                self.advance()
                right = self.parse_multiplication()
                node = Node(NodeKind.BINOP, value="+", left=node, right=right, line=token.line)
            elif token.type == TokenType.KEYWORD and token.value == "minus":
                self.advance()
                right = self.parse_multiplication()
                node = Node(NodeKind.BINOP, value="-", left=node, right=right, line=token.line)
            else:
                break
        return node

    def parse_multiplication(self) -> Node:
        node = self.parse_postfix()
        while True:
            token = self.current()
            if token.type == TokenType.KEYWORD and token.value == "times":
                self.advance()
                right = self.parse_postfix()
                node = Node(NodeKind.BINOP, value="*", left=node, right=right, line=token.line)
            elif token.type == TokenType.KEYWORD and token.value == "divided":
                self.advance()
                self.expect_keyword("by")
                right = self.parse_postfix()
                node = Node(NodeKind.BINOP, value="/", left=node, right=right, line=token.line)
            else:
                break
        return node

    def parse_postfix(self) -> Node:
        node = self.parse_primary()
        while True:
            if self.match_keyword("of"):
                self.skip_the()
                if node.kind != NodeKind.VAR:
                    raise EppSyntaxError("Use 'something of object' like: name of player", node.line)
                field = node.value
                obj = self.parse_primary()
                node = Node(NodeKind.MEMBER, value={"object": obj, "field": field}, line=node.line)
                continue
            if self.match_keyword("in"):
                break
            break
        return node

    def parse_primary(self) -> Node:
        self.skip_the()

        if self.match_keyword("first"):
            self.expect_keyword("item")
            self.expect_keyword("in")
            self.skip_the()
            lst = self.parse_primary()
            return Node(NodeKind.INDEX, value={"target": lst, "index": 1}, line=lst.line)

        if self.match_keyword("last"):
            self.expect_keyword("item")
            self.expect_keyword("in")
            self.skip_the()
            lst = self.parse_primary()
            return Node(NodeKind.INDEX, value={"target": lst, "index": -1}, line=lst.line)

        if self.match_keyword("item"):
            idx_node = self.parse_primary()
            self.expect_keyword("of")
            self.skip_the()
            lst = self.parse_primary()
            return Node(NodeKind.INDEX, value={"target": lst, "index": idx_node}, line=lst.line)

        if self.current().type == TokenType.KEYWORD and self.current().value == "run":
            return self._parse_call()

        token = self.current()
        if token.type == TokenType.STRING:
            self.advance()
            return Node(NodeKind.LITERAL, value=token.value, line=token.line)
        if token.type == TokenType.NUMBER:
            self.advance()
            value: int | float = float(token.value) if "." in token.value else int(token.value)
            return Node(NodeKind.LITERAL, value=value, line=token.line)
        if token.type == TokenType.KEYWORD and token.value in {"true", "false"}:
            self.advance()
            return Node(NodeKind.LITERAL, value=(token.value == "true"), line=token.line)
        if token.type == TokenType.IDENT:
            self.advance()
            return Node(NodeKind.VAR, value=token.value, line=token.line)
        if token.type == TokenType.KEYWORD and token.value == "not":
            line = token.line
            self.advance()
            expr = self.parse_primary()
            return Node(NodeKind.UNOP, value="not", left=expr, line=line)
        raise EppSyntaxError(f"I need a value here, not '{token.value}'.", token.line)


def parse(source: str) -> Node:
    tokens = strip_newlines(tokenize(source))
    return Parser(tokens).parse()
