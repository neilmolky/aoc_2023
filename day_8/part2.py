from collections import deque
from math import lcm

# only additional consideration on this round is first, to pop the initial chalenge solution into a function in order to use it repeatedly
# second use lcm to find the lowest comon multiple of all the solutions (the length of the dirs reppeating pattern should be included)

i1 = len("HFF")
i2 = len("HFF = (")
i3 = len("HFF = (HRR")
i4 = len("HFF = (HRR, ")
i5 = len("HFF = (HRR, BSG")

nodes = {}
for i, line in enumerate(open("data.txt")):
    if i < 1:
        dirs = deque([int(l == "R") for l in line.strip()], len(line.strip())) # we can rotate a deque and set it to be fixed size making it easier to check 
    elif i > 1:
        name = line[:i1]
        left = line[i2:i3]
        right = line[i4:i5]
        nodes[name] = (left, right)

def find_path(root, dirs):
    i = 0
    while root[2] != "Z":
        dir = dirs.popleft()
        dirs.append(dir)
        root = nodes[root][dir]
        i += 1
    return i


lengths = [len(dirs)]
for n in nodes:
    if n[2] == "A":
        l = find_path(n, dirs.copy())
        lengths.append(l)
print(lcm(*lengths))

