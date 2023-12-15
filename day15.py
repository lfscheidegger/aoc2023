from typing import Dict, List

from aoc_api import get_input, submit


def my_hash(string: str) -> int:
    hash = 0
    for char in string:
        hash += ord(char)
        hash *= 17
        hash %= 256
    return hash


def part1():
    input = get_input(15)

    input = ''.join(input).replace('\n', '')
    individuals = input.split(',')

    answer = 0
    for string in individuals:
        answer += my_hash(string)

    submit(day=15, level=1, answer=answer)


def part2():
    input = get_input(15)

    input = ''.join(input).replace('\n', '')
    individuals = input.split(',')
    boxes: Dict[int, List[str]] = {}

    for string in individuals:
        if '-' in string:
            label = string[:-1]
            box = my_hash(label)
            if box in boxes:
                # removing the lens
                boxes[box] = [lens for lens in boxes[box] if lens.split(' ')[0] != label]
        else:
            assert '=' in string
            label, focal_length = string.split("=")
            focal_length = int(focal_length)
            box = my_hash(label)
            if box not in boxes:
                boxes[box] = []

            found = False
            for i, lens in enumerate(boxes[box]):
                if lens.split()[0] == label:
                    boxes[box][i] = f'{label} {focal_length}'
                    found = True

            if not found:
                boxes[box].append(f'{label} {focal_length}')

    answer = 0
    for box in boxes:
        lenses = boxes[box]
        for i, lens in enumerate(lenses):
            answer += (box + 1) * (i + 1) * int(lens.split(' ')[1])

    submit(day=15, level=2, answer=answer)


part2()