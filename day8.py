from dataclasses import dataclass
from typing import Dict, Tuple, List

from aoc_api import get_input, submit
from maths import lcm


@dataclass(frozen=True)
class Node:
    id: str
    left: str
    right: str

    @staticmethod
    def parse(line: str) -> 'Node':
        line = line.split("=")
        id = line[0].strip()

        left, right = line[1].split(",")

        left = left[2:]
        right = right.strip()[:-1]

        return Node(id=id, left=left, right=right)


def get_node_map(nodes: List[Node]) -> Dict[Tuple[str, str], str]:
    result = {}
    for node in nodes:
        result[(node.id, 'L')] = node.left
        result[(node.id, 'R')] = node.right

    return result


def part1():
    input = get_input(8)
    instructions = input[0].strip()

    input = input[2:]
    nodes = [Node.parse(line) for line in input]

    node_map = get_node_map(nodes)
    current_node = 'AAA'
    count = 0

    while current_node != 'ZZZ':
        for inst in instructions:
            if current_node == 'ZZZ':
                break

            current_node = node_map[(current_node, inst)]
            count += 1

    answer = count

    submit(day=8, level=1, answer=answer, really=True)


def part2():
    input = get_input(8)
    instructions = input[0].strip()

    input = input[2:]
    nodes = [Node.parse(line) for line in input]

    node_map = get_node_map(nodes)

    current_nodes = list(map(lambda node: node[0], filter(lambda node: node[0].endswith('A'), node_map.keys())))

    counts = []
    for current_node in current_nodes:
        count = 0

        while not current_node.endswith('Z'):
            for inst in instructions:
                if current_node.endswith('Z'):
                    break

                current_node = node_map[(current_node, inst)]
                count += 1

        counts.append(count)

    answer = lcm(counts)
    submit(day=8, level=2, answer=answer, really=True)


part2()
