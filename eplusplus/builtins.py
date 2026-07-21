"""Lua-style built-in operations for E++ — plain English versions."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from .errors import EppRuntimeError

if TYPE_CHECKING:
    from .interpreter import Interpreter
    from .parser import Node


def eval_builtin(interp: "Interpreter", node: "Node") -> object:
    op = node.value["op"]
    args = node.value.get("args", [])
    line = node.line

    if op == "floor":
        return math.floor(interp._num(interp.eval_expr(args[0]), line))
    if op == "ceiling":
        return math.ceil(interp._num(interp.eval_expr(args[0]), line))
    if op == "round":
        return round(interp._num(interp.eval_expr(args[0]), line))
    if op == "absolute":
        return abs(interp._num(interp.eval_expr(args[0]), line))
    if op == "sqrt":
        return math.sqrt(interp._num(interp.eval_expr(args[0]), line))

    if op == "remainder":
        left = int(interp._num(interp.eval_expr(args[0]), line))
        right = int(interp._num(interp.eval_expr(args[1]), line))
        if right == 0:
            raise EppRuntimeError("You can't modulo by zero!", line)
        return left % right

    if op == "power":
        base = interp._num(interp.eval_expr(args[0]), line)
        exp = interp._num(interp.eval_expr(args[1]), line)
        return base**exp

    if op == "smallest":
        a = interp._num(interp.eval_expr(args[0]), line)
        b = interp._num(interp.eval_expr(args[1]), line)
        return min(a, b)

    if op == "largest":
        a = interp._num(interp.eval_expr(args[0]), line)
        b = interp._num(interp.eval_expr(args[1]), line)
        return max(a, b)

    if op == "slice":
        text = str(interp.eval_expr(args[0]))
        start = int(interp._num(interp.eval_expr(args[1]), line))
        end = int(interp._num(interp.eval_expr(args[2]), line))
        if start < 1:
            start = 1
        if end < start:
            end = start
        return text[start - 1 : end]

    if op == "find":
        needle = str(interp.eval_expr(args[0]))
        haystack = str(interp.eval_expr(args[1]))
        idx = haystack.find(needle)
        return idx + 1 if idx >= 0 else 0

    if op == "replace":
        old = str(interp.eval_expr(args[0]))
        new = str(interp.eval_expr(args[1]))
        text = str(interp.eval_expr(args[2]))
        return text.replace(old, new)

    if op == "split":
        text = str(interp.eval_expr(args[0]))
        sep = str(interp.eval_expr(args[1]))
        if sep == "":
            return list(text)
        return text.split(sep)

    if op == "join":
        items = interp._as_list(interp.eval_expr(args[0]), line)
        sep = str(interp.eval_expr(args[1]))
        return sep.join(interp.to_display(v) for v in items)

    if op == "trim":
        return str(interp.eval_expr(args[0])).strip()

    if op == "starts_with":
        prefix = str(interp.eval_expr(args[0]))
        text = str(interp.eval_expr(args[1]))
        return text.startswith(prefix)

    if op == "ends_with":
        suffix = str(interp.eval_expr(args[0]))
        text = str(interp.eval_expr(args[1]))
        return text.endswith(suffix)

    if op == "copy":
        text = str(interp.eval_expr(args[0]))
        count = int(interp._num(interp.eval_expr(args[1]), line))
        return text * max(0, count)

    if op == "type":
        value = interp.eval_expr(args[0])
        if isinstance(value, bool):
            return "yes/no"
        if isinstance(value, (int, float)):
            return "number"
        if isinstance(value, str):
            return "text"
        if isinstance(value, list):
            return "list"
        if isinstance(value, dict):
            return "object"
        return "unknown"

    if op == "number_from":
        raw = str(interp.eval_expr(args[0]))
        try:
            return float(raw) if "." in raw else int(raw)
        except ValueError as exc:
            raise EppRuntimeError(f"'{raw}' is not a number.", line) from exc

    if op == "text_from":
        return str(interp.eval_expr(args[0]))

    raise EppRuntimeError(f"Unknown built-in '{op}'.", line)
