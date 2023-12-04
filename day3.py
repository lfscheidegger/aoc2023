from dataclasses import dataclass
from typing import List, Set, Dict, Optional, Union, Any, Tuple

from aoc_api import get_input, submit


def neighboring_coords(r: int, c: int, height: int, width: int) -> List[Tuple[int, int]]:
    result = [
        (r+1, c),
        (r+1, c+1),
        (r, c+1),
        (r-1, c+1),
        (r-1, c),
        (r-1, c-1),
        (r, c-1),
        (r+1, c-1),
    ]

    return list(filter(lambda coord: 0 <= coord[0] < height and 0 <= coord[1] < width, result))


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
                neighbors = neighboring_coords(r, c, len(input), len(input[0]))
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
                neighbors = neighboring_coords(r, c, len(input), len(input[0]))
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
