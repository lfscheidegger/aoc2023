from functools import cache
from typing import List, Tuple, Dict

from aoc_api import get_input, submit


Graph = Tuple[Tuple[str, Tuple[str]]]


def parse(lines: List[str]) -> Graph:
    result: Dict[str, List[str]] = {}
    for line in lines:
        left, right = line.split(":")
        src = left.strip()
        dsts = [x.strip() for x in right.split()]

        for dst in dsts:
            if src not in result:
                result[src] = []

            if dst not in result:
                result[dst] = []

            result[src].append(dst)
            result[dst].append(src)

    return tuple((x, tuple(result[x])) for x in result)


@cache
def count_components(graph: Graph, excluded: Tuple[Tuple[str, str]] = tuple()) -> int:
    graph = {x[0]: x[1] for x in graph}

    connected_components = 0
    while len(graph) > 0:
        head = list(graph.keys())[0]
        queue: List[str] = [head]

        while len(queue) > 0:
            head = queue.pop()
            connections = graph.get(head)
            if connections is None:
                continue

            del graph[head]
            queue += connections

        connected_components += 1

    return connected_components


def part1():
    input = get_input(day=25)
    answer = count_components(parse(input))

    submit(day=25, level=1, answer=answer)


part1()