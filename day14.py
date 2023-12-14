import re
from typing import List, Tuple, Union, Dict


from aoc_api import get_input, submit


def find_hash_indices(s):
    return [match.start() + 1 for match in re.finditer(r'#', s)]


def transpose(input_chunk: Union[List[str], Tuple[str]]) -> Union[List[str], Tuple[str]]:
    result = []
    for c in range(len(input_chunk[0])):
        line = []
        for r in range(len(input_chunk)):
            line.append(input_chunk[r][c])
        result.append(''.join(line))

    if isinstance(input_chunk, tuple):
        return tuple(result)
    else:
        return result


def flip(input_chunk: Union[List[str], Tuple[str]]) -> Union[List[str], Tuple[str]]:
    result = [r[::-1] for r in input_chunk]
    if isinstance(input_chunk, tuple):
        return tuple(result)
    else:
        return result


def simulate(input: Tuple[str], direction: str) -> Tuple[str]:
    if direction == 'north':
        return transpose(simulate(transpose(input), 'west'))
    elif direction == 'south':
        return transpose(simulate(transpose(input), 'east'))
    elif direction == 'east':
        return flip(simulate(flip(input), 'west'))

    assert direction == 'west'

    result = []
    for row in input:
        hash_indices = [0] + find_hash_indices(row) + [len(row)]
        next_row = ''
        for start, end in zip(hash_indices, hash_indices[1:]):
            if start != 0:
                next_row += '#'

            rock_count = row[start: end].count('O')
            next_row += 'O' * rock_count
            next_row += '.' * (end - start - rock_count - 1)

        if len(next_row) != len(row):
            assert len(next_row) == len(row) - 1
            next_row += '.'

        assert len(next_row) == len(row)
        result.append(next_row)

    return tuple(result)


def simulate_full_cycle(input: Tuple[str]) -> Tuple[str]:
    for direction in ['north', 'west', 'south', 'east']:
        input = simulate(input, direction)

    return input


def find_cycle_data(input: Tuple[str]) -> Tuple[int, int, Tuple[str]]:
    """
    Returns the number of steps to hit the cycle, and the size of the cycle."""
    graph: Dict[Tuple[str], Tuple[str]] = {}

    def count_cycle_size(node: Tuple[str]) -> int:
        result = 1
        next_node = graph[node]
        while next_node != node:
            next_node = graph[next_node]
            result += 1

        return result

    steps_to_complete_cycle = 0
    while True:
        if input in graph:
            cycle_size = count_cycle_size(input)
            return steps_to_complete_cycle - cycle_size, cycle_size, input
        next_input = simulate_full_cycle(input)
        graph[input] = next_input
        input = next_input
        steps_to_complete_cycle += 1


def count_load(input: Tuple[str]) -> int:
    input = transpose(input)
    answer = 0

    for row in input:
        hash_indices = [0] + find_hash_indices(row) + [len(row)]
        rocks_in_row = 0
        for start, end in zip(hash_indices, hash_indices[1:]):
            rock_cost = len(row) - start
            for c in range(start, end):
                if row[c] == 'O':
                    rocks_in_row += rock_cost
                    rock_cost -= 1
        answer += rocks_in_row

    return answer


def count_simple_load(input: Tuple[str]) -> int:
    input = transpose(input)
    answer = 0

    for row in input:
        for x, char in enumerate(row):
            if char == 'O':
                answer += len(row) - x

    return answer


def part1():
    input = tuple(get_input(14))
    answer = count_load(input)
    submit(day=14, level=1, answer=answer)


def part2():
    input = tuple(get_input(14))

    cycle_data = find_cycle_data(input)

    target_count = 1_000_000_000

    left_out_of_cycle = (target_count - cycle_data[0]) % cycle_data[1]
    input = cycle_data[2]
    for _ in range(left_out_of_cycle):
        input = simulate_full_cycle(input)

    answer = count_simple_load(input)

    submit(day=14, level=2, answer=answer, really=True)


part2()
