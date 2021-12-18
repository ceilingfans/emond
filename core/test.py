from os import path

from core.lexer import *
from core.interpreter import *


def run_test(filepath: str | bytes) -> None | Error | str:
    if not path.exists(filepath):
        return "INVALID_FILE_PATH"

    src = open(filepath).read().strip()
    lex_o = lex(src, exit_on_fail=False)
    if type(lex_o) != tuple:
        return lex_o

    interpret_o = interpret(lex_o[0], lex_o[1], 1000, exit_on_fail=False, silent=True)
    if interpret_o:
        return interpret_o
