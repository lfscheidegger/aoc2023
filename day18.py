from dataclasses import dataclass
from functools import lru_cache
from typing import List, Tuple, Dict, Set, Collection

from arrays import print_strings
from aoc_api import get_input, submit
from intervals import Interval
from kernels import four_kernel


@dataclass(frozen=True)
class Instruction:
    direction: str
    step_size: int
    hex_color: str

    @staticmethod
    def parse(line: str) -> 'Instruction':
        direction_str, step_size_str, hex_color_str = line.split()
        return Instruction(
            direction=direction_str,
            step_size=int(step_size_str),
            hex_color=hex_color_str[1:-1])

    def get_direction2(self) -> str:
        return ['R', 'D', 'L', 'U'][int(self.hex_color[-1])]

    def get_step_size2(self) -> int:
        return int(self.hex_color[1:-1], 16)


@dataclass(frozen=True)
class Breakpoints:
    x_breakpoints: List[int]
    y_breakpoints: List[int]


OFFSET_MAP = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, -1),
    'D': (0, 1)
}


def get_dug_cubes(instructions: List[Instruction]) -> List[Tuple[int, int]]:
    dug_cubes: List[Tuple[int, int]] = [(0, 0)]
    dig_head_position: Tuple[int, int] = 0, 0

    for instruction in instructions:
        offset = OFFSET_MAP[instruction.direction]
        for _ in range(instruction.step_size):
            dig_head_position = dig_head_position[0] + offset[0], dig_head_position[1] + offset[1]
            dug_cubes.append(dig_head_position)

    return dug_cubes


def get_trench_map(dug_cubes: Collection[Tuple[int, int]]) -> Tuple[str]:
    min_x = min(dug_cubes, key=lambda cube: cube[0])[0]
    max_x = max(dug_cubes, key=lambda cube: cube[0])[0]

    min_y = min(dug_cubes, key=lambda cube: cube[1])[1]
    max_y = max(dug_cubes, key=lambda cube: cube[1])[1]

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    result = [['.'] * width for _ in range(height)]

    for dug_cube in dug_cubes:
        x = dug_cube[0] - min_x
        y = dug_cube[1] - min_y
        result[y][x] = '#'

    return tuple(''.join(line) for line in result)


REVERSE_FLOOD_FILL_MAP: Dict[Tuple[int, int], Set[Tuple[int, int]]] = {}


@lru_cache(maxsize=150*150)
def flood_fill(input: Tuple[str], starting_point: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """
    Returns the set of flood-filled points given a starting empty point."""
    assert input[starting_point[1]][starting_point[0]] == '.'

    result: Set[Tuple[int, int]] = {starting_point}

    if starting_point in REVERSE_FLOOD_FILL_MAP:
        return REVERSE_FLOOD_FILL_MAP[starting_point]

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

    for point in result:
        REVERSE_FLOOD_FILL_MAP[point] = result
    return result


REVERSE_VALID_FILL_MAP: Dict[Tuple[int, int], bool] = {}


@lru_cache(maxsize=150*150)
def is_valid_fill(input: Tuple[str], starting_point: Tuple[int, int]) -> bool:
    """
    Returns true iff the flood fill starting in the given starting point is valid.

    A valid flood fill is adjacent to the pipe path that contains the starting point, and does not touch the outside."""
    assert input[starting_point[1]][starting_point[0]] == '.'

    if starting_point in REVERSE_VALID_FILL_MAP:
        return REVERSE_VALID_FILL_MAP[starting_point]

    fill = flood_fill(input, starting_point)

    for point in fill:
        # touches the outside
        if point[0] == 0 or point[0] == len(input[0]) - 1 or point[1] == 0 or point[1] == len(input) - 1:
            for f in fill:
                REVERSE_VALID_FILL_MAP[f] = False
            return False

    for point in fill:
        REVERSE_VALID_FILL_MAP[point] = True
    return True


def part1():
    instructions: List[Instruction] = get_input(18, mapper=Instruction.parse)

    dug_cubes = get_dug_cubes(instructions)
    trench_map = get_trench_map(dug_cubes)

    answer = None
    for y, line in enumerate(trench_map):
        if answer is not None:
            break

        for x, char in enumerate(line):
            if char != '.':
                continue
            if not is_valid_fill(trench_map, (x, y)):
                continue

            answer = len(set(dug_cubes)) + len(flood_fill(trench_map, (x, y)))
            break

    submit(day=18, level=1, answer=answer, really=True)


def get_break_points(instructions: List[Instruction]) -> Breakpoints:
    x, y = 0, 0

    x_breakpoints = []
    y_breakpoints = []

    for instruction in instructions:
        direction = instruction.get_direction2()
        step_size = instruction.get_step_size2()

        if direction == 'R':
            x += step_size
            x_breakpoints.append(x)
            x_breakpoints.append(x + 1)
        elif direction == 'L':
            x -= step_size
            x_breakpoints.append(x)
            x_breakpoints.append(x + 1)
        elif direction == 'U':
            y -= step_size
            y_breakpoints.append(y)
            y_breakpoints.append(y + 1)
        elif direction == 'D':
            y += step_size
            y_breakpoints.append(y)
            y_breakpoints.append(y + 1)

    return Breakpoints(
        x_breakpoints=sorted(set(x_breakpoints)),
        y_breakpoints=sorted(set(y_breakpoints)))


def get_dug_cubes2(instructions: List[Instruction], breakpoints: Breakpoints) -> List[Tuple[int, int]]:
    dug_cubes: List[Tuple[int, int]] = [(breakpoints.x_breakpoints.index(0), breakpoints.y_breakpoints.index(0))]
    dig_head_position: Tuple[int, int] = breakpoints.x_breakpoints.index(0), breakpoints.y_breakpoints.index(0)

    for idx, instruction in enumerate(instructions):
        direction = instruction.get_direction2()
        step_size = instruction.get_step_size2()
        offset = OFFSET_MAP[direction]

        if direction == 'R':
            next_x = breakpoints.x_breakpoints[dig_head_position[0]] + step_size
            next_x_breakpoint_idx = breakpoints.x_breakpoints.index(next_x)
            step_size = next_x_breakpoint_idx - dig_head_position[0]
            for _ in range(step_size):
                dig_head_position = dig_head_position[0] + offset[0], dig_head_position[1] + offset[1]
                dug_cubes.append(dig_head_position)
        elif direction == 'L':
            next_x = breakpoints.x_breakpoints[dig_head_position[0]] - step_size
            next_x_breakpoint_idx = breakpoints.x_breakpoints.index(next_x)
            step_size = dig_head_position[0] - next_x_breakpoint_idx
            for _ in range(step_size):
                dig_head_position = dig_head_position[0] + offset[0], dig_head_position[1] + offset[1]
                dug_cubes.append(dig_head_position)
        elif direction == 'D':
            next_y = breakpoints.y_breakpoints[dig_head_position[1]] + step_size
            next_y_breakpoint_idx = breakpoints.y_breakpoints.index(next_y)
            step_size = next_y_breakpoint_idx - dig_head_position[1]
            for _ in range(step_size):
                dig_head_position = dig_head_position[0] + offset[0], dig_head_position[1] + offset[1]
                dug_cubes.append(dig_head_position)
        elif direction == 'U':
            next_y = breakpoints.y_breakpoints[dig_head_position[1]] - step_size
            next_y_breakpoint_idx = breakpoints.y_breakpoints.index(next_y)
            step_size = dig_head_position[1] - next_y_breakpoint_idx
            for _ in range(step_size):
                dig_head_position = dig_head_position[0] + offset[0], dig_head_position[1] + offset[1]
                dug_cubes.append(dig_head_position)

    return dug_cubes


def part2():
    instructions: List[Instruction] = get_input(18, mapper=Instruction.parse)
    breakpoints = get_break_points(instructions)

    dug_cubes = get_dug_cubes2(instructions, breakpoints)
    trench_map = get_trench_map(dug_cubes)

    ff = set()
    for y, line in enumerate(trench_map):
        if len(ff) > 0:
            break

        for x, char in enumerate(line):
            if char != '.':
                continue
            if not is_valid_fill(trench_map, (x, y)):
                continue

            ff = flood_fill(trench_map, (x, y))
            break

    x_breakpoints = breakpoints.x_breakpoints
    y_breakpoints = breakpoints.y_breakpoints

    all_cubes: Set[Tuple[int, int]] = set(dug_cubes + list(ff))
    answer = 0
    for cube in all_cubes:
        width = x_breakpoints[cube[0] + 1] - x_breakpoints[cube[0]]
        height = y_breakpoints[cube[1] + 1] - y_breakpoints[cube[1]]

        answer += width * height

    submit(day=18, level=2, answer=answer)


part2()
