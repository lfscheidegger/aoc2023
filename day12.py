from functools import lru_cache
from typing import List, Tuple, Optional, Generator
import itertools
from multiprocessing import Pool
import re

from aoc_api import get_input, submit


def get_combinations(row: str) -> int:
    left, right = row.split()
    damaged_counts = [int(x) for x in right.split(",")]

    return count_valid_arrangements(left, tuple(damaged_counts))


@lru_cache(maxsize=10000000)
def count_valid_arrangements(springs: str, groups: Tuple[int]) -> int:
    if len(groups) == 0 and all([x not in ['?', '#'] for x in springs]):
        return 1
    elif len(groups) == 0 and any([x == '#' for x in springs]):
        return 0

    question_mark_span = find_question_mark_span(springs)

    result = 0
    for candidate in generate_all_options(springs, question_mark_span):
        if candidate == springs:
            # Eliminated all unknowns
            first_damaged_size, after_first_damaged_group = find_first_contiguous_damaged(candidate)
            if first_damaged_size == -1 or first_damaged_size != groups[0]:
                # Invalid case - ran out of damaged chunks and the groups still expect us to find some
                return 0
            else:
                # Candidate has a broken group
                if len(groups) == 0:
                    pass
                elif first_damaged_size == groups[0]:
                    # This is a valid configuration so far
                    result += count_valid_arrangements(candidate[after_first_damaged_group:], groups[1:])
        else:
            first_damaged_size, after_first_damaged_group = find_first_contiguous_damaged(candidate)
            if first_damaged_size == -1:
                # Nothing known about first broken chunks yet, simply recurse
                result += count_valid_arrangements(candidate, groups)
            else:
                if len(groups) == 0:
                    pass
                elif first_damaged_size == groups[0]:
                    # This is a valid configuration so far
                    result += count_valid_arrangements(candidate[after_first_damaged_group:], groups[1:])

    return result


@lru_cache(maxsize=10000000)
def find_question_mark_span(text: str) -> Optional[Tuple[int, int]]:
    match = re.search(r'\?+', text)
    if match:
        return match.start(), match.end() - match.start()
    else:
        return None


def generate_all_options(text: str, span: Optional[Tuple[int, int]]) -> Generator[str, None, None]:
    if span is None:
        yield text
    else:
        for chunk in itertools.product(['.', '#'], repeat=span[1]):
            yield text[:span[0]] + ''.join(chunk) + text[span[0]+span[1]:]


@lru_cache(maxsize=10000000)
def find_first_contiguous_damaged(springs: str) -> Tuple[int, int]:
    """
    Returns the size of, and last index + 1, of the first contiguous group of broken springs found in the given springs
    line"""
    first_broken = springs.find('#')
    if first_broken == -1:
        # no known broken chunks
        return -1, -1

    first_question_mark = springs.find('?')
    if first_question_mark != -1 and first_question_mark < first_broken:
        # unknowns coming before known broken chunks
        return -1, -1

    size = 0
    while first_broken < len(springs) and springs[first_broken] == '#':
        size += 1
        first_broken += 1

    if first_broken < len(springs) and springs[first_broken] == '?':
        # still no known broken chunk - the one we found might be larger with this question mark
        return -1, -1

    return size, first_broken


def expand_line(line: str, amount: int) -> str:
    if amount == 1:
        return line

    left, right = line.split()

    left = '?'.join([left.strip() for _ in range(amount)])
    right = ','.join([right.strip() for _ in range(amount)])

    return f'{left} {right}'


def part1():
    input = get_input(12)

    answer = 0
    for line in input:
        answer += get_combinations(line)

    submit(day=12, level=1, answer=answer, really=True)


def answer_single(line: str) -> int:
    initial_count = get_combinations(line)
    ratio = get_combinations(expand_line(line, 2)) // initial_count
    return initial_count * ratio ** 4


def part2():
    input = get_input(12)

    p = Pool()
    numbers = p.map(answer_single, input)
    answer = sum(numbers)
    #answer = 0
    #for idx, line in enumerate(input):
    #    initial_count = get_combinations(line)
    #    ratio = get_combinations(expand_line(line, 2)) // initial_count
    #    answer += initial_count * ratio ** 4
    #    print(idx)
        #print(line)
        #for expand_count in range(1, 6):
        #    expanded = expand_line(line, expand_count)
        #    print(expand_count, get_combinations(expanded))
        #print()
        #expanded = expand_line(line, 5)
        #print(line, '------', expanded)
        #answer += get_combinations(expanded)
        #print(answer)
        #print(get_combinations(line))
        #print(get_combinations(expanded))

    submit(day=12, level=2, answer=answer)


if __name__ == '__main__':
    part2()
