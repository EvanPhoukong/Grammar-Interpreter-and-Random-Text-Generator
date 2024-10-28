from grin import GrinTokenKind
from grin.Cache import Cache
from grin.Keyword_Interpreter import Interpreter
from grin.Return import returning
from grin import GrinToken

def file_interpreter(file: list[list[GrinToken]]) -> None:
    """Iterates through each line of the Grin File and evaluates it."""
    index = 0
    END = 0
    Cache.current_line = 1
    while END != 1:
        line = file[index]
        Cache.current_line = index + 1
        var_index = 1
        value_index = 2
        for token in line: #Identifies what kind of Grin statement the line is
            match token.kind():
                case GrinTokenKind.LET:
                    Interpreter.let(line[var_index], line[value_index])
                    break
                case GrinTokenKind.PRINT:
                    Interpreter.print_var(line[var_index])
                    break
                case GrinTokenKind.INNUM:
                    if Interpreter.innum(line[var_index]):
                        pass
                    else:
                        END = 1
                        index -= 1
                    break
                case GrinTokenKind.INSTR:
                    Interpreter.instr(line[var_index])
                    break
                case GrinTokenKind.ADD:
                    if Interpreter.add(line[var_index], line[value_index]):
                        END = 1
                        index -= 1
                    break
                case GrinTokenKind.SUB:
                    if Interpreter.sub(line[var_index], line[value_index]):
                        END = 1
                        index -= 1
                    break
                case GrinTokenKind.MULT:
                    if Interpreter.mult(line[var_index], line[value_index]):
                        END = 1
                        index -= 1
                    break
                case GrinTokenKind.DIV:
                    if Interpreter.div(line[var_index], line[value_index]):
                        END = 1
                        index -= 1
                    break
                case GrinTokenKind.GOTO:
                    _ = Interpreter.start_jump_for_goto(line, index, file)
                    if _ is None:
                        pass
                    elif type(_) is tuple:
                        END, index = _
                    elif type(_) is int:
                        index = _
                    break
                case GrinTokenKind.GOSUB:
                    _ = Interpreter.start_jump_for_gosub(line, index, file)
                    if _ is None:
                        pass
                    elif type(_) is tuple:
                        END, index = _
                    elif type(_) is int:
                        index = _
                    break
                case GrinTokenKind.RETURN:
                    _ = returning(index)
                    if type(_) is tuple:
                        END, index = _
                    elif type(_) is int:
                        index = _
                    break
                case GrinTokenKind.END:
                    END = 1
                    index -= 1
                    break
        index += 1
        Cache.current_line += 1
    #print(Cache.current_line, Cache.var_memory, Cache.label_memory, Cache.gosub_memory)