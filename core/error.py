from enum import Enum, auto
from sys import stderr

class Error(Enum):
    # lexing related errors
    UNKNOWN_TOKEN = auto()

    # runtime related errors
    NEGATIVE_CELL = auto()
    OVERFLOW_CELL = auto()
    NEGATIVE_VALUE_PRINT = auto()


class ErrorPrinter:
    @staticmethod
    def lexing_error(error: Error, current_token_literal: str, line: str, index: str) -> None:
        match error:
            case Error.UNKNOWN_TOKEN:
                stderr.write(f"SyntaxError[{error.name}]: Unknown Token -> {current_token_literal}\n\r")
            case _:
                stderr.write(f"InternalError: An unexpected error has occured -> Invalid lexing error type\n\r")
                exit(-1)

        error_message = f"    at <source_file>:{index}\n\r" \
                        f"    at {ErrorPrinter.__get_snippet(line, int(index.split(':')[1]))}\n\r"
        stderr.write(error_message)
        exit(1)

    @staticmethod
    def runtime_error(error: Error, line: str, index: str):
        match error:
            case Error.NEGATIVE_CELL:
                stderr.write(f"ValueError[{error.name}]: Cell pointers may not be negative\n\r")
            case Error.OVERFLOW_CELL:
                stderr.write(f"ValueError[{error.name}]: Cell pointer overloaded\n\r")
            case Error.NEGATIVE_VALUE_PRINT:
                stderr.write(f"ValueError[{error.name}]: The print operator may not be used on a negative value\n\r")
            case _:
                stderr.write(f"InternalError: An unexpected error has occured -> Invalid runtime error type\n\r")
                exit(-1)

        error_message = f"\tat <source_file>:{index}\n\r" \
                        f"\t   at {ErrorPrinter.__get_snippet(line, int(index.split(':')[1]))}\n\r"
        stderr.write(error_message)
        exit(1)

    @staticmethod
    def __get_snippet(line: str, index: int):
        if len(line) == 1:
            return f"{line}\n\r" \
                   f"       ^"

        start = index - 4
        end = index + 6

        start_extend = True
        end_extend = True

        if start < 0:
            start = 0
            start_extend = False
        if end >= len(line):
            end = len(line)-1
            end_extend = False

        return f"{line[start:end]}\n\r" \
               f"       {' '*(index-start)}^"
