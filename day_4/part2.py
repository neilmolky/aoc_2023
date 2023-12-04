
from collections import defaultdict

copies = defaultdict(lambda: 1)

def jackpot(this_ticket: int, wins: int):  
    for i in range(this_ticket, this_ticket + wins):
        copies[i + 1] += copies[this_ticket]
    return copies[this_ticket] # will initialise copies with 1 if no wins

for i, line in enumerate(open("data.txt"), start=1):
    p1, p2 = tuple(line.split(":")[1].strip().split("|"))
    wins = len(set({c for c in p1.strip().split(" ") if c != ""}).intersection(set({c for c in p2.strip().split(" ") if c != ""})))
    jackpot(i, wins)

print(sum(copies.values()))
assert sum(copies.values()) == 8736438