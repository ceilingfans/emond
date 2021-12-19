from enum import Enum, auto
from typing import Tuple, Optional, List
from sys import stderr


class Errors(Enum):
    #  lexing errors
    UNKNOWN_TOKEN = auto()
    UNMATCHED_BRACKET = auto()

    #  runtime errors
    OVERFLOW_CELL_POINTER = auto()
    NEGATIVE_CELL_POINTER = auto()
    PRINT_NEGATIVE_CELL_VALUE = auto()


def __error_snippet(line: str, index: int) -> List[str]:
    start = index - 4
    end = index + 6

    if start < 0:
        start = 0
    if end >= len(line):
        end = len(line)

    source = f"at {line[start:end]}"
    arrow = f"   {' ' * (index - start)}^"

    return [source, arrow]


def print_error(
    error: Errors | str,
    line: str = None,
    filepath: str = None,
    index: Tuple[Optional[int], int] = None,
) -> None:
    if index is not None and line:
        if index[1] >= len(line):
            raise IndexError(
                "index provided is greater than or equal to length of line"
            )

    match error:
        case Errors.UNKNOWN_TOKEN:
            stderr.write(f"SyntaxError[{error.name}]: Unknown token\n\r")
        case Errors.UNMATCHED_BRACKET:
            stderr.write(f"SyntaxError[{error.name}]: Unmatched Bracket\n\r")
        case Errors.OVERFLOW_CELL_POINTER:
            stderr.write(
                f"ValueError[{error.name}]: Cell pointers cannot be larger than the cell array length\n\r"
            )
        case Errors.NEGATIVE_CELL_POINTER:
            stderr.write(
                f"ValueError[{error.name}]: Cell pointers cannot be negative\n\r"
            )
        case Errors.PRINT_NEGATIVE_CELL_VALUE:
            stderr.write(
                f"ValueError[{error.name}]: The print character operator cannot be used on negative cell values\n\r"
            )
        case _:
            if type(error) == str:
                stderr.write(error)
            else:
                stderr.write(
                    "InternalError: An invalid error was provided\n\r"
                )  # unexpected behaviour, therefore
                exit(-1)  # exit with -1

    stderr.write(f"    at <{filepath or 'source'}>")
    if index is None:
        stderr.write("\n\r")
        return
    if index[0] is None:
        stderr.write(f", position {index[1]+1}\n\r")
    else:
        stderr.write(f":{index[0]+1}:{index[1]+1}\n\r")

    if line:
        for s in __error_snippet(line, index[1]):
            stderr.write(f"    {s}\n\r")
