#!/usr/local/bin/python3.10

import sys
from core.lexer import lex
from core.interpreter import interpret


def main() -> None:
    if len(sys.argv) <= 1:
        sys.stderr.write("emond: no input file\n")
        exit(1)

    source_file = sys.argv[1]
    with open(source_file) as f:
        contents = f.read().strip()
    source, tokens = lex(contents)
    interpret(source, tokens, 1000)


if __name__ == "__main__":
    main()
