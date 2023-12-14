from typing import List

from aoc_api import get_input_chunks, submit


def fold_left(input_chunk: List[str], slice: int) -> List[str]:
    """
    'folds' a pattern over itself on the given fold line"""
    result: List[str] = []
    for line in input_chunk:
        left = line[:slice + 1][::-1]

        new_line = []
        for idx, char in enumerate(line):
            if len(left) <= idx < 2 * len(left):
                new_line.append(left[idx - len(left)])
            else:
                new_line.append(char)
        result.append(''.join(new_line))

    return result


def get_smudged_left_mirrors(input_chunk: List[str]) -> int:
    for slice in range(len(input_chunk)):
        folded = fold_left(input_chunk, slice)
        original = get_left_mirrors(input_chunk)
        left_mirrors = get_left_mirrors(folded)
        if is_off_by_one(input_chunk, folded) and left_mirrors != 0 and left_mirrors != original:
            return slice + 1
    return 0


def get_smudged_top_mirrors(input_chunk: List[str]) -> int:
    transposed = transpose(input_chunk)
    return get_smudged_left_mirrors(transposed)


def is_off_by_one(left: List[str], right: List[str]) -> bool:
    budget = 1
    for r in range(len(left)):
        for c in range(len(left[0])):
            if left[r][c] != right[r][c]:
                budget -= 1

    return budget == 0


def get_left_mirrors(input_chunk: List[str]) -> int:
    for slice in range(len(input_chunk[0]) - 1):
        valid_slice = True
        for line in input_chunk:
            left = line[:slice+1][::-1]
            right = line[slice+1:]

            small_dimension = min(len(left), len(right))
            if left[:small_dimension] != right[:small_dimension]:
                valid_slice = False
                break

        if valid_slice:
            return slice + 1

    return 0


def get_top_mirrors(input_chunk: List[str]) -> int:
    transposed = transpose(input_chunk)
    return get_left_mirrors(transposed)


def transpose(input_chunk: List[str]) -> List[str]:
    result = []
    for c in range(len(input_chunk[0])):
        line = []
        for r in range(len(input_chunk)):
            line.append(input_chunk[r][c])
        result.append(''.join(line))
    return result


def part1():
    input = get_input_chunks(13)

    answer = 0
    for chunk in input:
        answer += get_left_mirrors(chunk) + 100 * get_top_mirrors(chunk)

    submit(day=13, level=1, answer=answer)


def part2():
    input = get_input_chunks(13)

    answer = 0
    for chunk in input:
        answer += get_smudged_left_mirrors(chunk) + 100 * get_smudged_top_mirrors(chunk)

    submit(day=13, level=2, answer=answer)


part2()