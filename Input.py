from grin.Cache import Cache
from grin import GrinToken
class _Input:
    """This class provided the functionality to retrieve input from the user."""
    @staticmethod
    def innum(var: GrinToken) -> bool:
        """Retrieves a numeric input from the user."""
        try:
            number = input().strip()
            if "." in number:
                number = float(number)
            else:
                number = int(number)
            Cache.var_memory[var.text()] = number
            return True
        except ValueError:
            print("ERROR: INNUM only takes integer or float(numeric values) as input.")
            return False


    @staticmethod
    def instr(var: GrinToken) -> None:
        """Retrieves any input from the user."""
        Cache.var_memory[var.text()] = input()