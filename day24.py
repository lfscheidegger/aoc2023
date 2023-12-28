from dataclasses import dataclass
from typing import Optional, Tuple, List

from aoc_api import get_input, submit
from vectors import Vec2, intersect2


@dataclass(frozen=True)
class RaySegment:
    p_x: int
    p_y: int
    p_z: int

    v_x: int
    v_y: int
    v_z: int

    @staticmethod
    def parse(line: str) -> 'RaySegment':
        left, right = line.split('@')
        p_x, p_y, p_z = [int(t.strip()) for t in left.split(',')]
        v_x, v_y, v_z = [int(t.strip()) for t in right.split(',')]

        return RaySegment(p_x, p_y, p_z, v_x, v_y, v_z)

    def p_xy(self) -> Vec2:
        return self.p_x, self.p_y

    def v_xy(self) -> Vec2:
        return self.v_x, self.v_y


def part1():
    input: List[RaySegment] = get_input(day=24, mapper=RaySegment.parse)

    answer = 0
    left = 200000000000000
    right = 400000000000000

    for i, r1 in enumerate(input):
        for r2 in input[i+1:]:
            intersection = intersect2(r1.p_xy(), r1.v_xy(), r2.p_xy(), r2.v_xy())
            if intersection is None:
                continue

            if (left <= intersection[0] <= right) and (left <= intersection[1] <= right):
                answer += 1

    submit(day=24, level=1, answer=answer)


part1()
