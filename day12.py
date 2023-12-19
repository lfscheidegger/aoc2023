from functools import cache
from typing import Tuple

from aoc_api import get_input, submit


def get_combinations(row: str) -> int:
    left, right = row.split()
    damaged_counts = tuple(int(x) for x in right.split(","))

    return count_arrangements(left + '.', damaged_counts, 0)


@cache
def count_arrangements(springs: str, groups: Tuple[int], current_group_size: int) -> int:
    if springs == '':
        return int(len(groups) == 0 and current_group_size == 0)

    result = 0
    for option in (['.', '#'] if springs[0] == '?' else springs[0]):
        if option == '#':
            result += count_arrangements(springs[1:], groups, current_group_size + 1)
        else:
            assert option == '.'
            if current_group_size != 0:
                if len(groups) != 0 and groups[0] == current_group_size:
                    # Closing an existing group
                    result += count_arrangements(springs[1:], groups[1:], 0)
            else:
                # Noop, just go to next character
                result += count_arrangements(springs[1:], groups, 0)

    return result


def expand_line(line: str, amount: int) -> str:
    if amount == 1:
        return line

    left, right = line.split()

    left = '?'.join([left.strip() for _ in range(amount)])
    right = ','.join([right.strip() for _ in range(amount)])

    return f'{left} {right}'


def part1():
    input = get_input(12)

    answer = 0
    for line in input:
        answer += get_combinations(line)

    submit(day=12, level=1, answer=answer)


def part2():
    input = get_input(12)

    answer = 0
    for line in input:
        answer += get_combinations(expand_line(line, 5))

    submit(day=12, level=2, answer=answer)


if __name__ == '__main__':
    part2()
