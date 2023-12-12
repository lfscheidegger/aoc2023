from typing import List, Set, Tuple

from aoc_api import get_input, submit
from functools import lru_cache
from intervals import Interval
from kernels import four_kernel


@lru_cache()
def find_starting_point(input: Tuple[str]) -> Tuple[int, int]:
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            if char == 'S':
                return x, y

    raise


CONNECTIONS_MAP = {
    '-': ['left', 'right'],
    '|': ['up', 'down'],
    'F': ['right', 'down'],
    'L': ['right', 'up'],
    'J': ['left', 'up'],
    '7': ['left', 'down'],
    '.': []
}


@lru_cache()
def find_start_mapping(input: Tuple[str]) -> str:
    """
    Returns the corrected pipe value for the starting point of the maze."""
    starting_point = find_starting_point(input)

    neighbor_coords = four_kernel(
        starting_point[0],
        starting_point[1],
        x_bounds=Interval(0, len(input[0])),
        y_bounds=Interval(0, len(input)))

    neighbors = {
        (coord[0] - starting_point[0], coord[1] - starting_point[1]): input[coord[1]][coord[0]]
        for coord
        in neighbor_coords
    }

    candidates = ['-', '|', 'F', 'L', 'J', '7']
    for offset in neighbors:
        neighbor = offset[0] + starting_point[0], offset[1] + starting_point[1]
        if offset == (1, 0) and 'left' in CONNECTIONS_MAP[input[neighbor[1]][neighbor[0]]]:
            candidates = [candidate for candidate in candidates if 'right' in CONNECTIONS_MAP[candidate]]

        if offset == (-1, 0) and 'right' in CONNECTIONS_MAP[input[neighbor[1]][neighbor[0]]]:
            candidates = [candidate for candidate in candidates if 'left' in CONNECTIONS_MAP[candidate]]

        if offset == (0, 1) and 'up' in CONNECTIONS_MAP[input[neighbor[1]][neighbor[0]]]:
            candidates = [candidate for candidate in candidates if 'down' in CONNECTIONS_MAP[candidate]]

        if offset == (0, -1) and 'down' in CONNECTIONS_MAP[input[neighbor[1]][neighbor[0]]]:
            candidates = [candidate for candidate in candidates if 'up' in CONNECTIONS_MAP[candidate]]

    candidates = list(candidates)
    assert len(candidates) == 1

    return candidates[0]


def expand_input(input: Tuple[str]) -> Tuple[str]:
    """
    Expands the maze adding dots and lengthening pipes horizontally and vertically."""

    expanded_vertically: List[str] = []
    # Expand horizontally first
    for line, next_line in zip(input, input[1:]):
        expanded_vertically.append(line)
        expanded = ''
        for idx, _ in enumerate(line):
            char = line[idx] if line[idx] != 'S' else find_start_mapping(input)
            next_char = next_line[idx] if next_line[idx] != 'S' else find_start_mapping(input)

            connections = CONNECTIONS_MAP[char]
            next_connections = CONNECTIONS_MAP[next_char]

            if 'down' in connections and 'up' in next_connections:
                expanded += '|'
            else:
                expanded += '.'
        assert len(expanded) == len(line)
        expanded_vertically.append(expanded)

    expanded_vertically.append(input[-1])

    # Now expand vertically
    result: List[str] = []
    for row, _ in enumerate(expanded_vertically):
        expanded = ''
        for char, next_char in zip(expanded_vertically[row], expanded_vertically[row][1:]):
            expanded += char

            char = char if char != 'S' else find_start_mapping(input)
            next_char = next_char if next_char != 'S' else find_start_mapping(input)

            connections = CONNECTIONS_MAP[char]
            next_connections = CONNECTIONS_MAP[next_char]

            if 'right' in connections and 'left' in next_connections:
                expanded += '-'
            else:
                expanded += '.'
        expanded += expanded_vertically[row][-1]
        result.append(expanded)

    return tuple(result)


@lru_cache()
def flood_fill(input: Tuple[str], starting_point: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """
    Returns the set of flood-filled points given a starting empty point."""
    assert input[starting_point[1]][starting_point[0]] == '.'

    result: Set[Tuple[int, int]] = {starting_point}

    queue = [starting_point]
    while len(queue) > 0:
        head = queue.pop()

        for neighbor in [x for x in four_kernel(
            head[0],
            head[1],
            x_bounds=Interval(0, len(input[0])),
            y_bounds=Interval(0, len(input))) if x not in result and input[x[1]][x[0]] == '.']:
            result.add(neighbor)
            queue.append(neighbor)

    return result


def pipe_kernel(input: Tuple[str], pipe_coords: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Returns the neighboring kernel of a given pipe type."""
    pipe = input[pipe_coords[1]][pipe_coords[0]]

    assert pipe != '.'
    if pipe == 'S':
        pipe = find_start_mapping(input)

    offsets = {
        '|': [(0, -1), (0, 1)],
        '-': [(-1, 0), (1, 0)],
        'F': [(1, 0), (0, 1)],
        '7': [(-1, 0), (0, 1)],
        'J': [(-1, 0), (0, -1)],
        'L': [(1, 0), (0, -1)]
    }

    return [(offset[0] + pipe_coords[0], offset[1] + pipe_coords[1]) for offset in offsets[pipe]]


@lru_cache()
def pipe_path(input: Tuple[str], starting_point: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """
    Returns the set of points forming a pipeline or loop given a starting pipe point."""
    assert input[starting_point[1]][starting_point[0]] != '.'

    result: Set[Tuple[int, int]] = {starting_point}

    queue = [starting_point]
    while len(queue) > 0:
        head = queue.pop()

        for neighbor in [x for x in pipe_kernel(input, head) if x not in result]:
            result.add(neighbor)
            queue.append(neighbor)

    return result


@lru_cache()
def is_valid_fill(input: Tuple[str], starting_point: Tuple[int, int]) -> bool:
    """
    Returns true iff the flood fill starting in the given starting point is valid.

    A valid flood fill is adjacent to the pipe path that contains the starting point, and does not touch the outside."""
    assert input[starting_point[1]][starting_point[0]] == '.'

    fill = flood_fill(input, starting_point)
    for point in fill:
        # touches the outside
        if point[0] == 0 or point[0] == len(input[0]) - 1 or point[1] == 0 or point[1] == len(input) - 1:
            return False

        neighbors = four_kernel(
            point[0], point[1],
            x_bounds=Interval(0, len(input[0])), y_bounds=Interval(0, len(input)))

        for neighbor in neighbors:
            if input[neighbor[1]][neighbor[0]] == '.':
                continue
            path = pipe_path(input, neighbor)
            if 'S' in [input[p[1]][p[0]] for p in path]:
                return True

    return False


def part2():
    input = tuple(get_input(10))
    input = expand_input(input)

    #for l in expanded_input:
    #    print(l)
    #print(expanded_input)
    #print(flood_fill(expanded_input, (0, 0)))
    #print(pipe_path(expanded_input, find_starting_point(expanded_input)))

    for y, line in enumerate(input):
        for x, _ in enumerate(line):
            if input[y][x] != '.':
                continue

            if is_valid_fill(input, (x, y)):
                fill = flood_fill(input, (x, y))
                result = len(list(f for f in fill if f[0] % 2 == 0 and f[1] % 2 == 0))

    print(result)

part2()