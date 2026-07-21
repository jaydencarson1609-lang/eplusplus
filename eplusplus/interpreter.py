from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from pathlib import Path

from .builtins import eval_builtin
from .errors import EppRuntimeError, EppSyntaxError
from .parser import Node, NodeKind, parse


class ReturnSignal(Exception):
    def __init__(self, value: object) -> None:
        self.value = value
        super().__init__()


class BreakSignal(Exception):
    pass


@dataclass
class FunctionValue:
    name: str
    params: list[str]
    body: list[Node]


class Environment:
    def __init__(self, parent: Environment | None = None) -> None:
        self.parent = parent
        self.vars: dict[str, object] = {}
        self.functions: dict[str, FunctionValue] = {}

    def get(self, name: str, line: int | None = None) -> object:
        key = name.lower()
        if key in self.vars:
            return self.vars[key]
        if self.parent:
            return self.parent.get(name, line)
        raise EppRuntimeError(
            f"I don't know a variable called '{name}'. Did you create it first?",
            line,
        )

    def set(self, name: str, value: object) -> None:
        self.vars[name.lower()] = value

    def set_local(self, name: str, value: object) -> None:
        self.vars[name.lower()] = value

    def define_function(self, fn: FunctionValue) -> None:
        self.functions[fn.name.lower()] = fn

    def get_function(self, name: str, line: int | None = None) -> FunctionValue:
        key = name.lower()
        if key in self.functions:
            return self.functions[key]
        if self.parent:
            return self.parent.get_function(name, line)
        raise EppRuntimeError(
            f"I don't know a recipe called '{name}'. Did you write 'to {name} do ... done' first?",
            line,
        )

    def all_names(self) -> set[str]:
        names = set(self.vars.keys()) | set(self.functions.keys())
        if self.parent:
            names |= self.parent.all_names()
        return names


class Interpreter:
    def __init__(
        self,
        env: Environment | None = None,
        input_fn=input,
        output_fn=print,
        base_path: Path | None = None,
        loaded_files: set[str] | None = None,
        is_module: bool = False,
    ) -> None:
        self.env = env or Environment()
        self.input_fn = input_fn
        self.output_fn = output_fn
        self.base_path = (base_path or Path.cwd()).resolve()
        self.loaded_files = loaded_files if loaded_files is not None else set()
        self.is_module = is_module
        self.shared_names: set[str] = set()

    def run(self, source: str) -> None:
        try:
            tree = parse(source)
        except EppSyntaxError:
            raise
        except ValueError as exc:
            raise EppSyntaxError(str(exc)) from exc
        self.execute_program(tree)

    def execute_program(self, node: Node) -> None:
        for stmt in node.children or []:
            self.execute(stmt)

    def execute(self, node: Node) -> None:
        kind = node.kind

        if kind == NodeKind.NOOP:
            return

        if kind == NodeKind.IMPORT:
            self.execute_import(node)
            return

        if kind == NodeKind.SHARE:
            for name in node.value:
                self.shared_names.add(name.lower())
            return

        if kind == NodeKind.CLEAR:
            self.output_fn("\033[2J\033[H", end="")
            return

        if kind == NodeKind.APPEND:
            target = node.value["target"]
            item = self.eval_expr(node.value["item"])
            current = self.env.get(target, node.line)
            items = list(self._as_list(current, node.line))
            items.append(item)
            self.env.set(target, items)
            return

        if kind == NodeKind.REMOVE:
            name = node.value["name"]
            current = list(self._as_list(self.env.get(name, node.line), node.line))
            if node.value["mode"] == "index":
                index = int(self._num(self.eval_expr(node.value["value"]), node.line))
                if index == -1:
                    index = len(current)
                if index < 1 or index > len(current):
                    raise EppRuntimeError(f"List item #{index} does not exist.", node.line)
                current.pop(index - 1)
            else:
                item = self.eval_expr(node.value["value"])
                if item in current:
                    current.remove(item)
                else:
                    for i, v in enumerate(current):
                        if str(v) == str(item):
                            current.pop(i)
                            break
            self.env.set(name, current)
            return

        if kind == NodeKind.SORT:
            current = list(self._as_list(self.env.get(node.value, node.line), node.line))
            current.sort(key=lambda v: str(v))
            self.env.set(node.value, current)
            return

        if kind == NodeKind.REVERSE:
            current = list(self._as_list(self.env.get(node.value, node.line), node.line))
            current.reverse()
            self.env.set(node.value, current)
            return

        if kind == NodeKind.BREAK:
            raise BreakSignal()

        if kind == NodeKind.RETURN:
            raise ReturnSignal(self.eval_expr(node.value))

        if kind == NodeKind.ASSIGN:
            name = node.value["name"]
            value = self.eval_expr(node.value["expr"])
            self.env.set(name, value)
            return

        if kind == NodeKind.OBJECT:
            name = node.value["name"]
            obj: dict[str, object] = {}
            for key, expr_node in node.value["fields"].items():
                obj[key.lower()] = self.eval_expr(expr_node)
            self.env.set(name, obj)
            return

        if kind == NodeKind.SAY:
            self.output_fn(self.to_display(self.eval_expr(node.value)))
            return

        if kind == NodeKind.SHOW:
            self.output_fn(self.to_display(self.eval_expr(node.value)))
            return

        if kind == NodeKind.ASK:
            prompt = self.to_display(self.eval_expr(node.value["prompt"]))
            if prompt:
                self.output_fn(prompt, end="")
            else:
                self.output_fn(f"What is {node.value['name']}? ", end="")
            answer = self.input_fn()
            self.env.set(node.value["name"], answer)
            return

        if kind == NodeKind.WAIT:
            amount = self.eval_expr(node.value["amount"])
            unit = node.value["unit"]
            seconds = float(amount)
            if unit == "minute":
                seconds *= 60
            time.sleep(max(0, seconds))
            return

        if kind == NodeKind.IF:
            if self.is_truthy(self.eval_expr(node.value["condition"])):
                if self._run_block(node.children or []):
                    raise BreakSignal()
            elif node.value["else"]:
                if self._run_block(node.value["else"]):
                    raise BreakSignal()
            return

        if kind == NodeKind.REPEAT:
            count_value = self.eval_expr(node.value)
            count = int(self._num(count_value, node.line))
            for _ in range(max(0, count)):
                if self._run_block(node.children or []):
                    break
            return

        if kind == NodeKind.WHILE:
            while self.is_truthy(self.eval_expr(node.value)):
                if self._run_block(node.children or []):
                    break
            return

        if kind == NodeKind.UNTIL:
            while not self.is_truthy(self.eval_expr(node.value)):
                if self._run_block(node.children or []):
                    break
            return

        if kind == NodeKind.FOR_EACH:
            var_name = node.value["var"]
            iterable = self.eval_expr(node.value["iterable"])
            items = self._as_list(iterable, node.line)
            for item in items:
                self.env.set(var_name, item)
                if self._run_block(node.children or []):
                    break
            return

        if kind == NodeKind.FOR_RANGE:
            var_name = node.value["var"]
            start = int(self._num(self.eval_expr(node.value["start"]), node.line))
            end = int(self._num(self.eval_expr(node.value["end"]), node.line))
            step = 1 if start <= end else -1
            value = start
            while (step > 0 and value <= end) or (step < 0 and value >= end):
                self.env.set(var_name, value)
                if self._run_block(node.children or []):
                    break
                value += step
            return

        if kind == NodeKind.FUNCTION:
            fn = FunctionValue(
                name=node.value["name"],
                params=node.value["params"],
                body=node.children or [],
            )
            self.env.define_function(fn)
            return

        if kind == NodeKind.CALL:
            self.call_function(node.value["name"], node.value["args"], node.line)
            return

        raise EppRuntimeError("Something went wrong running the program (unknown step).", node.line)

    def _run_block(self, statements: list[Node]) -> bool:
        """Run statements. Returns True if loop should break."""
        for stmt in statements:
            try:
                self.execute(stmt)
            except BreakSignal:
                return True
        return False

    def execute_import(self, node: Node) -> None:
        rel_path = node.value
        resolved = self.resolve_script_path(rel_path, node.line)
        canonical = str(resolved)

        if canonical in self.loaded_files:
            return

        self.loaded_files.add(canonical)
        source = resolved.read_text(encoding="utf-8")

        module_env = Environment()
        module_interp = Interpreter(
            env=module_env,
            input_fn=self.input_fn,
            output_fn=self.output_fn,
            base_path=resolved.parent,
            loaded_files=self.loaded_files,
            is_module=True,
        )
        module_interp.run(source)
        self.merge_module(module_env, module_interp.shared_names, rel_path, node.line)

    def merge_module(
        self,
        module_env: Environment,
        shared_names: set[str],
        rel_path: str,
        line: int | None,
    ) -> None:
        if shared_names:
            names = shared_names
        else:
            names = set(module_env.vars.keys()) | set(module_env.functions.keys())

        for name in sorted(names):
            if name in module_env.vars:
                self.env.set(name, module_env.vars[name])
            elif name in module_env.functions:
                self.env.define_function(module_env.functions[name])
            else:
                raise EppRuntimeError(
                    f"The file '{rel_path}' does not share anything called '{name}'. "
                    f"Add 'share {name}' in that file.",
                    line,
                )

    def resolve_script_path(self, rel_path: str, line: int | None) -> Path:
        direct = (self.base_path / rel_path).resolve()
        if direct.exists():
            return direct

        project_root = Path(__file__).resolve().parent.parent
        stdlib = (project_root / rel_path).resolve()
        if stdlib.exists():
            return stdlib

        stdlib_named = (project_root / "stdlib" / rel_path).resolve()
        if stdlib_named.exists():
            return stdlib_named

        raise EppRuntimeError(
            f"I couldn't find the script '{rel_path}'. "
            f"Looked in {self.base_path} and the E++ stdlib folder.",
            line,
        )

    def call_function(self, name: str, arg_nodes: list[Node], line: int | None) -> object:
        fn = self.env.get_function(name, line)
        if len(arg_nodes) != len(fn.params):
            raise EppRuntimeError(
                f"Recipe '{fn.name}' needs {len(fn.params)} input(s), but got {len(arg_nodes)}.",
                line,
            )
        call_env = Environment(parent=self.env)
        for param, arg_node in zip(fn.params, arg_nodes):
            call_env.set_local(param, self.eval_expr(arg_node))
        child = Interpreter(
            call_env,
            input_fn=self.input_fn,
            output_fn=self.output_fn,
            base_path=self.base_path,
            loaded_files=self.loaded_files,
        )
        try:
            for stmt in fn.body:
                child.execute(stmt)
        except ReturnSignal as signal:
            return signal.value
        return None

    def eval_expr(self, node: Node) -> object:
        kind = node.kind

        if kind == NodeKind.LITERAL:
            return node.value

        if kind == NodeKind.VAR:
            return self.env.get(node.value, node.line)

        if kind == NodeKind.LIST:
            return [self.eval_expr(item) for item in node.value]

        if kind == NodeKind.CALL:
            result = self.call_function(node.value["name"], node.value["args"], node.line)
            if result is None:
                raise EppRuntimeError(
                    f"Recipe '{node.value['name']}' did not give back a value. "
                    f"Add 'give back ...' inside it.",
                    node.line,
                )
            return result

        if kind == NodeKind.MEMBER:
            obj = self.eval_expr(node.value["object"])
            field = node.value["field"].lower()
            if not isinstance(obj, dict):
                raise EppRuntimeError("That value is not an object with named parts.", node.line)
            if field not in obj:
                raise EppRuntimeError(f"This object has no part called '{field}'.", node.line)
            return obj[field]

        if kind == NodeKind.INDEX:
            target = self.eval_expr(node.value["target"])
            items = self._as_list(target, node.line)
            raw_index = node.value["index"]
            if isinstance(raw_index, Node):
                index = int(self._num(self.eval_expr(raw_index), node.line))
            else:
                index = int(raw_index)
            if index == -1:
                index = len(items)
            if index < 1 or index > len(items):
                raise EppRuntimeError(
                    f"List item #{index} does not exist (this list has {len(items)} items).",
                    node.line,
                )
            return items[index - 1]

        if kind == NodeKind.UNOP:
            if node.value == "not":
                return not self.is_truthy(self.eval_expr(node.left))
            if node.value == "length":
                return self._length(self.eval_expr(node.left), node.line)
            if node.value == "uppercase":
                return str(self.eval_expr(node.left)).upper()
            if node.value == "lowercase":
                return str(self.eval_expr(node.left)).lower()
            raise EppRuntimeError(f"Unknown operator '{node.value}'.", node.line)

        if kind == NodeKind.PICK:
            items = self._as_list(self.eval_expr(node.value), node.line)
            if not items:
                raise EppRuntimeError("Can't pick from an empty list.", node.line)
            return random.choice(items)

        if kind == NodeKind.BUILTIN:
            return eval_builtin(self, node)

        if kind == NodeKind.RANDOM:
            low = int(self._num(self.eval_expr(node.value["low"]), node.line))
            high = int(self._num(self.eval_expr(node.value["high"]), node.line))
            if low > high:
                low, high = high, low
            return random.randint(low, high)

        if kind == NodeKind.BINOP:
            op = node.value
            left = self.eval_expr(node.left)
            right = self.eval_expr(node.right)

            if op == "+":
                return self._add(left, right, node.line)
            if op == "-":
                return self._num(left, node.line) - self._num(right, node.line)
            if op == "*":
                return self._num(left, node.line) * self._num(right, node.line)
            if op == "/":
                divisor = self._num(right, node.line)
                if divisor == 0:
                    raise EppRuntimeError("You can't divide by zero!", node.line)
                return self._num(left, node.line) / divisor
            if op == "%":
                divisor = self._num(right, node.line)
                if divisor == 0:
                    raise EppRuntimeError("You can't modulo by zero!", node.line)
                return int(self._num(left, node.line)) % int(divisor)
            if op == "==":
                return self._compare_equal(left, right)
            if op == "!=":
                return not self._compare_equal(left, right)
            if op == ">":
                return self._num(left, node.line) > self._num(right, node.line)
            if op == "<":
                return self._num(left, node.line) < self._num(right, node.line)
            if op == "and":
                return self.is_truthy(left) and self.is_truthy(right)
            if op == "or":
                return self.is_truthy(left) or self.is_truthy(right)
            if op == "in":
                return self._contains(right, left, node.line)
            raise EppRuntimeError(f"Unknown operator '{op}'.", node.line)

        raise EppRuntimeError("I couldn't figure out this value.", node.line)

    @staticmethod
    def _length(value: object, line: int | None) -> int:
        if isinstance(value, str):
            return len(value)
        if isinstance(value, list):
            return len(value)
        raise EppRuntimeError("length of only works on text or lists.", line)

    @staticmethod
    def _contains(container: object, item: object, line: int | None) -> bool:
        if isinstance(container, list):
            return item in container or str(item) in [str(x) for x in container]
        if isinstance(container, str):
            return str(item) in container
        raise EppRuntimeError("'is in' only works with lists or text.", line)

    @staticmethod
    def _as_list(value: object, line: int | None) -> list[object]:
        if isinstance(value, list):
            return value
        raise EppRuntimeError("That is not a list.", line)

    @staticmethod
    def _add(left: object, right: object, line: int | None) -> object:
        if isinstance(left, str) or isinstance(right, str):
            return str(left) + str(right)
        return Interpreter._num(left, line) + Interpreter._num(right, line)

    @staticmethod
    def _num(value: object, line: int | None) -> float:
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, bool):
            return 1.0 if value else 0.0
        if isinstance(value, str):
            try:
                return float(value) if "." in value else float(int(value))
            except ValueError as exc:
                raise EppRuntimeError(f"'{value}' is not a number.", line) from exc
        raise EppRuntimeError(f"I expected a number, not {type(value).__name__}.", line)

    @staticmethod
    def _compare_equal(left: object, right: object) -> bool:
        if isinstance(left, bool) or isinstance(right, bool):
            return bool(left) == bool(right)
        if isinstance(left, str) or isinstance(right, str):
            return str(left) == str(right)
        return left == right

    @staticmethod
    def is_truthy(value: object) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return value != ""
        if isinstance(value, list):
            return len(value) > 0
        if isinstance(value, dict):
            return len(value) > 0
        return bool(value)

    @staticmethod
    def to_display(value: object) -> str:
        if isinstance(value, bool):
            return "yes" if value else "no"
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        if isinstance(value, list):
            parts = [Interpreter.to_display(v) for v in value]
            return "[" + ", ".join(parts) + "]"
        if isinstance(value, dict):
            parts = [f"{k}: {Interpreter.to_display(v)}" for k, v in value.items()]
            return "{" + ", ".join(parts) + "}"
        return str(value)
