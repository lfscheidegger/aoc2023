from functools import cache
from typing import Tuple, Set, Dict

from aoc_api import get_input, submit
from intervals import Interval
from kernels import four_kernel


def get_starting_position(input: Tuple[str]) -> Tuple[int, int]:
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            if char == 'S':
                return x, y

    assert False


@cache
def steps_from_steps(input: Tuple[str], current_plots: Tuple[Tuple[int, int]]) -> Tuple[Tuple[int, int]]:
    result: Set[Tuple[int, int]] = set()

    x_bounds = Interval(0, len(input[0]))
    y_bounds = Interval(0, len(input))

    for x, y in current_plots:
        for (n_x, n_y) in four_kernel(x, y, x_bounds, y_bounds):
            if input[n_y][n_x] == '#':
                continue
            result.add((n_x, n_y))

    return tuple(result)


def part1():
    input = tuple(get_input(day=21))

    current_plots: Tuple[Tuple[int, int]] = (get_starting_position(input), )
    steps = 0
    while steps < 64:
        current_plots = steps_from_steps(input, current_plots)
        steps += 1

    submit(day=21, level=1, answer=len(current_plots))


def part2():
    input = tuple(get_input(day=21))


part2()
