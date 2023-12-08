from dataclasses import dataclass
from functools import cmp_to_key

from aoc_api import get_input, submit

FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

ORDER_MAPPING = {
    'A': '0',
    'K': '1',
    'Q': '2',
    'J': '3',
    'T': '4',
    '9': '5',
    '8': '6',
    '7': '7',
    '6': '8',
    '5': '9',
    '4': 'A',
    '3': 'B',
    '2': 'C',
}

JOKER_ORDER_MAPPING = {
    'A': '0',
    'K': '1',
    'Q': '2',
    'T': '4',
    '9': '5',
    '8': '6',
    '7': '7',
    '6': '8',
    '5': '9',
    '4': 'A',
    '3': 'B',
    '2': 'C',
    'J': 'D',
}


CARDS_NO_JOKER = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2']


@dataclass(frozen=True)
class Hand:
    cards: str
    bid: int

    @staticmethod
    def parse(line: str) -> 'Hand':
        left, right = line.split()
        return Hand(cards=left, bid=int(right))

    def get_type(self) -> int:
        char_count = {}
        for char in self.cards:
            char_count[char] = char_count.get(char, 0) + 1

        counts = set(char_count.values())
        if len(char_count) == 1:
            return FIVE_OF_A_KIND
        elif len(char_count) == 2:
            if counts == {1, 4}:
                return FOUR_OF_A_KIND
            else:
                assert counts == {2, 3}
                return FULL_HOUSE
        elif len(char_count) == 3:
            if set(char_count.values()) == {3, 1}:
                # three of a kind
                return THREE_OF_A_KIND
            elif set(char_count.values()) == {2, 1}:
                # two pair
                return TWO_PAIR
        elif len(char_count) == 4:
            return ONE_PAIR
        else:
            assert len(char_count) == 5
            return HIGH_CARD

    @staticmethod
    def compare(left: 'Hand', right: 'Hand') -> int:
        if left.get_type() != right.get_type():
            return right.get_type() - left.get_type()

        left_mapped = ''.join([ORDER_MAPPING[x] for x in left.cards])
        right_mapped = ''.join([ORDER_MAPPING[x] for x in right.cards])
        if left_mapped > right_mapped:
            return 1
        elif left_mapped < right_mapped:
            return -1
        return 0


class Hand2(Hand):

    @staticmethod
    def parse(line: str) -> 'Hand2':
        left, right = line.split()
        return Hand2(cards=left, bid=int(right))

    def get_type(self) -> int:
        if self.cards == "JJJJJ":
            return FIVE_OF_A_KIND

        char_count = {}
        for char in self.cards:
            char_count[char] = char_count.get(char, 0) + 1

        joker_count = char_count.get('J', 0)
        if joker_count == 0:
            # no jokers
            return super().get_type()
        elif joker_count == 4:
            # quick optimization
            return FIVE_OF_A_KIND

        first_joker = self.cards.find('J')

        best_type = HIGH_CARD
        for card in CARDS_NO_JOKER:
            next_cards = self.cards[:first_joker] + card + self.cards[first_joker + 1:]
            best_type = max(best_type, Hand2(bid=self.bid, cards=next_cards).get_type())

        return best_type

    @staticmethod
    def compare(left: 'Hand', right: 'Hand') -> int:
        if left.get_type() != right.get_type():
            return right.get_type() - left.get_type()

        left_mapped = ''.join([JOKER_ORDER_MAPPING[x] for x in left.cards])
        right_mapped = ''.join([JOKER_ORDER_MAPPING[x] for x in right.cards])
        if left_mapped > right_mapped:
            return 1
        elif left_mapped < right_mapped:
            return -1
        return 0


def part1():
    hands = get_input(7, mapper=Hand.parse)

    answer = 0
    hands = sorted(hands, key=cmp_to_key(Hand.compare), reverse=True)

    for idx, hand in enumerate(hands):
        answer += hand.bid * (idx + 1)

    submit(day=7, level=1, answer=answer, really=True)


def part2():
    hands = get_input(7, mapper=Hand2.parse)

    answer = 0
    hands = sorted(hands, key=cmp_to_key(Hand2.compare), reverse=True)

    for idx, hand in enumerate(hands):
        answer += hand.bid * (idx + 1)

    submit(day=7, level=2, answer=answer, really=True)


part2()