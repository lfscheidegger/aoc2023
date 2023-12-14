import re
from typing import Tuple

from arrays import transpose_strings, reverse_strings
from aoc_api import get_input, submit
from state_machines import find_cycle_data


def find_hash_indices(s):
    return [match.start() + 1 for match in re.finditer(r'#', s)]


def simulate(input: Tuple[str], direction: str) -> Tuple[str]:
    if direction == 'north':
        return transpose_strings(simulate(transpose_strings(input), 'west'))
    elif direction == 'south':
        return transpose_strings(simulate(transpose_strings(input), 'east'))
    elif direction == 'east':
        return reverse_strings(simulate(reverse_strings(input), 'west'))

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


def count_load(input: Tuple[str]) -> int:
    input = transpose_strings(input)
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
    input = transpose_strings(input)
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

    cycle_data = find_cycle_data(input, simulate_full_cycle)

    target_count = 1_000_000_000

    left_out_of_cycle = (target_count - cycle_data.steps_to_cycle) % cycle_data.cycle_size
    input = cycle_data.first_state_in_cycle
    for _ in range(left_out_of_cycle):
        input = simulate_full_cycle(input)

    answer = count_simple_load(input)

    submit(day=14, level=2, answer=answer, really=True)


part2()
