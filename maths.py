import math

from functools import reduce
from typing import List


def lcm_pair(a: int, b: int) -> int:
    """
    Returns the least common multiple of two integers."""
    return a * b // math.gcd(a, b)


def lcm(lst: List[int]) -> int:
    """
    Returns the least common multiple of the given list of integers."""
    return reduce(lcm_pair, lst)
