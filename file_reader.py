from grin.parsing import parse
from grin import GrinToken
def get_file() -> list[GrinToken]:
    """Gets the Grin file as user input and turns it into a list of lists, where the nested lists represent lines and contain Grintokens."""
    grinfile = []
    line = 0
    while line != '.':
        line = input().strip()
        grinfile.append(line)
    for e, i in enumerate(grinfile[:]):
        if i == '.':
            grinfile[e] = 'END'
    tokengen = parse(grinfile)
    return [[token for token in line] for line in tokengen]