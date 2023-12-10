from aoc_api import get_input, submit

from typing import List


def extrapolate_line(line: List[int]) -> int:
    if all([x == 0 for x in line]):
        return 0

    differences = [x - y for x, y in zip(line[1:], line)]

    return line[-1] + extrapolate_line(differences)


def extrapolate_back(line: List[int]) -> int:
    if all([x == 0 for x in line]):
        return 0

    differences = [x - y for x, y in zip(line[1:], line)]

    return line[0] - extrapolate_back(differences)

def part1():
    input = get_input(9)

    answer = 0
    for line in input:
        line = [int(x) for x in line.split()]
        answer += extrapolate_line(line)

    submit(day=9, level=1, answer=answer, really=True)


def part2():
    input = get_input(9)

    answer = 0
    for line in input:
        line = [int(x) for x in line.split()]
        answer += extrapolate_back(line)

    submit(day=9, level=2, answer=answer, really=True)


part2()
