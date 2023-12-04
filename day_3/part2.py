from math import prod

number_list = []
gears = dict()
# because we will chech for neighbors identity in symbols

arr = [line.strip() for line in open("data.txt")]
max_idx = height, width = (len(arr), len(arr[0]))

for i, row in enumerate(arr):
    number = []
    for j, char in enumerate(row):
        if char.isdigit() and (len(number) == 0 or number[-1][1] + 1 == j):
            number.append((i, j))
        elif char.isdigit():
            number_list.append(number.copy())
            number = [(i, j)]
        elif char == "*":
            gears[(i, j)] = []
    if len(number) > 0:
        number_list.append(number)

for n in number_list:
    gear_factor = False
    for pos in n:
        for i in range (pos[0] - 1, pos[0] + 2):
            for j in range(pos[1] - 1, pos[1] + 2):
                if (i, j) in gears:
                    gear_factor = (i, j)
    if gear_factor:
        gears[gear_factor].append(int("".join([arr[i][j] for i, j in n])))

sum_prod = 0
for nums in gears.values():
    if len(nums) > 1:
        sum_prod += prod(nums)

print(sum_prod)
assert sum_prod == 79842967
