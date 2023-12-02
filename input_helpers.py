from typing import Callable, List, TypeVar, Optional, overload, Union

import subprocess

T = TypeVar('T')


@overload
def get_input(day: int) -> List[str]:
    ...


@overload
def get_input(day: int, mapper: Callable[[str], T]) -> List[T]:
    ...


def get_input(day: int, mapper: Optional[Callable[[str], T]] = None) -> Union[List[str], List[T]]:
    lines = get_raw_input(day).split("\n")
    if lines[-1] == "":
        lines = lines[:-1]

    if mapper is not None:
        return list(mapper(line) for line in lines)

    return lines


def get_raw_input(day: int) -> str:
    """
    Returns the raw string input for the given day."""
    cache_filename = f"./day{day}.txt"
    try:
        with open(cache_filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        pass

    with open("./session", "r") as f:
        cookie = f"session={f.read()}"

    url = f"https://adventofcode.com/2023/day/{day}/input"
    command = ["curl", url, "--cookie", cookie]

    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = result.stdout.decode('utf-8')

    with open(cache_filename, "w") as f:
        f.write(data)

    return data
