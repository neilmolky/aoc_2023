from functools import cache
from enum import Enum

class Direction(Enum):
    North = int("11", 2)
    East = int("100", 2)
    South = int("10", 2)
    West = int("101", 2)

def weight_index(direction):
    if direction.value & int("100", 2):
        return 1
    return 0
    
def pos_index(direction):
    if direction.value & int("10", 2):
        return 1
    return 0

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

def roll_line(rolls: frozenset[int], blocks: frozenset[int], d: Direction, length: int):
    indices = []
    start = 0 if is_start(d) else length
    stop = length if is_start(d) else -1
    limit = 0 if is_start(d) else length - 1
    for i in range(start, stop, range_orientation(d)):
        if i in rolls:
            indices.append(limit)
            limit += range_orientation(d)
        if i in blocks:
            limit = i+range_orientation(d)
    return indices

def roll_loop(rolls: frozenset[(int, int)], blocks: frozenset[(int, int)], d: Direction, arr_size: (int, int)):
    new_rolls = []
    # each pos_index represents a line rolling in the same direction
    for i in range(arr_size[pos_index(d)]):
        # the subset of integers for rolls and blocks goes into the function (reduced cache size)
        subset_rolls = frozenset({r[weight_index(d)] for r in rolls if r[pos_index(d)] == i})
        subset_blocks = frozenset({b[weight_index(d)] for b in blocks if b[pos_index(d)] == i})
        # a collection integers returned is reconstruced into a set 
        int_set = roll_line(subset_rolls, subset_blocks, d, arr_size[weight_index(d)])
        # intersection is added 
        new_rolls.extend([rebuild(d, i, j) for j in int_set])
    return frozenset(new_rolls)

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
    n = roll_loop(frozenset(rolls), frozenset(blocks), d, arr_size)
    print(calc_sum(n, arr_size, d))
    show(rolls, blocks, arr_size)
    print()
    show(n, blocks, arr_size)

if __name__ == "__main__":
    solve("test1.txt")
