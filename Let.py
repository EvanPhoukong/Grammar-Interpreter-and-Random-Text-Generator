from grin.Cache import Cache
from grin import GrinToken

class _Let:
    """This class contains the functionality to evaluate let statements."""
    @staticmethod
    def let(var: GrinToken, value: GrinToken) -> None:
        """Assigns a variable to the value of another GrinToken."""
        if value.text() in Cache.var_memory:
            Cache.var_memory[var.text()] = Cache.var_memory[value.text()]
        else:
            Cache.var_memory[var.text()] = value.value()