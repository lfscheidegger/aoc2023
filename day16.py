from typing import List, Tuple, Set

from aoc_api import get_input, submit
from intervals import Interval


DIRECTION_MAP = {
    'right': '>',
    'up': '^',
    'down': 'v',
    'left': '<'
}


OFFSET_MAP = {
    ('right', '.'): [((1, 0), 'right')],
    ('right', '-'): [((1, 0), 'right')],
    ('right', '|'): [((0, -1), 'up'), ((0, 1), 'down')],
    ('right', '/'): [((0, -1), 'up')],
    ('right', '\\'): [((0, 1), 'down')],

    ('left', '.'): [((-1, 0), 'left')],
    ('left', '-'): [((-1, 0), 'left')],
    ('left', '|'): [((0, -1), 'up'), ((0, 1), 'down')],
    ('left', '/'): [((0, 1), 'down')],
    ('left', '\\'): [((0, -1), 'up')],

    ('up', '.'): [((0, -1), 'up')],
    ('up', '-'): [((-1, 0), 'left'), ((1, 0), 'right')],
    ('up', '|'): [((0, -1), 'up')],
    ('up', '/'): [((1, 0), 'right')],
    ('up', '\\'): [((-1, 0), 'left')],

    ('down', '.'): [((0, 1), 'down')],
    ('down', '-'): [((-1, 0), 'left'), ((1, 0), 'right')],
    ('down', '|'): [((0, 1), 'down')],
    ('down', '/'): [((-1, 0), 'left')],
    ('down', '\\'): [((1, 0), 'right')],
}


def process_beam(
        position: Tuple[int, int],
        direction: str,
        input: List[str],
        output: List[List[str]]):

    x_bounds = Interval(0, len(input[0]))
    y_bounds = Interval(0, len(input))

    other_beams: Set[Tuple[Tuple[int, int], str]] = set()

    while True:
        if not x_bounds.contains(position[0]) or not y_bounds.contains(position[1]):
            break

        cell = input[position[1]][position[0]]

        if output[position[1]][position[0]] == 'S':
            # we already split here
            break

        output[position[1]][position[0]] = DIRECTION_MAP[direction]
        offsets = OFFSET_MAP[(direction, cell)]

        next = offsets[0]

        old_position = position
        position = (position[0] + next[0][0], position[1] + next[0][1])
        direction = next[1]

        if len(offsets) != 1:
            # there's a split
            output[old_position[1]][old_position[0]] = 'S'

            split = offsets[1]
            split_position = (old_position[0] + split[0][0], old_position[1] + split[0][1])
            split_direction = split[1]
            other_beams.add((split_position, split_direction))

    for split in other_beams:
        process_beam(split[0], split[1], input, output)


def count_illuminated(output: List[List[str]]) -> int:
    answer = 0
    for row in output:
        for char in row:
            if char != '.':
                answer += 1

    return answer


def part1():
    input = get_input(16)

    output = [['.'] * len(input[0]) for _ in range(len(input))]

    process_beam((0, 0), 'right', input, output)

    answer = count_illuminated(output)

    submit(day=16, level=1, answer=answer)


def part2():
    input = get_input(16)

    answer = 0
    for y in range(len(input)):
        output = [['.'] * len(input[0]) for _ in range(len(input))]
        process_beam((0, y), 'right', input, output)
        answer = max(answer, count_illuminated(output))

        output = [['.'] * len(input[0]) for _ in range(len(input))]
        process_beam((len(input[0]) - 1, y), 'left', input, output)
        answer = max(answer, count_illuminated(output))

    for x in range(len(input[0])):
        output = [['.'] * len(input[0]) for _ in range(len(input))]
        process_beam((x, 0), 'down', input, output)
        answer = max(answer, count_illuminated(output))

        output = [['.'] * len(input[0]) for _ in range(len(input))]
        process_beam((x, len(input) - 1), 'up', input, output)
        answer = max(answer, count_illuminated(output))

    submit(day=16, level=2, answer=answer)


part2()