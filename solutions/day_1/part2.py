# assuming zero does not occur in strings
# dict is dual purpose, serving to turn words into respective digits but also provide the full spectrum of matches when using items
digit_dict = {
    "one": "1", 
    "two": "2", 
    "three": "3", 
    "four": "4", 
    "five": "5", 
    "six": "6", 
    "seven": "7", 
    "eight": "8", 
    "nine": "9"
}

# assuming each line has 1 number, start will be lazily set for the first number, end will be greedily set for every number
def getDigit(s):
    start, end = None, None
    for i in range(len(s)):
         for word, number in digit_dict.items():
            if s[i:].startswith(word) or s[i] == number:
                if start is None:
                    start = number
                end = number
    return int(start + end)


total = 0
for line in open("data.txt"):
    total += getDigit(line.strip())
print(total)
assert total == 55358