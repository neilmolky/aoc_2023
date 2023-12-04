number_list = []
symbols = set()  
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
        elif char != ".":
            symbols.add((i, j))
    if len(number) > 0:
        number_list.append(number)

total = 0
for n in number_list:
    for pos in n:
        part = False
        for i in range (pos[0] - 1, pos[0] + 2):
            for j in range(pos[1] - 1, pos[1] + 2):
                if (i, j) in symbols:
                    part = True
        if part:
            total += int("".join([arr[i][j] for i, j in n]))
            break

print(total)
assert total == 532445

