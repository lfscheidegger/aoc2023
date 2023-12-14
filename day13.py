from typing import List, Tuple

from arrays import transpose_strings
from aoc_api import get_input_chunks, submit


def fold_left(input_chunk: List[str], slice: int) -> List[str]:
    """
    'folds' a pattern over itself on the given fold line"""
    result: List[str] = []
    for line in input_chunk:
        new_line = []
        for idx in range(len(line)):
            if idx > slice:
                # past the fold line
                new_line.append(line[idx])
                continue

            target = 2 * slice + 1 - idx
            if target >= len(line):
                # aiming too far
                new_line.append(line[idx])
            else:
                new_line.append(line[target])

        result.append(''.join(new_line))

    return result


def get_smudged_left_mirrors(input_chunk: List[str], old_left: int) -> Tuple[int, List[str]]:
    for slice in range(len(input_chunk[0])):
        folded = fold_left(input_chunk, slice)
        off_by_one = is_off_by_one(input_chunk, folded)

        if off_by_one and slice + 1 != old_left:
            return slice + 1, folded
    return 0, input_chunk


def get_smudged_top_mirrors(input_chunk: List[str], old_top: int) -> Tuple[int, List[str]]:
    transposed = transpose_strings(input_chunk)
    slices, result = get_smudged_left_mirrors(transposed, old_top)
    return slices, transpose_strings(result)


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
    transposed = transpose_strings(input_chunk)
    return get_left_mirrors(transposed)


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
        old_top_slices = get_top_mirrors(chunk)
        old_left_slices = get_left_mirrors(chunk)

        new_top_slices, new_top = get_smudged_top_mirrors(chunk, old_top_slices)
        new_left_slices, new_left = get_smudged_left_mirrors(chunk, old_left_slices)

        assert old_top_slices * old_left_slices == 0
        assert new_top_slices * new_left_slices == 0

        assert new_top_slices == 0 or new_top_slices != old_top_slices
        assert new_left_slices == 0 or new_left_slices != old_left_slices

        assert old_top_slices + old_left_slices != 0
        assert new_top_slices + new_left_slices != 0

        new_score = new_left_slices + 100 * new_top_slices

        answer += new_score

    submit(day=13, level=2, answer=answer)


part2()
