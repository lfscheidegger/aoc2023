from dataclasses import dataclass
from typing import Callable, Dict, Generic, TypeVar, Tuple

T = TypeVar('T')


@dataclass(frozen=True)
class CycleData(Generic[T]):
    """
    Information about a cycle in a deterministic state machine. Contains the number of steps to enter the cycle,
    the cycle size, and the first state in the cycle."""
    steps_to_cycle: int
    cycle_size: int
    first_state_in_cycle: T


def find_cycle_data(input: T, advance: Callable[[T], T]) -> CycleData[T]:
    """
    Returns the number of steps to hit the cycle, and the size of the cycle."""
    graph: Dict[T, T] = {}

    def count_cycle_size(node: T) -> int:
        result = 1
        next_node = graph[node]
        while next_node != node:
            next_node = graph[next_node]
            result += 1

        return result

    steps_to_complete_cycle = 0
    while True:
        if input in graph:
            cycle_size = count_cycle_size(input)
            return CycleData(
                steps_to_cycle=steps_to_complete_cycle - cycle_size,
                cycle_size=cycle_size,
                first_state_in_cycle=input)
        next_input = advance(input)
        graph[input] = next_input
        input = next_input
        steps_to_complete_cycle += 1
