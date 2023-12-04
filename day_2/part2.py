with open("data.txt", "r") as file:
    power_sum = 0
    for line in file:
        power = 1
        fewest = {"red": 0, "green": 0, "blue": 0}
        moves = line.strip().split(": ")[1]
        for pull in moves.split("; "):
            for number, colour in [tuple(move.split(" ")) for move in pull.split(", ")]:
                if fewest[colour] < int(number):
                    fewest[colour] =int(number)
        for v in fewest.values():
            power *= v
        power_sum += power
        
    print(power_sum)