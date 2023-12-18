from dataclasses import dataclass
from typing import Dict, Set, Tuple, List
import heapq


@dataclass(frozen=True)
class Edge:
    next_node_id: str
    cost: int


Graph = Dict[str, Set[Edge]]


def dijkstra(starting_point: str, graph: Graph) -> Dict[str, Tuple[int, List[str]]]:
    result = {}

    heap = [(0, starting_point, [])]
    while len(heap) != 0:
        best_cost, node, path = heapq.heappop(heap)

        if node in result:
            # already processed
            continue

        result[node] = (best_cost, path)

        for neighbor in graph.get(node, set()):
            next_node = neighbor.next_node_id
            next_cost = best_cost + neighbor.cost
            heapq.heappush(heap, (next_cost, next_node, path + [next_node]))

    return result
