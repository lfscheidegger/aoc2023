from aoc_api import get_input

lines = get_input(1)

# part 1
def part1():
    sum = 0
    for line in lines:
        for char in line:
            if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                left = char
                break

        for char in reversed(line):
            if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                right = char
                break

        print(left, right)
        val = int(f"{left}{right}")
        sum += val

    print(sum)

#part 2
def part2():
    sum = 0
    values = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    for line in lines:
        lfinds = [(value, line.find(value)) for value in values]
        rfinds = [(value, line.rfind(value)) for value in values]
        left = min(filter(lambda find: find[1] != -1, lfinds), key=lambda find: find[1])
        right = max(filter(lambda find: find[1] != -1, rfinds), key=lambda find: find[1])

        value = int(f'{values[left[0]]}{values[right[0]]}')
        sum += value

        print(line, left[0], right[0], value)
    print(sum)

part2()