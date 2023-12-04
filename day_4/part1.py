
cache = {0: 0, 1: 1}

def lottorial(i: int)->int:
    if i not in cache:
        cache[i] = lottorial(i-1) * 2
    return cache[i] 

total = 0
for line in open("data.txt"):
    p1, p2 = tuple(line.split(":")[1].strip().split("|"))
    wins = len(set({c for c in p1.strip().split(" ") if c != ""}).intersection(set({c for c in p2.strip().split(" ") if c != ""})))
    total += lottorial(wins)

print(total)
assert total == 24542
