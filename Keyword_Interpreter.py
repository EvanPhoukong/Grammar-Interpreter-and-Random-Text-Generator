from grin.Cache import Cache
from grin.Let import _Let
from grin.Print import _Print
from grin.Input import _Input
from grin.Arithmetic import _Arithmetic
from grin.GOTO import _GOTO
from grin.GOSUB import _GOSUB
class Interpreter(_Let, _Print, _Input, _Arithmetic, _GOSUB):
    """A derived class that takes the functionality of _Let, _Print, _Input, _Arithmetic, and _GOSUB and combines it into one class for simplicity."""
    pass