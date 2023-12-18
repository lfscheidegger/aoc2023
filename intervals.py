from dataclasses import dataclass
from typing import List, Union, Tuple


@dataclass(frozen=True)
class Interval:
    left: int
    right: int

    def __post_init__(self):
        if self.left >= self.right:
            raise ValueError("Left bound must be less than right bound")

    def contains(self, candidate: Union[int, 'Interval']) -> bool:
        if isinstance(candidate, int):
            return self.left <= candidate < self.right

        if candidate.is_empty():
            return True

        return candidate.left >= self.left and candidate.right <= self.right

    def is_empty(self) -> bool:
        return self.right - self.left == 1


def union(intervals: List[Interval]) -> List[Interval]:
    if not intervals:
        return []
    sorted_intervals = sorted(intervals, key=lambda x: x.left)
    merged = [sorted_intervals[0]]
    for current in sorted_intervals[1:]:
        last = merged[-1]
        if current.left <= last.right:
            last.right = max(last.right, current.right)
        else:
            merged.append(current)
    return merged


def intersection(intervals1: List[Interval], intervals2: List[Interval]) -> List[Interval]:
    i, j = 0, 0
    result = []
    while i < len(intervals1) and j < len(intervals2):
        a, b = intervals1[i], intervals2[j]
        if a.right > b.left and b.right > a.left:
            result.append(Interval(max(a.left, b.left), min(a.right, b.right)))
        if a.right < b.right:
            i += 1
        else:
            j += 1
    return result


def difference(interval: Interval, intervals_to_subtract: List[Interval]) -> List[Interval]:
    result = [interval]
    for sub in intervals_to_subtract:
        new_result = []
        for r in result:
            if sub.left <= r.left and sub.right >= r.right:
                continue
            elif sub.left > r.right or sub.right < r.left:
                new_result.append(r)
            else:
                if sub.left > r.left:
                    new_result.append(Interval(r.left, sub.left))
                if sub.right < r.right:
                    new_result.append(Interval(sub.right, r.right))
        result = new_result
    return result


def get_string_bounds(input: List[str]) -> Tuple[Interval, Interval]:
    return Interval(0, len(input[0])), Interval(0, len(input))
