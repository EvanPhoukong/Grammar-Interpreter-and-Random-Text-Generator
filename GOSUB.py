from grin.Cache import Cache
from grin.GOTO import _GOTO
from grin import GrinToken, GrinTokenKind

class _GOSUB(_GOTO):
    """The _GOTO class but with its unique method for initiating the jump to a line."""
    @staticmethod
    def start_jump_for_gosub(line: list[GrinToken], index: int, file: list[list[GrinToken]]) -> None | tuple | int:
        """Initiates the GOSUB jump to a line via label or jump size. Stores the line to return to in the Cache"""
        goto_here = line[1]
        if goto_here.kind() is GrinTokenKind.IDENTIFIER: #Extracts value from variable in GOSUB statement
            if goto_here.text() in Cache.var_memory:
                goto_here = Cache.var_memory[goto_here.text()]
            else:
                Cache.var_memory[goto_here.text()] = 0
                goto_here = 0
        else:
            goto_here = goto_here.value()
        if type(goto_here) is int: #Handles GOSUB when given jump size
            if len(line) <= 2:
                jump_to_index = _GOTO.goto_int(goto_here, index, len(file))
            else:
                jump_to_index = _GOTO.goto_int(goto_here, index, len(file), line[3], line[4],
                                                     line[5])
            if type(jump_to_index) is str:
                return None
            elif type(jump_to_index) is int:
                Cache.gosub_memory.append(index)
                index += jump_to_index - 1
                return index
            else:
                END = 1
                index -= 1
                return END, index
        elif type(goto_here) is str: #Handles GOSUB when given label
            if len(line) <= 2:
                jump_to_index = _GOTO.goto_label(goto_here, index)
            else:
                jump_to_index = _GOTO.goto_label(goto_here, index, line[3], line[4], line[5])
            if type(jump_to_index) is str:
                return None
            elif type(jump_to_index) is int:
                Cache.gosub_memory.append(index)
                index = jump_to_index - 2
                return index
            else:
                END = 1
                index -= 1
                return END, index