from typing import Generator, List, Tuple

from aoc_api import get_input, submit
from graphs import Edge, Graph, dijkstra
from intervals import get_string_bounds


OFFSET_MAP = {
    '-': [((1, 0), '>'), ((0, 1), 'v')],
    '>': [((1, 0), '>')],
    '<': [((-1, 0), '<')],
    'v': [((0, 1), 'v')],
    '^': [((0, -1), '^')],
}


def get_coords_between(left: Tuple[int, int], right: Tuple[int, int]) -> Generator[Tuple[int, int], None, None]:
    if right[0] - left[0] > 0:
        for x in range(left[0] + 1, right[0] + 1):
            yield x, left[1]
    elif left[0] - right[0] > 0:
        for x in range(right[0] + 1, left[0] + 1):
            yield x, left[1]
    elif right[1] - left[1] > 0:
        for y in range(left[1] + 1, right[1] + 1):
            yield left[0], y
    elif left[1] - right[1] > 0:
        for y in range(right[1] + 1, left[1] + 1):
            yield left[0], y
    else:
        raise ValueError()


def build_graph(input: List[str]) -> Graph:
    x_bounds, y_bounds = get_string_bounds(input)

    graph: Graph = {}

    # Initial state: 0,0 / no direction / 3 moves remaining
    queue: List[str] = ['0,0/-/3']
    while len(queue) != 0:
        graph_node = queue.pop()

        if graph_node in graph:
            continue

        graph[graph_node] = set()

        coords_str, direction, moves_remaining_str = graph_node.split('/')
        coords = tuple(int(x) for x in coords_str.split(','))
        moves_remaining = int(moves_remaining_str)

        # same direction
        if moves_remaining > 0:
            offsets = OFFSET_MAP[direction]
            for coord_offset, next_direction in offsets:
                next_coords = coords[0] + coord_offset[0], coords[1] + coord_offset[1]
                if not x_bounds.contains(next_coords[0]) or not y_bounds.contains(next_coords[1]):
                    continue

                cost = int(input[next_coords[1]][next_coords[0]])
                next_node_id = f'{next_coords[0]},{next_coords[1]}/{next_direction}/{moves_remaining - 1}'
                graph[graph_node].add(Edge(next_node_id=next_node_id, cost=cost))
                queue.append(next_node_id)

        # switch direction
        if direction in ['>', '<']:
            next_direction = 'v'
            next_coords = coords[0], coords[1] + 1
            if x_bounds.contains(next_coords[0]) and y_bounds.contains(next_coords[1]):
                cost = int(input[next_coords[1]][next_coords[0]])
                next_node_id = f'{next_coords[0]},{next_coords[1]}/{next_direction}/2'
                graph[graph_node].add(Edge(next_node_id=next_node_id, cost=cost))
                queue.append(next_node_id)

            next_direction = '^'
            next_coords = coords[0], coords[1] - 1
            if x_bounds.contains(next_coords[0]) and y_bounds.contains(next_coords[1]):
                cost = int(input[next_coords[1]][next_coords[0]])
                next_node_id = f'{next_coords[0]},{next_coords[1]}/{next_direction}/2'
                graph[graph_node].add(Edge(next_node_id=next_node_id, cost=cost))
                queue.append(next_node_id)

        elif direction in ['v', '^']:
            next_direction = '>'
            next_coords = coords[0] + 1, coords[1]
            if x_bounds.contains(next_coords[0]) and y_bounds.contains(next_coords[1]):
                cost = int(input[next_coords[1]][next_coords[0]])
                next_node_id = f'{next_coords[0]},{next_coords[1]}/{next_direction}/2'
                graph[graph_node].add(Edge(next_node_id=next_node_id, cost=cost))
                queue.append(next_node_id)

            next_direction = '<'
            next_coords = coords[0] - 1, coords[1]
            if x_bounds.contains(next_coords[0]) and y_bounds.contains(next_coords[1]):
                cost = int(input[next_coords[1]][next_coords[0]])
                next_node_id = f'{next_coords[0]},{next_coords[1]}/{next_direction}/2'
                graph[graph_node].add(Edge(next_node_id=next_node_id, cost=cost))
                queue.append(next_node_id)

    return graph


def build_graph2(input: List[str]) -> Graph:
    x_bounds, y_bounds = get_string_bounds(input)

    graph: Graph = {}

    # Initial state: 0,0 / no direction / 0 moves made / 10 moves remaining
    queue: List[str] = ['0,0/-/0/10']
    while len(queue) != 0:
        graph_node = queue.pop()

        if graph_node in graph:
            continue

        graph[graph_node] = set()

        coords_str, direction, moves_made_str, moves_remaining_str = graph_node.split('/')
        coords = tuple(int(x) for x in coords_str.split(','))
        moves_made = int(moves_made_str)
        moves_remaining = int(moves_remaining_str)

        # same direction
        if moves_remaining > 0:
            offsets = OFFSET_MAP[direction]
            for coord_offset, next_direction in offsets:
                next_coords = coords[0] + coord_offset[0], coords[1] + coord_offset[1]
                if not x_bounds.contains(next_coords[0]) or not y_bounds.contains(next_coords[1]):
                    continue

                cost = int(input[next_coords[1]][next_coords[0]])
                next_node_id = f'{next_coords[0]},{next_coords[1]}/{next_direction}/{moves_made + 1}/{moves_remaining - 1}'
                graph[graph_node].add(Edge(next_node_id=next_node_id, cost=cost))
                queue.append(next_node_id)

        # switch direction
        if moves_made >= 4 and direction in ['>', '<']:
            next_direction = 'v'
            next_coords = coords[0], coords[1] + 1
            if x_bounds.contains(next_coords[0]) and y_bounds.contains(next_coords[1]):
                cost = int(input[next_coords[1]][next_coords[0]])
                next_node_id = f'{next_coords[0]},{next_coords[1]}/{next_direction}/1/9'
                graph[graph_node].add(Edge(next_node_id=next_node_id, cost=cost))
                queue.append(next_node_id)

            next_direction = '^'
            next_coords = coords[0], coords[1] - 1
            if x_bounds.contains(next_coords[0]) and y_bounds.contains(next_coords[1]):
                cost = int(input[next_coords[1]][next_coords[0]])
                next_node_id = f'{next_coords[0]},{next_coords[1]}/{next_direction}/1/9'
                graph[graph_node].add(Edge(next_node_id=next_node_id, cost=cost))
                queue.append(next_node_id)

        elif moves_made >= 4 and direction in ['v', '^']:
            next_direction = '>'
            next_coords = coords[0] + 1, coords[1]
            if x_bounds.contains(next_coords[0]) and y_bounds.contains(next_coords[1]):
                cost = int(input[next_coords[1]][next_coords[0]])
                next_node_id = f'{next_coords[0]},{next_coords[1]}/{next_direction}/1/9'
                graph[graph_node].add(Edge(next_node_id=next_node_id, cost=cost))
                queue.append(next_node_id)

            next_direction = '<'
            next_coords = coords[0] - 1, coords[1]
            if x_bounds.contains(next_coords[0]) and y_bounds.contains(next_coords[1]):
                cost = int(input[next_coords[1]][next_coords[0]])
                next_node_id = f'{next_coords[0]},{next_coords[1]}/{next_direction}/1/9'
                graph[graph_node].add(Edge(next_node_id=next_node_id, cost=cost))
                queue.append(next_node_id)

    return graph


def part1():
    input = get_input(17)

    graph = build_graph(input)

    costs = dijkstra('0,0/-/3', graph)

    answer = 10 * len(input) * len(input[0])
    for node_id in costs:
        cost, path = costs[node_id]
        node_id_without_state = node_id.split("/")[0]
        if node_id_without_state == f'{len(input[0]) - 1},{len(input)-1}':
            if cost < answer:
                answer = cost

    submit(day=17, level=1, answer=answer)


def part2():
    input = get_input(17)

    graph = build_graph2(input)

    costs = dijkstra('0,0/-/0/10', graph)

    answer = 10 * len(input) * len(input[0])
    for node_id in costs:
        cost, path = costs[node_id]
        node_id_without_state = node_id.split("/")[0]
        if node_id_without_state == f'{len(input[0]) - 1},{len(input)-1}':
            if cost < answer:
                answer = cost

    submit(day=17, level=2, answer=answer)


part2()
