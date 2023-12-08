from dataclasses import dataclass
from typing import List, Set, Dict, Optional, Union, Any, Tuple

from aoc_api import get_input, submit
from intervals import Interval
from kernels import eight_kernel


def extract_full_number(r: int, c: int, input: List[str]) -> Tuple[int, int, int, int]:
    start = c
    while start >= 0 and input[r][start].isdigit():
        start -= 1

    start += 1

    end = c
    while end < len(input[r]) and input[r][end].isdigit():
        end += 1

    end -= 1

    return int(input[r][start:end+1]), r, start, end


def part1():
    input = get_input(3)

    numbers = set()
    for r in range(len(input)):
        for c in range(len(input[0])):
            char = input[r][c]
            if not char.isdigit() and char != ".":
                # this is a "symbol"
                neighbors = eight_kernel(r, c, x_bounds=Interval(0, len(input)), y_bounds=Interval(0, len(input)))
                for rr, cr in neighbors:
                    if input[rr][cr].isdigit():
                        # part of a number
                        number = extract_full_number(rr, cr, input)
                        numbers.add(number)

    answer = sum([number[0] for number in numbers])
    submit(day=3, level=1, answer=answer)


def part2():
    input = get_input(3)

    answer = 0
    for r in range(len(input)):
        for c in range(len(input[0])):
            char = input[r][c]
            if char == '*':
                # this is a "symbol"
                neighbors = eight_kernel(r, c, x_bounds=Interval(0, len(input)), y_bounds=Interval(0, len(input)))
                numbers = set()
                for rr, cr in neighbors:
                    if input[rr][cr].isdigit():
                        # part of a number
                        number = extract_full_number(rr, cr, input)
                        numbers.add(number[0])
                if len(numbers) == 2:
                    lnumbers = list(numbers)
                    answer += lnumbers[0] * lnumbers[1]

    submit(day=3, level=2, answer=answer)


part2()
