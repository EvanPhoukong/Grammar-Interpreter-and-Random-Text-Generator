class Cache:
    """Acts as the cache/memory for the interpreter. Stores the current line, variables and their values, labels and their locations, and GOSUB locations"""
    current_line = 1
    var_memory = {}
    label_memory = {}
    gosub_memory = []