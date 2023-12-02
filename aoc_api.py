from typing import Any, Callable, List, TypeVar, Optional, overload, Union

import subprocess

T = TypeVar('T')


@overload
def get_input(day: int, year: int = 2023) -> List[str]:
    ...


@overload
def get_input(day: int, mapper: Callable[[str], T], year: int = 2023) -> List[T]:
    ...


def get_input(day: int, mapper: Optional[Callable[[str], T]] = None, year: int = 2023) -> Union[List[str], List[T]]:
    """
    Returns the mapped input for the given day, either as a list of strings or as a list of objects from
    the optional mapper."""
    lines = get_raw_input(day, year).split("\n")
    if lines[-1] == "":
        lines = lines[:-1]

    if mapper is not None:
        return list(mapper(line) for line in lines)

    return lines


def get_raw_input(day: int, year: int = 2023) -> str:
    """
    Returns the raw string input for the given day."""
    cache_filename = f"./cache-{year}-{day}.txt"
    try:
        with open(cache_filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        pass

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    command = ["curl", url, "--cookie", _get_session_cookie()]

    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = result.stdout.decode('utf-8')

    with open(cache_filename, "w") as f:
        f.write(data)

    return data


def submit_with_day(day: int, level: int, answer: Any, really: bool = False, year: int = 2023) -> bool:
    """
    Submits the given answer, on the given day and level (level should be 1 or 2)"""

    if not really:
        print(f"{answer} - not actually submitting ({year}-{day} (part {level})")
        return False

    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    command = ["curl", "-X", "POST", url, "--cookie", _get_session_cookie(), "-d", f"level={level}", "-d", f"answer={answer}"]

    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = result.stdout.decode('utf-8')

    if data.find("That's not the right answer;") != -1:
        print(f"{answer} is wrong for {year}-{day} (part {level})... :(")
        return False

    if data.find("That's the right answer!") != -1:
        print(f"⭐⭐⭐ You got it! For {year}-{day} (part {level}) ⭐⭐⭐")
        return True

    if data.find("You gave an answer too recently;") != -1:
        raise Exception("🕒🕒🕒 Submitted too recently")

    raise Exception("Got neither right nor wrong answer, whoops")


def _get_session_cookie() -> str:
    with open("./session", "r") as f:
        return f"session={f.read()}"
