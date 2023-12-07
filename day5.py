from dataclasses import dataclass
from typing import List, Set, Tuple

from aoc_api import get_raw_input_chunks, submit
from intervals import Interval, intersection, difference


@dataclass
class Mapping:
    source_type: str
    destination_type: str

    # source interval, dest offset
    intervals: List[Tuple[Interval, int]]

    @staticmethod
    def parse(lines: List[str]) -> 'Mapping':
        source_type, _, destination_type = lines[0].split()[0].split("-")
        intervals: List[Tuple[Interval, int]] = []

        lines = lines[1:]
        for line in lines:
            destination, source, length = map(lambda s: int(s), line.split())
            intervals.append((Interval(source, source + length), destination))

        return Mapping(
            source_type=source_type,
            destination_type=destination_type,
            intervals=intervals)

    def advance_seed(self, seed: int) -> int:
        for interval in self.intervals:
            if interval[0].contains(seed):
                return interval[1] + (seed - interval[0].left)
        return seed

    def advance_range(self, seed_interval: Interval) -> List[Interval]:
        unprocessed: Set[Interval] = {seed_interval}
        result: Set[Interval] = set()
        for interval in self.intervals:
            failed_to_process: Set[Interval] = set()
            while len(unprocessed) > 0:
                candidate = unprocessed.pop()

                intersect = intersection([candidate], [interval[0]])
                assert len(intersect) <= 1
                if len(intersect) == 1 and not intersect[0].is_empty():
                    intersect = intersect[0]
                    left = interval[1] + intersect.left - interval[0].left
                    right = interval[1] + intersect.right - interval[0].left
                    result.add(Interval(left=left, right=right))

                differ = difference(candidate, [interval[0]])
                for d in differ:
                    failed_to_process.add(d)

            unprocessed = failed_to_process
            if len(unprocessed) == 0:
                return list(result)

        # whatever's left is a passthrough
        return list(set(list(unprocessed) + list(result)))

    def advance_ranges(self, intervals: List[Interval]) -> List[Interval]:
        result: Set[Interval] = set()
        for interval in intervals:
            result = result.union(self.advance_range(interval))

        return list(result)


def parse_seeds(line: str) -> List[int]:
    return [int(x.strip()) for x in line.split(":")[1].strip().split()]


def parse_seed_intervals(line: str) -> List[Interval]:
    tokens = line.split(":")[1].strip().split()
    assert len(tokens) % 2 == 0

    result: List[Interval] = []
    for idx in range(len(tokens) // 2):
        left = int(tokens[2 * idx])
        right = int(tokens[2 * idx + 1])

        result.append(Interval(left=left, right=left+right))
    return result


def part1():
    input = get_raw_input_chunks(5)

    seeds = parse_seeds(input[0][0])
    mappings = [Mapping.parse(chunk) for chunk in input[1:]]

    answer = 2**64

    for seed in seeds:
        for mapping in mappings:
            seed = mapping.advance_seed(seed)
        answer = min(answer, seed)

    submit(day=5, level=1, answer=answer)


def part2():
    input = get_raw_input_chunks(5)

    seed_intervals = parse_seed_intervals(input[0][0])
    mappings = [Mapping.parse(chunk) for chunk in input[1:]]

    answer = 2**128

    for interval in seed_intervals:
        intervals = [interval]
        for mapping in mappings:
            intervals = mapping.advance_ranges(intervals)

        min_in_batch = min(intervals, key=lambda i: i.left).left
        answer = min(answer, min_in_batch)

    submit(day=5, level=2, answer=answer, really=True)


part2()