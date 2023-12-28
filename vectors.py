import math
from typing import Tuple, Union, Optional

Vec2 = Union[Tuple[float, float], Tuple[int, int]]
Vec3 = Union[Tuple[float, float, float], Tuple[int, int, int]]


def cross2(left: Vec2, right: Vec2) -> float:
    """
    2-d cross product. Returns the "z component" of the cross product between the two xy vectors."""
    return left[0] * right[1] - left[1] * right[0]


def plus2(left: Vec2, right: Vec2) -> Vec2:
    return left[0] + right[0], left[1] + right[1]


def minus2(left: Vec2, right: Vec2) -> Vec2:
    return left[0] - right[0], left[1] - right[1]


def times2(left: Vec2, right: Union[int, float]) -> Vec2:
    return left[0] * right, left[1] * right


def divide2(left: Vec2, right: Union[int, float]) -> Vec2:
    return left[0] / right, left[1] / right


def plus3(left: Vec3, right: Vec3) -> Vec3:
    return left[0] + right[0], left[1] + right[1], left[2] + right[2]


def minus3(left: Vec3, right: Vec3) -> Vec3:
    return left[0] - right[0], left[1] - right[1], left[2] - right[2]


def times3(left: Vec3, right: Union[int, float]) -> Vec3:
    return left[0] * right, left[1] * right, left[2] * right


def divide3(left: Vec3, right: Union[int, float]) -> Vec3:
    return left[0] / right, left[1] / right, left[2] / right


def norm_sq3(vec: Vec3) -> float:
    return vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2


def norm3(vec: Vec3) -> float:
    return math.sqrt(norm_sq3(vec))


def intersect2(p1: Vec2, v1: Vec2, p2: Vec2, v2: Vec2) -> Optional[Vec2]:
    """
    Returns the point in 2-d where the two ray segments defined by p1, v1 and p2, v2 intersect, if any. Does not
    consider intersections with negative t or u parameters.

    Based on https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect/565282#565282"""
    p = p1
    r = v1
    q = p2
    s = v2

    determinant = cross2(r, s)
    if determinant == 0:
        return None

    t = cross2((minus2(q, p)), divide2(s, determinant))
    u = cross2((minus2(q, p)), divide2(r, determinant))

    if t < 0 or u < 0:
        return None

    return plus2(p, times2(r, t))
