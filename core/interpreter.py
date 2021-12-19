from sys import stdout, stderr
from core.error import print_error, Errors
from core.parser import TokenType


class Interpreter:
    def __init__(
        self,
        tree,
        cell_array_size: int,
        filepath: str = None,
        silent: bool = False,
        print_to_string: bool = False,
        exit_on_fail: bool = True,
        input_text: str = "",
    ) -> None:
        if print_to_string:
            stderr.write("WARNING: print_to_string has not been implemented\n\r")

        self.tree = tree
        self.filepath = filepath
        self.silent = silent
        # self.print_to_string = print_to_string
        self.exit_on_fail = exit_on_fail
        self.input_text = input_text

        self.CELL_ARRAY = [0] * cell_array_size
        self.CELL_POINTER = 0
        self.index = 0
        self.line = 0
        self.input_text_index = 0
        # self.output = ""

    def interpret(self) -> None | Errors:
        for node in self.tree:
            res = self.__interpret_node(node)
            if isinstance(res, Errors):
                return res

    def __interpret_node(self, node) -> None | Errors:
        if type(node) == list:
            tmp_ptr = self.CELL_POINTER
            while self.CELL_ARRAY[tmp_ptr]:
                # print(self.CELL_ARRAY[tmp_ptr])
                # print(node)
                for n in node:
                    self.__interpret_node(n)

        match node:
            case TokenType.ADD:
                self.CELL_ARRAY[self.CELL_POINTER] += 1
            case TokenType.MINUS:
                self.CELL_ARRAY[self.CELL_POINTER] -= 1
            case TokenType.CELL_SHIFT_LEFT:
                if self.CELL_POINTER <= 0:
                    if not self.silent:
                        print_error(
                            Errors.NEGATIVE_CELL_POINTER,
                            filepath=self.filepath,
                            index=(self.line, self.index),
                        )
                    if self.exit_on_fail:
                        exit(1)
                    else:
                        return Errors.NEGATIVE_CELL_POINTER
                self.CELL_POINTER -= 1

            case TokenType.CELL_SHIFT_RIGHT:
                if self.CELL_POINTER >= len(self.CELL_ARRAY) - 1:
                    if not self.silent:
                        print_error(
                            Errors.OVERFLOW_CELL_POINTER,
                            filepath=self.filepath,
                            index=(self.line, self.index),
                        )
                    if self.exit_on_fail:
                        exit(1)
                    else:
                        return Errors.OVERFLOW_CELL_POINTER
                self.CELL_POINTER += 1

            case TokenType.PRINT_CHAR:
                if self.CELL_ARRAY[self.CELL_POINTER] < 0:
                    if not self.silent:
                        print_error(
                            Errors.PRINT_NEGATIVE_CELL_VALUE,
                            filepath=self.filepath,
                            index=(self.line, self.index),
                        )
                    if self.exit_on_fail:
                        exit(1)
                    else:
                        return Errors.PRINT_NEGATIVE_CELL_VALUE
                if not self.silent:
                    stdout.write(chr(self.CELL_ARRAY[self.CELL_POINTER]))

            case TokenType.PRINT_NUM:
                if not self.silent:
                    stdout.write(str(self.CELL_ARRAY[self.CELL_POINTER]))

            case TokenType.PRINT_NEWLINE:
                if not self.silent:
                    stdout.write("\n")

            case TokenType.ALPHA_RESET:
                self.CELL_ARRAY[self.CELL_POINTER] = ord("a")

            case TokenType.UPPER_ALPHA_RESET:
                self.CELL_ARRAY[self.CELL_POINTER] = ord("A")

            case TokenType.HARD_RESET:
                self.CELL_ARRAY[self.CELL_POINTER] = 0

            case TokenType.VALUE_GET:
                if not self.input_text:
                    self.CELL_ARRAY[self.CELL_POINTER] = 0
                else:
                    self.CELL_ARRAY[self.CELL_POINTER] = ord(
                        self.input_text[self.input_text_index]
                    )
                    if self.input_text_index < len(self.input_text):
                        self.input_text_index += 1

            case TokenType.NEWLINE:
                self.line += 1
                self.index = -1

            case TokenType.WHITESPACE:
                pass  # handled below

        self.index += 1
