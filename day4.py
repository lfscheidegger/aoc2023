from dataclasses import dataclass
from typing import List, Set, Dict, Optional, Union, Any, Tuple

from aoc_api import get_input, submit


def part1():
    input = get_input(4)

    answer = 0

    for idx, line in enumerate(input):
        left, right = line.split("|")
        left = left.split(":")[1]
        left = set(int(x.strip()) for x in left.split())
        right = set(int(x.strip()) for x in right.split())

        intersect = len(left.intersection(right))
        if intersect == 0:
            continue

        answer += 2**(intersect - 1)

    submit(day=4, level=2, answer=answer, really=True)


def part2():
    input = get_input(4)

    counts = [1 for _ in range(len(input))]

    for idx, line in enumerate(input):
        left, right = line.split("|")
        left = left.split(":")[1]
        left = set(int(x.strip()) for x in left.split())
        right = set(int(x.strip()) for x in right.split())

        intersect = len(left.intersection(right))
        if intersect == 0:
            continue

        for offset in range(intersect):
            counts[idx + offset + 1] += counts[idx]

    submit(day=4, level=2, answer=sum(counts), really=True)


part2()
