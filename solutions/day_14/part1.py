from functools import cache
from enum import Enum

class Direction(Enum):
    # bits represent weight index, pos index and is_start respectively
    # (i, j) represents a position and directions each store a binary representation of range details
    North = int("11", 2)
    West = int("101", 2)
    South = int("10", 2)
    East = int("100", 2)

def weight_index(direction):
    return int(bool(direction.value & int("100", 2)))

def pos_index(direction):
    return int(bool(direction.value & int("10", 2)))

def range_orientation(direction):
    if is_start(direction):
        return 1
    return -1

def is_start(direction):
    return direction.value & int("1", 2)

def rebuild(direction, pos, weight):
    if weight_index(direction):
        return (pos, weight)
    return (weight, pos)

def calc_sum(rolls, arr_size, d):
    weight = arr_size[weight_index(d)]
    total = 0
    for i in range(arr_size[0]):
        for j in range(arr_size[1]):
            if (i, j) in rolls:
                total += weight + ((i, j)[weight_index(d)] * -range_orientation(d))
    return total

def show(rolls, blocks, arr_size):
    for i in range(arr_size[0]):
        for j in range(arr_size[1]):
            if (i, j) in rolls:
                print("O", end="")
            elif (i, j) in blocks:
                print("#", end="")
            else:
                print(".", end="")
        print()

def roll_loop(rolls: set[(int, int)], blocks: set[(int, int)], d: Direction, arr_size: (int, int)):
    new_rolls = set()
    length = arr_size[weight_index(d)]

    # each pos_index represents a line rolling in the same direction
    for pos in range(arr_size[pos_index(d)]):
        # initialise the range and limit
        start = 0 if is_start(d) else length
        stop = length if is_start(d) else -1
        limit = 0 if is_start(d) else length - 1
        for weight in range(start, stop, range_orientation(d)):
            if rebuild(d, pos, weight) in rolls:
                # add blocks in order they were encountered, the limit will increase by the number added
                new_rolls.add(rebuild(d, pos, limit))
                limit += range_orientation(d)
            if rebuild(d, pos, weight) in blocks:
                # the limit will increase to the blok + the direction of the range
                limit = weight+range_orientation(d) 
    return set(new_rolls)


def solve(filename):
    blocks, rolls = set(), set()
    for i, line in enumerate(open(filename)):
        for j, char in enumerate(line.strip()):
            if char == "#":
                blocks.add((i, j))
            elif char == "O":
                rolls.add((i, j))
    arr_size = (i+1, j+1)
    d = Direction.North
    n = roll_loop(rolls, blocks, d, arr_size)
    print(calc_sum(n, arr_size, d))

if __name__ == "__main__":
    solve("test1.txt")
