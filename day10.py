from typing import List, Set, Tuple

from aoc_api import get_input, submit


"""
CHECK THE HARDCODED THINGS FOR S BEFORE PICKING UP AGAIN
"""


CONNECTION_DELTAS = {
    '-': [(-1, 0), (1, 0)],
    '|': [(0, -1), (0, 1)],

    'F': [(0, 1), (1, 0)],
    'J': [(0, -1), (-1, 0)],
    '7': [(-1, 0), (0, 1)],
    'L': [(0, -1), (1, 0)]
}


def get_connections(input: List[str], x: int, y: int) -> List[Tuple[int, int]]:
    pipe = input[y][x]
    if pipe == 'S':
        # hardcoded by looking at the input

        # real input
        #return [(x, y-1), (x+1, y)]

        # fake input
        return [(x + 1, y), (x, y + 1)]

    return [(x + delta[0], y + delta[1]) for delta in CONNECTION_DELTAS[pipe]]


def find_starting_point(input: List[str]) -> Tuple[int, int]:
    for r, line in enumerate(input):
        for c, pipe in enumerate(line):
            if pipe == 'S':
                return c, r


def part1():
    input = get_input(10)

    starting_point = find_starting_point(input)

    visited = set()
    queue = [starting_point]
    while len(queue) != 0:
        head = queue.pop()
        next, previous = get_connections(input, head[0], head[1])
        if next not in visited:
            visited.add(next)
            queue.append(next)
        if previous not in visited:
            visited.add(previous)
            queue.append(previous)

    answer = len(visited) // 2

    submit(day=10, level=1, answer=answer, really=True)


def flood_fill(input: List[str], x: int, y: int) -> Set[Tuple[int, int]]:



def part2():
    input = get_input(10)
    input = [f'.{line}' for line in input]

    starting_point = find_starting_point(input)

    visited = set()
    queue = [starting_point]
    while len(queue) != 0:
        head = queue.pop()
        next, previous = get_connections(input, head[0], head[1])
        if next not in visited:
            visited.add(next)
            queue.append(next)
        if previous not in visited:
            visited.add(previous)
            queue.append(previous)

    answer = 0
    for r, line in enumerate(input):
        for c, pipe in enumerate(line):
            if c == 0:
                # this is the extra column
                continue
            if pipe != '.':
                continue

            crossing_count = 0
            for c1 in range(1, c):
                tx = line[c1-1:c1+1]

                # fake input
                tx = tx.replace('S', 'F')

                # real input
                # tx = tx.replace('S', 'L')

                if (c1, r) in visited and CROSSING_MAP[tx]:
                    crossing_count += 1
                    print((c1, r), tx, crossing_count)

            if crossing_count % 2 == 1:
                print(c, r, input[r][c], crossing_count)
                answer += 1

        break
    submit(day=10, level=2, answer=answer)


part2()
