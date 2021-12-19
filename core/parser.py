from enum import Enum, auto
from typing import List
from core.error import print_error, Errors

VALID_TOKENS = "+-><][%|^$?!/"


class TokenType(Enum):
    ADD = auto()                # +
    MINUS = auto()              # -
    CELL_SHIFT_LEFT = auto()    # <
    CELL_SHIFT_RIGHT = auto()   # >
    LOOP_START = auto()         # [
    LOOP_END = auto()           # ]
    PRINT_CHAR = auto()         # %
    PRINT_NUM = auto()          # |
    PRINT_NEWLINE = auto()      # ^
    ALPHA_RESET = auto()        # $
    UPPER_ALPHA_RESET = auto()  # ?
    HARD_RESET = auto()         # !
    VALUE_GET = auto()          # /
    NEWLINE = auto()
    WHITESPACE = auto()


def push(obj, lst, depth):
    while depth:
        lst = lst[-1]
        depth -= 1

    lst.append(obj)


def parse_brackets(tokens: List[TokenType]):
    groups = []
    depth = 0

    try:
        for char in tokens:
            if char == TokenType.LOOP_START:
                push([], groups, depth)
                depth += 1
            elif char == TokenType.LOOP_END:
                depth -= 1
            else:
                push(char, groups, depth)
    except IndexError:
        print_error(Errors.UNMATCHED_BRACKET)
        exit(1)

    if depth > 0:
        print_error(Errors.UNMATCHED_BRACKET)
        exit(1)
    else:
        return groups


def parse(source: str, filepath: str = None, exit_on_fail: bool = True) -> List | bool:
    if source.count("[") != source.count("]"):
        print_error(Errors.UNMATCHED_BRACKET)
        exit(1)

    tokens = []
    for line_i, line in enumerate(source.strip().splitlines()):
        for token_i, token in enumerate(line):
            match token:
                case "+":
                    tokens.append(TokenType.ADD)
                case "-":
                    tokens.append(TokenType.MINUS)
                case "<":
                    tokens.append(TokenType.CELL_SHIFT_LEFT)
                case ">":
                    tokens.append(TokenType.CELL_SHIFT_RIGHT)
                case "[":
                    tokens.append(TokenType.LOOP_START)
                case "]":
                    tokens.append(TokenType.LOOP_END)
                case "%":
                    tokens.append(TokenType.PRINT_CHAR)
                case "|":
                    tokens.append(TokenType.PRINT_NUM)
                case "^":
                    tokens.append(TokenType.PRINT_NEWLINE)
                case "!":
                    tokens.append(TokenType.HARD_RESET)
                case "$":
                    tokens.append(TokenType.ALPHA_RESET)
                case "?":
                    tokens.append(TokenType.UPPER_ALPHA_RESET)
                case "/":
                    tokens.append(TokenType.VALUE_GET)
                case " " | "\t":
                    tokens.append(TokenType.WHITESPACE)
                case ";":
                    break
                case _:
                    if exit_on_fail:
                        print_error(
                            Errors.UNKNOWN_TOKEN, line, filepath, (line_i, token_i)
                        )
                        exit(1)
                    return False
        tokens.append(TokenType.NEWLINE)

    return parse_brackets(tokens)
