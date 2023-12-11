# initial ideas, pathfind both directions at once checking neighbors
# the pos class will help simplify the coordinate math and checks

class Pos:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __add__(self, other):
        return Pos(self.i + other.i, self.j + other.j)
    
    def __sub__(self, other):
        return Pos(self.i - other.i, self.j - other.j)
    
    def inlimits(self, limiti, limitj):
        return 0 <= self.i < limiti and 0 <= self.j < limitj 
    
    def __eq__(self, other):
        return self.i == other.i and self.j == other.j
    
    def __hash__(self):
        return hash((self.i, self.j))
    
    def __repr__(self):
        return f"Pos({self.i}, {self.j})"

# read the whole map in first as an array of strings (treat it as a 2d array with the sring being a char array)
pipe_map = []
for i, line in enumerate(open("data.txt")):
    if line.find("S") >= 0:
        start = Pos(i, line.index("S"))
    pipe_map.append(line)

limiti, limitj = len(pipe_map), len(line)
neighbors_list = [Pos(0, 1), Pos(1, 0), Pos(-1, 0), Pos(0, -1)]
pipes = {
    "-": {Pos(0, -1), Pos(0, 1)},
    "|": {Pos(-1, 0), Pos(1, 0)},
    "L": {Pos(-1, 0), Pos(0, 1)},
    "7": {Pos(1, 0), Pos(0, -1)},
    "J": {Pos(-1, 0), Pos(0, -1)},
    "F": {Pos(1, 0), Pos(0, 1)},
    ".": set()

}

# functions defined below use the above global variables
def neighbors(pos):   
    pre_filter = [pos + n for n in neighbors_list]
    return [p for p in pre_filter if p.inlimits(limiti, limitj)]

def connecting_pipes(pos):
    # assume pipes will always connect from start in a loop
    return {pos + p for p in pipes[show(pos)]}

def show(pos):
    return pipe_map[pos.i][pos.j]

# part 1 solution
# the visited set contains only pipe Pos values 
visited = {start}
# traveled gets manually incremented
traveled = 0
# keep track of te left and right pointers simultaneously until 
left, right = tuple([p for p in neighbors(start) if start in connecting_pipes(p)])
# change the S char in the pipe_map global variable so it reflecs its actual piece otherwise this char represents a break in the pipe
for char, positions in pipes.items():
    if {left - start, right - start} == positions:
        print(f"resetting S to {char}")
        pipe_map[start.i] = pipe_map[start.i].replace("S", char)
        assert pipe_map[start.i][start.j] != "S"

while not (left in visited or right in visited):
    visited.add(left)
    visited.add(right)
    traveled += 1
    # 
    try:
        left = connecting_pipes(left).difference(visited).pop()
        right = connecting_pipes(right).difference(visited).pop()
    except:
        break

def show(pos):
    return pipe_map[pos.i][pos.j]



print(traveled)

# part 2 solution

# find the top left corner pipe which will by design be an F pipe
# we know that the inside of this piece will be diagonally down and right
# if we travel round the pipe only looking inwards we will find internal spaces/pipes 
# (yes pipes not connected to the loop can be inside the pipe loop, fortunately if they are themselves loops they do not block the inside)
# we use the last and next to create an immutable state for each time we look inwards
# when looking inwards if we find a position that is not in the pipe path we enter a find loop
# in the find loop we will add positions to the inside set


inside = set() # positions which are deffinitely inside
min_i = min(visited, key = lambda x: x.i).i
first_line = {v for v in visited if v.i == min_i}
first_corner = min(first_line, key = lambda x: x.j)

def colourMeDebug(pipe_set, inside_set):
    from termcolor import colored
    # shows the pipemap with tiles considered inside as red
    for i in range(limiti):
        for j in range(limitj):
            if Pos(i, j) in pipe_set:
                print(colored(show(Pos(i, j)), "blue"), end="")
            elif Pos(i, j) in inside_set:
                print(colored(show(Pos(i, j)), "red"), end="")
            else:
                print(show(Pos(i, j)), end="")
        # print()
    print()


def positions_to_check(last_check, last_pos, last_dir, next_pos, next_dir)->list[Pos]:
    # return new tiles to check or the last check if no new tiles to check because we always need a last checked to maintain continuity on the inside
    check_last_dir = last_check - last_pos
    marker = show(next_pos)
    next_dir

    # was inside corner next straight; x == y, return the last check again
    # F-
    # Lx
    if marker in ["|", "-"] and last_check in neighbors(next_pos):
        return [last_check]
    
    # was either an outside corner or straight, next straight
    # either way theres only 1 last check which would be the same either way, x lastcheck, y next check, direction of travel determines the next check
    # y|
    # xL
    elif marker in ["|", "-"]:
        return [last_check + last_dir]
    
    # was an inside corner and next an inside corner; x lastcheck y nextcheck; we want to make the value of last check the diagonal
    # this diagonal will have already been checked or may be part of the pipes
    # next_pos = F, last_pos = L
    # Fx-
    # Ly-
    elif show(last_pos) in ["L", "J", "7", "F"] and next_pos + next_dir == last_check:
        return [last_pos + next_dir]
    
    # was an inside corner next a outside corner x = lastcheck and nextcheck, y = next_check
    # lastpos = J, nextpos = F
    #  y
    # xF-
    # -J
    elif show(last_pos) in ["L", "J", "7", "F"] and next_pos - next_dir == last_check:
        # only need to return y as x already checked
        return [next_pos + last_dir]
    
    # was an outside corner or straight, now an inside corner x = lastcheck and nextcheck
    # nextpos = J lastpos = F
    #  x|
    # -FJ
    elif last_pos + next_dir == last_check:
        return [last_check]
    
    # was an outside corner or straight, now an outside corner or straight
    # nextpos 
    #  y
    # yF
    # xL
    elif last_pos - next_dir == last_check:
        return [last_check + last_dir, next_pos + last_dir]
    
    else:
        raise Exception("Conditions ae not sufficient to find all cases!")


# before sterting the loop we need to populate both the last state and the next state
last_piece = first_corner  # F
last_dir = Pos(0, 1)  # travel right
next_piece = last_piece + last_dir # the next piece will follow the direction of travel
# check the possible next directions by excluding the direction that takes you back to where you came from
next_dir = [d for d in pipes[show(next_piece)] if d + next_piece != last_piece][0]
last_check = last_piece + Pos(1, 1) # set the value of last checked for the corner to enforce only inside checks
# while we haven't actually checked this it will be checked at the last stage of the loop if not beffore then

# loop to move round the perimiter
while next_piece != first_corner:
    newly_added = positions_to_check(last_check, last_piece, last_dir, next_piece, next_dir)
    check_set = {p for p in newly_added if p not in visited and p not in inside}
    # loop to find all neighbours of all values in check_set
    while len(check_set) > 0:
        current_check_pos = check_set.pop()
        inside.add(current_check_pos)
        for n in neighbors(current_check_pos):
            if n not in visited and n not in inside:
                check_set.add(n)
    # update state for next iteration
    last_piece = next_piece
    last_dir = next_dir
    next_piece = last_piece + last_dir
    next_dir = [d for d in pipes[show(next_piece)] if d + next_piece != last_piece][0]
    last_check = newly_added[-1]

colourMeDebug(visited, inside)
print(len(inside))

# reflections: This was prety tough. findig the loop was required for both parts so I didn't split into part 1 and 2 today
# probably worth tidying it up a little. turn this into a package so I can import the required parts where needed
# coud add a run file at the root which accepts cmd line args
# the colourmedubug function was a nice idea for debugging
# there were also many more test cases provided, I used the 2 final ones which are less relevant to part 1
# coding this declaratively means functions are often defined mid file after global variables have been specified, 
# I should deffinitely move the solution parts into functions to tidy this up






    



