from input_helpers import get_input

from dataclasses import dataclass
import re
from typing import List


@dataclass
class Game:
    red: int
    green: int
    blue: int

    def is_acceptable(self) -> bool:
        return self.red <= 12 and self.green <= 13 and self.blue <= 14
@dataclass
class GameLine:
    id: int
    games: List[Game]

    def is_acceptable(self) -> bool:
        return all([game.is_acceptable() for game in self.games])

    def power(self) -> int:
        max_red = max(self.games, key=lambda game: game.red).red
        max_green = max(self.games, key=lambda game: game.green).green
        max_blue = max(self.games, key=lambda game: game.blue).blue

        return max_red * max_green * max_blue


def parse_game_line(line: str) -> GameLine:
    (id, games_line) = line.split(":")
    id = int(id.split(" ")[1].strip())
    return GameLine(
        id=id,
        games=parse_games(games_line)
    )


PATTERN = r'(?:(\d+)\s*(blue|red|green))'


def parse_games(games_line: str) -> List[Game]:
    result = []
    for single_game in games_line.split(";"):
        single_game = single_game.strip()
        matches = re.findall(PATTERN, single_game)
        color_numbers = {color: int(number) for number, color in matches}

        result.append(Game(
            red=color_numbers.get("red", 0),
            green=color_numbers.get("green", 0),
            blue=color_numbers.get("blue", 0)
        ))
    return result


def part1():
    game_lines = get_input(2, parse_game_line)
    print(sum([game_line.id for game_line in game_lines if game_line.is_acceptable()]))


def part2():
    game_lines = get_input(2, parse_game_line)
    print(sum([game_line.power() for game_line in game_lines]))

part2()