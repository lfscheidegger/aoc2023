from dataclasses import dataclass

from aoc_api import get_input, submit
from intervals import Interval


@dataclass(frozen=True)
class Brick:
    x_bounds: Interval
    y_bounds: Interval
    z_bounds: Interval

    @staticmethod
    def parse(line: str) -> 'Brick':
        min, max = line.split("~")

        x_min, y_min, z_min = (int(n) for n in min.split(","))
        x_max, y_max, z_max = (int(n) for n in max.split(","))

        return Brick(
            x_bounds=Interval(x_min, x_max + 1),
            y_bounds=Interval(y_min, y_max + 1),
            z_bounds=Interval(z_min, z_max + 1))


def part1():
    input = get_input(day=22, mapper=Brick.parse)

    
    answer = 0

    submit(day=22, level=1, answer=answer)


part1()
