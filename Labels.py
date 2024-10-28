from grin.Cache import Cache
from grin.token import GrinTokenKind, GrinToken
def extract_labels(file: list[list[GrinToken]]) -> list[list[GrinToken]]:
    """Extracts labels and their corresponding locations and stores them in the cache"""
    file2 = []
    for index, line in enumerate(file[:]):
        if line[0].kind() is GrinTokenKind.IDENTIFIER:
            Cache.label_memory[line[0].text()] = line[0].location()
            #print('line', index, file[index])
            file2.append(line[2:])
        else:
            file2.append(line)
    #print('h', file2)
    return file2
