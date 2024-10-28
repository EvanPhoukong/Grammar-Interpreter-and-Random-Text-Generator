from grin.Cache import Cache
from grin import GrinTokenKind, GrinToken

class _Print:
    """This class contains the functionality to evaluate print statements."""
    @staticmethod
    def print_var(var:GrinToken) -> None:
        """Prints the value of a GrinToken."""
        if var.kind() is GrinTokenKind.IDENTIFIER:
            if var.text() in Cache.var_memory:
                print(Cache.var_memory[var.text()])
            else:
                Cache.var_memory[var.text()] = 0
                print("0")
        else:
            print(var.value())
