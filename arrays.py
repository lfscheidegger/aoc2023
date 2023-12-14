from typing import List, Tuple, Union


def transpose_strings(input_chunk: Union[List[str], Tuple[str]]) -> Union[List[str], Tuple[str]]:
    """
    Returns a list of transposed strings given a list of strings. Examples:

    ['abc',
     'def']

    returns
    ['ad',
     'be',
     'cf']"""
    result = []
    for c in range(len(input_chunk[0])):
        line = []
        for r in range(len(input_chunk)):
            line.append(input_chunk[r][c])
        result.append(''.join(line))

    if isinstance(input_chunk, tuple):
        return tuple(result)
    else:
        return result


def reverse_strings(input_chunk: Union[List[str], Tuple[str]]) -> Union[List[str], Tuple[str]]:
    """
    Returns the given collection of strings, reversed."""
    result = [r[::-1] for r in input_chunk]
    if isinstance(input_chunk, tuple):
        return tuple(result)
    else:
        return result


def print_strings(input_chunk: Union[List[str], Tuple[str]]):
    for r in input_chunk:
        print(r)
    print()