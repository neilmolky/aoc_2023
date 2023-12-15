from functools import cache
from solutions.day_14.part1 import Direction, roll_loop, show, calc_sum

def washing_machine(rolls, blocks, arr_size):
    n = roll_loop(rolls, blocks, Direction.North, arr_size)
    w = roll_loop(n, blocks, Direction.West, arr_size)
    s = roll_loop(w, blocks, Direction.South, arr_size)
    e = roll_loop(s, blocks, Direction.East, arr_size)
    return e

def solve(filename):
    blocks, rolls = set(), set()
    for i, line in enumerate(open(filename)):
        for j, char in enumerate(line.strip()):
            if char == "#":
                blocks.add((i, j))
            elif char == "O":
                rolls.add((i, j))
    arr_size = (i+1, j+1)
    itter_rolls = frozenset(rolls)
    itter_blocks = frozenset(blocks)

    stored_loops = []
    start = 1000000000
    loopIdx = False
    while not loopIdx:
        stored_loops.append(itter_rolls)
        itter_rolls = washing_machine(itter_rolls, itter_blocks, arr_size)
        for i, past in enumerate(stored_loops):
            if past == itter_rolls:

                loopIdx = True
                break
        start -= 1
    print(start)
    print(i)
    infinite_loop = stored_loops[i:]

    print(calc_sum(infinite_loop[start % len(infinite_loop)], arr_size, Direction.North))

if __name__ == "__main__":
    solve("test1.txt")
