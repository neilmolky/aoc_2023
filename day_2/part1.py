
valid_moves_sum = 0
base_game = {"red": 12, "green": 13, "blue": 14}
for line in open("data.txt"):
    game, moves = tuple(line.strip().split(": "))
    valid = True
    for pull in moves.split("; "):
        if not valid:
            break
        for number, colour in [tuple(move.split(" ")) for move in pull.split(", ")]:
            if base_game[colour] < int(number):
                valid=False
                break
    if valid:
        valid_moves_sum += int(game.split(" ")[1])
print(valid_moves_sum)
assert valid_moves_sum == 2265
        
        
