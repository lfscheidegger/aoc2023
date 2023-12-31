from typing import Optional, List, Tuple

from intervals import Interval


def eight_kernel(
    x: int,
    y: int,
    x_bounds: Optional[Interval] = None,
    y_bounds: Optional[Interval] = None
) -> List[Tuple[int, int]]:
    """
    Returns the 8-neighborhood kernel around the given x, y point, optionally filtering for bounds if provided."""
    result = [
        (x+1, y),
        (x+1, y+1),
        (x,   y+1),
        (x-1, y+1),
        (x-1, y),
        (x-1, y-1),
        (x,   y-1),
        (x+1, y-1),
    ]

    if x_bounds:
        result = filter(lambda p: x_bounds.contains(p[0]), result)

    if y_bounds:
        result = filter(lambda p: y_bounds.contains(p[1]), result)

    return list(result)


def nine_kernel(
    x: int,
    y: int,
    x_bounds: Optional[Interval] = None,
    y_bounds: Optional[Interval] = None
) -> List[Tuple[int, int]]:
    """
    Returns the 9-neighborhood kernel around the given x, y point, optionally filtering for bounds if provided."""
    result = eight_kernel(x, y, x_bounds, y_bounds)
    result += [(x, y)]

    if x_bounds:
        result = filter(lambda p: x_bounds.contains(p[0]), result)

    if y_bounds:
        result = filter(lambda p: y_bounds.contains(p[1]), result)

    return list(result)


def four_kernel(
    x: int,
    y: int,
    x_bounds: Optional[Interval] = None,
    y_bounds: Optional[Interval] = None
) -> List[Tuple[int, int]]:
    """
    Returns the 4-neighborhood kernel around the given x, y point, optionally filtering for bounds if provided."""
    result = [
        (x + 1, y),
        (x, y + 1),
        (x - 1, y),
        (x, y - 1),
    ]

    if x_bounds:
        result = filter(lambda p: x_bounds.contains(p[0]), result)

    if y_bounds:
        result = filter(lambda p: y_bounds.contains(p[1]), result)

    return list(result)


def five_kernel(
    x: int,
    y: int,
    x_bounds: Optional[Interval] = None,
    y_bounds: Optional[Interval] = None
) -> List[Tuple[int, int]]:
    """
    Returns the 5-neighborhood kernel around the given x, y point, optionally filtering for bounds if provided."""
    result = four_kernel(x, y, x_bounds, y_bounds)
    result += [(x, y)]

    if x_bounds:
        result = filter(lambda p: x_bounds.contains(p[0]), result)

    if y_bounds:
        result = filter(lambda p: y_bounds.contains(p[1]), result)

    return list(result)
