from collections import deque, defaultdict

# initial ideas

# first ideas highlighted the importance of finding the loops and storing:
# start/end (which will be identical) 
# pattern of moves [which will store the pattern length too]
# do we assume loops will have more than 1 pattern through a different set of L-R directions?
# can we check if a pattern is relevant by comparing it to the input pattern [LRLRLRLRLRLRLRLRLRLRLRLRLRLRL] not relevant for pattern [LRRLRLRLRLRLRLRL]

# create trees
# parse input into trees
# store the loops (pattern of moves, start&end) while parsing input

# treat this as a pathfinding problem, 
# find all the paths that do have a loop (pattern of moves, start&end)
# check the input to see if the patterns match any of the found paths to reduce the size of the problem space

# the input wasn't actually complicated enough to require these considerations so today took longer than it should have

# the final solution was only a while condition to check if node is found and circling the list until found, literally no other optimisation required


i1 = len("HFF")  # My laziness knows no bounds, why count this yourself when the computer can do it for you [=
i2 = len("HFF = (")
i3 = len("HFF = (HRR")
i4 = len("HFF = (HRR, ")
i5 = len("HFF = (HRR, BSG")

nodes = {}
for i, line in enumerate(open("data.txt")):
    if i < 1:
        dirs = deque([int(l == "R") for l in line.strip()], len(line.strip())) # we can rotate a deque and set it to be fixed size making it efficient to check 
    elif i > 1:
        name = line[:i1]
        left = line[i2:i3]
        right = line[i4:i5]
        nodes[name] = (left, right)
root = "AAA"
i = 0
while root != "ZZZ":
    dir = dirs.popleft()
    dirs.append(dir)
    root = nodes[root][dir]
    i += 1
print(i)

