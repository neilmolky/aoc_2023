
valid_moves_sum = 0

game_rules = {"red": 12, "green": 13, "blue": 14}

for line in open("data.txt"):
    game_number, game = tuple(line.strip().split(": "))
    valid = True
    # game is split into pulls each of which may contain multiple colours
    for pull in game.split("; "):
        for number, colour in [tuple(move.split(" ")) for move in pull.split(", ")]:
            if game_rules[colour] < int(number):
                valid=False
                break
    if valid:
        valid_moves_sum += int(game_number.split(" ")[1])
print(valid_moves_sum)
assert valid_moves_sum == 2265
        
        
