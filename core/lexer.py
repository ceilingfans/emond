from enum import Enum, auto
from typing import List, Tuple

from core.error import ErrorPrinter, Error


class TokenTypes(Enum):
    ADD = auto()
    MINUS = auto()
    CELL_SHIFT_LEFT = auto()
    CELL_SHIFT_RIGHT = auto()
    PRINT = auto()
    PRINT_NEWLINE = auto()
    HARD_RESET = auto()
    ALPHABET_RESET = auto()


def lex(source: str) -> Tuple[List[str], List[List[TokenTypes]]]:
    lexed: List[List[TokenTypes]] = []
    lines = source.splitlines()

    for line in lines:
        tokens: List[TokenTypes] = []
        comment_flag = False
        for index, token in enumerate(line):
            match token:
                case "+":
                    tokens.append(TokenTypes.ADD)
                case "-":
                    tokens.append(TokenTypes.MINUS)
                case "<":
                    tokens.append(TokenTypes.CELL_SHIFT_LEFT)
                case ">":
                    tokens.append(TokenTypes.CELL_SHIFT_RIGHT)
                case "%":
                    tokens.append(TokenTypes.PRINT)
                case "^":
                    tokens.append(TokenTypes.PRINT_NEWLINE)
                case "!":
                    tokens.append(TokenTypes.HARD_RESET)
                case "$":
                    tokens.append(TokenTypes.ALPHABET_RESET)
                case " " | "\t":
                    continue
                case ";":
                    lexed.append(tokens)
                    comment_flag = True
                    break
                case _:
                    ErrorPrinter.lexing_error(Error.UNKNOWN_TOKEN, token, line, f":{index}")

        if not comment_flag:
            lexed.append(tokens)

    return lines, lexed
