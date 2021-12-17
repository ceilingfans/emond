from typing import List
from sys import stdout, stderr

from core.error import ErrorPrinter, Error
from core.lexer import TokenTypes


def interpret(source: List[str], lines: List[List[TokenTypes]], cell_array_size: int) -> None:
    CELL_ARRAY = [0]*cell_array_size
    CELL_POINTER = 0
    for line_i, line in enumerate(lines):
        for token_i, token in enumerate(line):
            match token:
                case TokenTypes.ADD:
                    CELL_ARRAY[CELL_POINTER] += 1

                case TokenTypes.MINUS:
                    CELL_ARRAY[CELL_POINTER] -= 1

                case TokenTypes.CELL_SHIFT_RIGHT:
                    if CELL_POINTER >= cell_array_size:
                        ErrorPrinter.runtime_error(Error.OVERFLOW_CELL, source[line_i], f"{line_i+1}:{token_i}")
                    CELL_POINTER += 1

                case TokenTypes.CELL_SHIFT_LEFT:
                    if CELL_POINTER <= 0:
                        ErrorPrinter.runtime_error(Error.NEGATIVE_CELL, source[line_i], f"{line_i+1}:{token_i}")
                    CELL_POINTER -= 1

                case TokenTypes.ALPHABET_RESET:
                    CELL_ARRAY[CELL_POINTER] = ord('a')

                case TokenTypes.HARD_RESET:
                    CELL_ARRAY[CELL_POINTER] = 0

                case TokenTypes.PRINT_NEWLINE:
                    stdout.write("\n")

                case TokenTypes.PRINT:
                    if CELL_ARRAY[CELL_POINTER] < 0:
                        ErrorPrinter.runtime_error(Error.NEGATIVE_VALUE_PRINT, source[line_i], f"{line_i+1}:{token_i }")
                    stdout.write(chr(CELL_ARRAY[CELL_POINTER]))

                case _:
                    stderr.write("InternalError: Invalid token type provided by the lexer\n")
                    exit(-1)
