#!/usr/bin/env python3
"""Run E++ (English++) scripts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from eplusplus import EppError, Interpreter


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="epp",
        description="E++ (English++) — code in plain English, made for kids and beginners",
    )
    parser.add_argument("file", nargs="?", help="Path to a .epp script")
    parser.add_argument("-e", "--eval", dest="code", help="Run E++ code from the command line")
    parser.add_argument("--repl", action="store_true", help="Start an interactive E++ shell")
    parser.add_argument("--open", action="store_true", help="Open the website in your browser after saving")
    parser.add_argument("--version", action="version", version="E++ 0.6.0")
    args = parser.parse_args()

    base_path = Path.cwd()
    if args.file:
        base_path = Path(args.file).resolve().parent

    interpreter = Interpreter(base_path=base_path, open_website=args.open)

    if args.repl:
        return repl(interpreter)
    if args.code:
        return run_source(interpreter, args.code, label="<command>")
    if args.file:
        path = Path(args.file).resolve()
        source = path.read_text(encoding="utf-8")
        interpreter.base_path = path.parent
        return run_source(interpreter, source, label=str(path))

    parser.print_help()
    return 1


def run_source(interpreter: Interpreter, source: str, label: str) -> int:
    try:
        interpreter.run(source)
    except EppError as exc:
        print(f"E++ says: {exc} ({label})", file=sys.stderr)
        return 1
    return 0


def block_depth(source: str) -> bool:
    """True when open blocks are balanced and code is ready to run."""
    opens = source.lower().count("if") + source.lower().count("when")
    opens += source.lower().count("repeat") + source.lower().count("while")
    opens += source.lower().count("until") + source.lower().count("for each")
    opens += source.lower().count("to ")
    closes = source.lower().count("end") + source.lower().count("done")
    return opens <= closes


def repl(interpreter: Interpreter) -> int:
    print("E++ (English++) — type plain English code!")
    print("Examples: say \"Hi!\"   |   let name be \"Jim\"   |   when age is 10 then ... done")
    print("Empty line runs your code. Empty line again to exit.")
    print()

    buffer: list[str] = []
    while True:
        try:
            prompt = "epp> " if not buffer else "... "
            line = input(prompt)
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            buffer.clear()
            continue

        if not line.strip():
            if buffer:
                source = "\n".join(buffer)
                buffer.clear()
                if run_source(interpreter, source, label="<repl>") != 0:
                    continue
            else:
                break
            continue

        buffer.append(line)

        joined = "\n".join(buffer)
        if block_depth(joined):
            source = joined
            buffer.clear()
            if run_source(interpreter, source, label="<repl>") != 0:
                continue

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

