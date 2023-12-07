from dataclasses import dataclass
from typing import List, Set, Dict, Optional, Union, Any, Tuple

from aoc_api import get_input, submit

@dataclass
class Race:
    time_ms: int
    distance_millis: int

    def simulate(self, hold_down_time_ms: int) -> int:
        return (self.time_ms - hold_down_time_ms) * hold_down_time_ms

    def beats(self, hold_down_time_ms: int) -> bool:
        return self.simulate(hold_down_time_ms) > self.distance_millis

    def count_beats(self) -> int:
        result = 0
        for hold_down_time_ms in range(self.time_ms + 1):
            if self.beats(hold_down_time_ms):
                result += 1

        return result

    def count_beats_smart(self) -> int:
        min_hold_down_time = 1
        old_min_hold_down_time = min_hold_down_time
        while not self.beats(min_hold_down_time):
            old_min_hold_down_time = min_hold_down_time
            min_hold_down_time *= 2

        left, right = old_min_hold_down_time, min_hold_down_time
        mid = (left + right) // 2

        while mid > left:
            if self.beats(mid):
                right = mid
                mid = (left + right) // 2
            else:
                left = mid
                mid = (left + right) // 2

        smallest_beating = mid + 1

        max_hold_down_time = self.time_ms
        old_max_hold_down_time = max_hold_down_time
        discount = 1
        while not self.beats(max_hold_down_time):
            old_max_hold_down_time = max_hold_down_time
            max_hold_down_time -= discount
            # whoops but fast enough
            discount *= 1

        largest_beating = max_hold_down_time

        return largest_beating - smallest_beating + 1

RACES: List[Race] = [
    Race(time_ms=59, distance_millis=430),
    Race(time_ms=70, distance_millis=1218),
    Race(time_ms=78, distance_millis=1213),
    Race(time_ms=78, distance_millis=1276),
]

RACES: List[Race] = [
    Race(time_ms=7, distance_millis=9),
    Race(time_ms=15, distance_millis=40),
    Race(time_ms=30, distance_millis=200),
]

def part1():
    answer = 1

    for count_beats in [race.count_beats() for race in RACES]:
        answer *= count_beats

    submit(day=6, level=1, answer=answer, really=True)


def part2():
    races: List[Race] = [
        Race(time_ms=59707878, distance_millis=430121812131276),
        #Race(time_ms=71530, distance_millis=940200)
    ]

    answer = 1

    for count_beats in [race.count_beats_smart() for race in races]:
        answer *= count_beats

    submit(day=6, level=2, answer=answer, really=True)

part2()