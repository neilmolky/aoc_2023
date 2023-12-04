
# extract the digits into a list and the beginning and end index make each number
total = 0
for line in open("data.txt"):
    digits = [d for d in line if d.isdigit()]
    total += int(digits[0] + digits[-1])
print(total)
assert total == 142