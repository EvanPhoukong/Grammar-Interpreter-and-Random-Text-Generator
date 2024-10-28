from grin.Cache import Cache
from grin.token import GrinTokenKind
from grin import GrinToken

class _GOTO:
    """This class handled GOTO statements."""
    @staticmethod
    def start_jump_for_goto(line: list[GrinToken], index: int, file: list[list[GrinToken]]) -> None | tuple | int:
        """Initiates the GOTO jump to a line via label or jump size."""
        goto_here = line[1]
        if goto_here.kind() is GrinTokenKind.IDENTIFIER: #Extracts value from variable in GOTO statement
            if goto_here.text() in Cache.var_memory:
                goto_here = Cache.var_memory[goto_here.text()]
            else:
                Cache.var_memory[goto_here.text()] = 0
                goto_here = 0
        else:
            goto_here = goto_here.value()
        if type(goto_here) is int: #Handles GOTO when given jump size
            if len(line) <= 2:
                jump_to_index = _GOTO.goto_int(goto_here, index, len(file))
            else:
                jump_to_index = _GOTO.goto_int(goto_here, index, len(file), line[3], line[4],
                                                     line[5])
            if type(jump_to_index) is str:
                return None
            elif type(jump_to_index) is int:
                index += jump_to_index - 1
                return index
            else:
                END = 1
                index -= 1
                return END, index
        elif type(goto_here) is str: #Handles GOTO when given label
            if len(line) <= 2:
                jump_to_index = _GOTO.goto_label(goto_here, index)
            else:
                jump_to_index = _GOTO.goto_label(goto_here, index, line[3], line[4], line[5])
            if type(jump_to_index) is str:
                return None
            elif type(jump_to_index) is int:
                index = jump_to_index - 2
                return index
            else:
                END = 1
                index -= 1
                return END, index

    @staticmethod
    def goto_int(jump_to_index: int, index: int, file_size: list[list[GrinToken]], left = None, comparison = None, right = None) -> str | dict | int:
        """Retrieves the index by which to jump given the jump size."""
        if comparison is not None:
            jump_to_index = _GOTO.compare(jump_to_index, left, comparison, right)
            if type(jump_to_index) is str:
                return ''
            elif type(jump_to_index) is dict:
                return {}
        if jump_to_index == 0:
            print(f"ERROR ON LINE {Cache.current_line}: Executing a GOTO or GOSUB statement would result in an infinite loop.")
            return {}
        elif (jump_to_index + index) < 0 or (jump_to_index + index + 1) > file_size:
            print(f"ERROR ON LINE {Cache.current_line}: A GOTO or GOSUB statement attempted to jump to a line that does not exist.")
            return {}
        else:
            return jump_to_index

    @staticmethod
    def conversion(left: GrinToken, right: GrinToken) -> tuple:
        """Retrieves the values from the GrinTokens that are being compared in a conditional expression"""
        if left.kind() is GrinTokenKind.IDENTIFIER:
            if left.text() in Cache.var_memory:
                left = Cache.var_memory[left.text()]
            else:
                Cache.var_memory[left.text()] = 0
                left = 0
        else:
            left = left.value()
        if right.kind() is GrinTokenKind.IDENTIFIER:
            if right.text() in Cache.var_memory:
                right = Cache.var_memory[right.text()]
            else:
                Cache.var_memory[right.text()] = 0
                right = 0
        else:
            right = right.value()
        return left, right

    @staticmethod
    def compare(jump_to_index: int, left: GrinToken, comparison: GrinToken, right: GrinToken) -> str | dict | int:
        """Evaluates possible conditional expressions that may be attached to GOSUB or GOTO statements."""
        try:
            if type(jump_to_index) is str:
                jump_to_index = 0
            left, right = _GOTO.conversion(left, right)
            if type(left) != type(right):
                raise TypeError
            match comparison.kind(): #Compares the left object with the right object using the comparison operator specified.
                case GrinTokenKind.LESS_THAN:
                    if left < right:
                        return jump_to_index
                    else:
                        return ''
                case GrinTokenKind.LESS_THAN_OR_EQUAL:
                    if left <= right:
                        return jump_to_index
                    else:
                        return ''
                case GrinTokenKind.GREATER_THAN:
                    if left > right:
                        return jump_to_index
                    else:
                        return ''
                case GrinTokenKind.GREATER_THAN_OR_EQUAL:
                    if left >= right:
                        return jump_to_index
                    else:
                        return ''
                case GrinTokenKind.EQUAL:
                    if left == right:
                        return jump_to_index
                    else:
                        return ''
                case GrinTokenKind.NOT_EQUAL:
                    if left != right:
                        return jump_to_index
                    else:
                        return ''
        except TypeError:
            print(f"ERROR ON LINE {Cache.current_line}: The conditional expression in a GOSUB or GOTO statement cannot compare two objects due to them being different types.")
            return {}



    @staticmethod
    def goto_label(label: GrinToken, index, left = None, comparison = None, right = None) -> str | dict | int:
        """Retrieves the index by which to jump given the label."""
        if comparison is None:
            if label in Cache.label_memory:
                index2 = Cache.label_memory[label].line()
                if index2 == index + 1:
                    print(f"ERROR ON LINE {Cache.current_line}: Executing a GOTO or GOSUB statement would result in an infinite loop.")
                    return {}
                return index2
            else:
                print(f"ERROR ON LINE {Cache.current_line}: A GOTO or GOSUB statement attempted to jump to a line that does not exist.")
                return {}
        else:
            _ = _GOTO.compare(label, left, comparison, right)
            if type(_) is int:
                if label in Cache.label_memory:
                    index2 = Cache.label_memory[label].line()
                    if index2 == index + 1:
                        print(f"ERROR ON LINE {Cache.current_line}: Executing a GOTO or GOSUB statement would result in an infinite loop.")
                        return {}
                    return index2
                else:
                    print(
                        f"ERROR ON LINE {Cache.current_line}: A GOTO or GOSUB statement attempted to jump to a line that does not exist.")
                    return {}
            elif type(_) is dict:
                return {}
            return ''