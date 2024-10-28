from grin.Cache import Cache

def returning(index: int) -> tuple | int:
    """Returns the file_interpreter to the GOSUB location upon reaching a Return. Alternatively raises an error if a Return statement
    is reached and there was no previous GOSUB called."""
    if len(Cache.gosub_memory) == 0:
        print(
            f"ERROR ON LINE {Cache.current_line}: Return statement was reached when there was no GOSUB previously called")
        END = 1
        index -= 1
        return END, index
    else:
        index = Cache.gosub_memory[-1]
        del Cache.gosub_memory[-1]
        return index