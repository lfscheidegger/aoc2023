from typing import List, Tuple

from aoc_api import get_input, submit


def expand_input(input: List[str]) -> List[str]:
    result: List[str] = []

    for line in input:
        if all([x == '.' for x in line]):
            result.append(line)
        result.append(line)

    final_result = []
    for r, line in enumerate(result):
        new_row = ''
        for c, _ in enumerate(line):
            if all([result[r2][c] == '.' for r2 in range(len(result))]):
                new_row += '.'
            new_row += line[c]
        final_result.append(new_row)

    return final_result


def expand_input_2(input: List[str]) -> List[str]:
    result: List[str] = []

    for line in input:
        if all([x == '.' for x in line]):
            result.append("".join(['X' for _ in line]))
        else:
            result.append(line)

    final_result = []
    for r, line in enumerate(result):
        new_row = ''
        for c, _ in enumerate(line):
            if all([result[r2][c] in ['.', 'X'] for r2 in range(len(result))]):
                new_row += 'X'
            else:
                new_row += line[c]
        final_result.append(new_row)

    return final_result


def find_all_galaxies(input: List[str]) -> List[Tuple[int, int]]:
    result = []
    for r, line in enumerate(input):
        for c, char in enumerate(line):
            if char == '#':
                result.append((c, r))

    return result


def part1():
    input = get_input(11)
    input = expand_input(input)

    galaxies = find_all_galaxies(input)
    answer = 0
    for left in galaxies:
        for right in galaxies:
            if left == right:
                continue

            answer += abs(left[0] - right[0]) + abs(left[1] - right[1])

    answer //= 2
    submit(day=11, level=1, answer=answer)


EXPANSION = 1_000_000


def part2():
    input = get_input(11)
    input = expand_input_2(input)

    galaxies = find_all_galaxies(input)
    answer = 0
    for left in galaxies:
        for right in galaxies:
            if left == right:
                continue

            x_min = min(left[0], right[0])
            y_min = min(left[1], right[1])

            x_max = max(left[0], right[0])
            y_max = max(left[1], right[1])

            distance = 0
            for x in range(x_min+1, x_max+1):
                if input[y_min][x] == 'X':
                    distance += EXPANSION
                else:
                    distance += 1

            for y in range(y_min+1, y_max+1):
                if input[y][x_max] == 'X':
                    distance += EXPANSION
                else:
                    distance += 1

            answer += distance

    answer //= 2
    submit(day=11, level=2, answer=answer, really=True)


part2()
