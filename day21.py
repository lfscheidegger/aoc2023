from collections import defaultdict
from typing import Tuple, Set, Dict, Collection, List

from aoc_api import get_input, submit
from intervals import Interval
from kernels import four_kernel
from vectors import Vec2, minus2


def get_starting_position() -> Vec2:
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            if char == 'S':
                return x, y

    assert False


def steps_from_steps(current_plots: Set[Vec2]) -> Set[Vec2]:
    result: Set[Vec2] = set()

    x_bounds = Interval(0, len(input[0]))
    y_bounds = Interval(0, len(input))

    for x, y in current_plots:
        for (n_x, n_y) in four_kernel(x, y, x_bounds, y_bounds):
            if input[n_y][n_x] == '#':
                continue
            result.add((n_x, n_y))

    return result


def advance_farms(this_farm: Vec2, current_plots: Set[Vec2]) -> Dict[Vec2, Set[Vec2]]:
    left_farm: Vec2 = (this_farm[0] - 1, this_farm[1])
    right_farm: Vec2 = (this_farm[0] + 1, this_farm[1])
    top_farm: Vec2 = (this_farm[0], this_farm[1] - 1)
    bottom_farm: Vec2 = (this_farm[0], this_farm[1] + 1)

    result: Dict[Vec2, Set[Vec2]] = defaultdict(set)

    width = len(input[0])
    height = len(input)

    for x, y in current_plots:
        for (n_x, n_y) in four_kernel(x, y):
            if n_x < 0:
                n_x += width
                if input[n_y][n_x] != '#':
                    result[left_farm].add((n_x, n_y))
                continue

            if n_x >= width:
                n_x -= width
                if input[n_y][n_x] != '#':
                    result[right_farm].add((n_x, n_y))
                continue

            if n_y < 0:
                n_y += height
                if input[n_y][n_x] != '#':
                    result[top_farm].add((n_x, n_y))
                continue

            if n_y >= height:
                n_y -= height
                if input[n_y][n_x] != '#':
                    result[bottom_farm].add((n_x, n_y))
                continue

            if input[n_y][n_x] != '#':
                result[this_farm].add((n_x, n_y))
                continue

    return result


input: List[str] = []
red: Set[Vec2] = set()
green: Set[Vec2] = set()


def print_farm(current_plots: Collection[Vec2]):
    current_plots = set(current_plots)
    for y, line in enumerate(input):
        to_print = []
        for x, char in enumerate(line):
            if (x, y) in current_plots:
                to_print.append('O')
            else:
                to_print.append(char.replace('S', '.'))
        print(''.join(to_print))
    print()


def count_garden_plots(
        farm_chart: Dict[Vec2, Set[Vec2]],
        steady_state_farms: Dict[Vec2, int],
        steps: int
) -> int:
    result = 0

    print(f'total farms: {len(farm_chart)}')
    print(f'total steady state farms: {len(steady_state_farms)}')

    for this_farm in sorted(list(farm_chart.keys()) + list(steady_state_farms.keys())):
        if this_farm in farm_chart:
            assert this_farm not in steady_state_farms

            print(this_farm)
            if farm_chart[this_farm] == red:
                print(f'Red farm: {len(farm_chart[this_farm])}')
            elif farm_chart[this_farm] == green:
                print(f'Green farm: {len(farm_chart[this_farm])}')
            else:
                print(len(farm_chart[this_farm]))
                print_farm(farm_chart[this_farm])

            result += len(farm_chart[this_farm])

        elif this_farm in steady_state_farms:
            assert this_farm not in farm_chart

            print(this_farm)
            parity = steady_state_farms[this_farm]
            if steps % 2 == parity:
                print(f'Green farm: {len(green)}')
                result += len(green)
            else:
                print(f'Red farm: {len(red)}')
                result += len(red)

    return result


def find_steady_states() -> Tuple[Set[Vec2], Set[Vec2]]:
    p0: Set[Tuple[int, int]] = {get_starting_position()}
    while True:
        p1 = steps_from_steps(p0)
        p2 = steps_from_steps(p1)

        if p0 == p2:
            return p0, p1

        p0 = p1


def part1():
    global input

    input = get_input(day=21)

    current_plots: Set[Vec2] = {get_starting_position()}
    steps = 0
    while steps < 64:
        current_plots = steps_from_steps(current_plots)
        steps += 1

    submit(day=21, level=1, answer=len(current_plots))


def part2():
    global input, red, green

    input = get_input(day=21)

    steps = 0
    farm_chart: Dict[Vec2, Set[Vec2]] = {(0, 0): {get_starting_position()}}

    red, green = find_steady_states()

    print('red')
    print_farm(red)

    print('green')
    print_farm(green)

    assert(steps_from_steps(red) == green)
    assert(steps_from_steps(green) == red)

    next_after_red = advance_farms((0, 0), red)
    next_after_green = advance_farms((0, 0), green)

    # parity of step when reaching red steady state
    steady_state_farms: Dict[Vec2, int] = {}

    while steps < 36:
        next_farm_chart: Dict[Vec2, Set[Vec2]] = {}

        # Advect "out" of the front
        for this_farm in farm_chart:
            next_farms = advance_farms(this_farm, farm_chart[this_farm])
            for next_farm in next_farms:
                if next_farm in steady_state_farms:
                    # Let's not advect out to cells that are already in steady state
                    continue
                next_farm_chart[next_farm] = next_farms[next_farm].union(next_farm_chart.get(next_farm, set()))

        # Advect "in" from the front
        for this_farm in farm_chart:
            for neighbor_farm in four_kernel(this_farm[0], this_farm[1]):
                if neighbor_farm not in steady_state_farms:
                    continue

                relative_farm_coords = minus2(this_farm, neighbor_farm)

                steady_state_parity = steady_state_farms[neighbor_farm]
                if steps % 2 == steady_state_parity:
                    next_farm_chart[this_farm] = next_after_green[relative_farm_coords].union(next_farm_chart.get(this_farm, set()))
                else:
                    next_farm_chart[this_farm] = next_after_red[relative_farm_coords].union(next_farm_chart.get(this_farm, set()))

        farm_chart = next_farm_chart


        # Cull farms that have reached steady state
        to_delete = set()
        for this_farm in farm_chart:
            #if this_farm == (0, -2):
            #    print(steps)
            #    print_farm(farm_chart[this_farm])
            if farm_chart[this_farm] == red:
                #continue
                to_delete.add(this_farm)
                steady_state_farms[this_farm] = steps % 2
            elif farm_chart[this_farm] == green:
                #continue
                to_delete.add(this_farm)
                steady_state_farms[this_farm] = 1 + steps % 2

        for this_farm in to_delete:
            del farm_chart[this_farm]

        steps += 1



    answer = count_garden_plots(farm_chart, steady_state_farms, steps)
    submit(day=21, level=2, answer=answer)


part2()
