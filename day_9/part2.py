def diff_check(l: list):
    if sum(l) == 0:
        return 0
    # to get the previous number take the first number instead and subtract the results of diff checker
    return l[0] - diff_check([l[i+1] - l[i] for i in range(len(l)-1)])

print(sum([diff_check([int(s) for s in line.strip().split(" ")]) for line in open("data.txt")]))

