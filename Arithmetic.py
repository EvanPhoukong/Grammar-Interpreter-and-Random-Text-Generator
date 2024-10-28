from grin.Cache import Cache
import sys
from sys import exit
from grin import GrinToken, GrinTokenKind
class _Arithmetic:
    """This class handles arithmetic related Grin statements."""

    @staticmethod
    def add(var: GrinToken, value: GrinToken) -> bool:
        """Adds the values of two grin tokens together and stores them in a variable."""
        try:
            if var.text() in Cache.var_memory:
                if value.text() in Cache.var_memory:
                    Cache.var_memory[var.text()] += Cache.var_memory[value.text()]
                elif value.kind() is GrinTokenKind.IDENTIFIER:
                    Cache.var_memory[value.text()] = 0
                    Cache.var_memory[var.text()] += Cache.var_memory[value.text()]
                else:
                    Cache.var_memory[var.text()] += value.value()
                return False
            else:
                if value.text() in Cache.var_memory:
                    Cache.var_memory[var.text()] = Cache.var_memory[value.text()]
                elif value.kind() is GrinTokenKind.IDENTIFIER:
                    Cache.var_memory[value.text()] = 0
                    Cache.var_memory[var.text()] = Cache.var_memory[value.text()]
                else:
                    Cache.var_memory[var.text()] = value.value()
                return False
        except TypeError:
            print(f"ERROR ON LINE {Cache.current_line}: Addition of the variable and the value is not possible due to them being incompatible types.")
            return True

    @staticmethod
    def sub(var: GrinToken, value: GrinToken) -> bool:
        """Subtracts the values of two grin tokens together and stores them in a variable."""
        try:
            if var.text() in Cache.var_memory:
                if value.text() in Cache.var_memory:
                    Cache.var_memory[var.text()] -= Cache.var_memory[value.text()]
                elif value.kind() is GrinTokenKind.IDENTIFIER:
                    Cache.var_memory[value.text()] = 0
                else:
                    Cache.var_memory[var.text()] -= value.value()
                return False
            else:
                if value.text() in Cache.var_memory:
                    Cache.var_memory[var.text()] = -Cache.var_memory[value.text()]
                elif value.kind() is GrinTokenKind.IDENTIFIER:
                    Cache.var_memory[value.text()] = 0
                    Cache.var_memory[var.text()] = Cache.var_memory[value.text()]
                else:
                    Cache.var_memory[var.text()] = -value.value()
                return False
        except TypeError:
            print(f"ERROR ON LINE {Cache.current_line}: Subtraction of the variable and the value is not possible due to them being incompatible types.")
            return True

    @staticmethod
    def mult(var: GrinToken, value: GrinToken) -> bool:
        """Multiplies the values of two grin tokens together and stores them in a variable."""
        try:
            if var.text() in Cache.var_memory:
                if value.text() in Cache.var_memory:
                    Cache.var_memory[var.text()] *= Cache.var_memory[value.text()]
                elif value.kind() is GrinTokenKind.IDENTIFIER:
                    Cache.var_memory[value.text()] = 0
                    Cache.var_memory[var.text()] = 0
                else:
                    Cache.var_memory[var.text()] *= value.value()
                return False
            else:
                Cache.var_memory[var.text()] = 0
                if value.kind() is GrinTokenKind.IDENTIFIER and value.text() not in Cache.var_memory:
                    Cache.var_memory[value.text()] = 0
                return False
        except TypeError:
            print(f"ERROR ON LINE {Cache.current_line}: Multiplication of the variable and the value. This can be due to the fact that they are incompatible types, or that there was an attempt to multiply a string and negative integer.")
            return True

    @staticmethod
    def div(var: GrinToken, value: GrinToken) -> bool:
        """Divides the values of two grin tokens together and stores them in a variable."""
        try:
            if var.text() in Cache.var_memory:
                if value.text() in Cache.var_memory:
                    quotient = Cache.var_memory[var.text()] / Cache.var_memory[value.text()]
                    if type(Cache.var_memory[var.text()]) is float or type(Cache.var_memory[
                                                                               value.text()]) is float:  # Makes sure int divided by int results in an int
                        pass
                    else:
                        if int(quotient) == float(quotient):
                            quotient = int(quotient)
                elif value.kind() is GrinTokenKind.IDENTIFIER:
                    raise ZeroDivisionError
                else:
                    quotient = Cache.var_memory[var.text()] / value.value()
                    if type(Cache.var_memory[var.text()]) is float or type(value.value()) is float:
                        pass
                    else:
                        if int(quotient) == float(quotient):
                            quotient = int(quotient)
            else:
                if value.text() in Cache.var_memory:
                    quotient = 0
                    Cache.var_memory[var.text()] = 0
                    if type(Cache.var_memory[var.text()]) is float or type(Cache.var_memory[
                                                                               value.text()]) is float:  # Makes sure int divided by int results in an int
                        quotient = float(quotient)
                    else:
                        if int(quotient) == float(quotient):
                            quotient = int(quotient)
                elif value.kind() is GrinTokenKind.IDENTIFIER:
                    raise ZeroDivisionError
                else:
                    quotient = 0
                    Cache.var_memory[var.text()] = 0
                    if type(Cache.var_memory[var.text()]) is float or type(value.value()) is float:
                        pass
                    else:
                        if int(quotient) == float(quotient):
                            quotient = int(quotient)
            Cache.var_memory[var.text()] = quotient
            return False
        except ZeroDivisionError:
            print(f"ERROR ON LINE {Cache.current_line}: Dividing by zero is not possible.")
            return True
        except TypeError:
            print(f"ERROR ON LINE {Cache.current_line}: Division of the variable and the value is not possible due to them being incompatible types.")
            return True