
from pyswip import Prolog
# import pyswip

prolog = Prolog()

prolog.consult("Agent.pl")

NUMROW = 7
NUMCOL = 6

ENTITIES = ['W', 'P', 'C', '#']


# Map
MAP = [
       ['#', '#', '#', '#', '#', '#'],
       ['#', '', '', '', '', '#'],
       ['#', 'P', '', 'P', '', '#'],
       ['#', 'W', '', '', 'C', '#'],
       ['#', '', '', '', '', '#'],
       ['#', 'P', '', '', '', '#'],
       ['#', '#', '#', '#', '#', '#']]


def populate_helper(absMap, rIndex, cIndex, col):

    newRight = cIndex + 1
    newLeft = cIndex - 1
    newUp = rIndex + 1
    newDown = rIndex - 1
    # Confounded

    # Stench
    if col == "W":  
        for i in range(9):
            absMap[rIndex][cIndex][i] = 'W'     
        # Right
        if (newRight < NUMCOL) and MAP[rIndex][newRight] not in ENTITIES:
            absMap[rIndex][newRight][1] = '='
        # LEFT
        if (newLeft > 0) and MAP[rIndex][newLeft] not in  ENTITIES:
            absMap[rIndex][newLeft][1] = '='
        # Right
        if (newUp < NUMROW) and MAP[newUp][cIndex] not in  ENTITIES:
            absMap[newUp][cIndex][1] = '='
        # Right
        if (newDown > 0) and MAP[newDown][cIndex] not in  ENTITIES:
            absMap[newDown][cIndex][1] = '='

    # Tingle
    elif col == "P":       
        for i in range(9):
            absMap[rIndex][cIndex][i] = 'P'
        # Right
        if (newRight < NUMCOL) and MAP[rIndex][newRight] not in  ENTITIES:
            absMap[rIndex][newRight][2] = 'T'
        # LEFT
        if (newLeft > 0) and MAP[rIndex][newLeft] not in  ENTITIES:
            absMap[rIndex][newLeft][2] = 'T'
        # Right
        if (newUp < NUMROW) and MAP[newUp][cIndex] not in  ENTITIES:
            absMap[newUp][cIndex][2] = 'T'
        # Right
        if (newDown > 0) and MAP[newDown][cIndex] not in  ENTITIES:
            absMap[newDown][cIndex][2] = 'T'
    # Entity
    # Percept
    # Entity (again?)
    # Glitter
    elif col == "C":
            for i in range(9):
                absMap[rIndex][cIndex][i] = '*'       


    # Scream
    # Walls
    if col == '#':
        for i in range(9):
            absMap[rIndex][cIndex][i] = '#'

def print_Absolute_Map():
    # Create 7 x 6 x 9 [] * 7 
    absMap = [ [ ['.', '.', '.', '.', '.', '.', '.', '.', '.'] for b in range(6)] for a in range(7) ]
    print()
    for (rIndex, row) in enumerate(MAP):
        for (cIndex, col) in enumerate(row):
            populate_helper(absMap, rIndex, cIndex, col)




    for z in range(7):
        for j in range(3):
            for col in absMap[z]:
                for i in range(3):
                    print(col[i + j*3], end='')
                print(' | ', end='')
            print()
        print('-'*35)


    

print_Absolute_Map()


# Reborn to reset agent
def reborn():
    list(prolog.query("reborn"))

def localisation():
    # Confunded
    c = list(prolog.query(f"confounded(What)"))
    print()
    print("Confounded: ", c)

    # Stench
    c = list(prolog.query(f"stench(X, Y)"))
    print()
    print("Stench at: ", c)

    # Tingle
    c = list(prolog.query(f"tingle(X, Y)"))
    print()
    print("Tingle at: ", c)

    # Glitter
    c = list(prolog.query(f"glitter(X, Y)"))
    print()
    print("Glitter at: ", c)

    # Bump
    c = list(prolog.query(f"is_wall(X, Y)"))
    print()
    print("Wall at: ", c)

    # Scream
    c = list(prolog.query(f"wumpus_dead(What)"))
    print()
    print("Wumpus dead: ", c)


# Move Forward
def move_forward():
    print("\nMoving Forward")
    c = list(prolog.query("moveforward([off, off, off, off, off, off])"))

def turn_left():
    print("\nTurning Left")
    c = list(prolog.query("turnleft"))

def turn_right():
    print("\nTurning Right")
    c = list(prolog.query("turnright"))


def test_hasarrow():
    c = bool(list(prolog.query("hasarrow")))
    print("\nHas arrow: ", c)


def shoot():
    c = bool(list(prolog.query("shoot")))
    if(c):
        print("Shot arrow!")
    else:
        print("Cannot shoot!")

def current():
    c = list(prolog.query("current(X, Y, Dir)"))
    print("\nCurrent Position: ", c)


def visited():
     c = list(prolog.query("visited(X, Y)"))
     print("\nVisited Cells: ", c)

def safe():
    c = list(prolog.query("safe(X, Y)"))
    print("\nSafe Cells: ", c)

def move(A, L):
    list(prolog.query(f"move({A}, {L})"))

def reposition(L):
    list(prolog.query(f"reposition({L})"))

reborn()
# testShooting()
# testPickup()
# test_hasarrow()
# shoot()
# test_hasarrow()
# shoot()
# testMoveForward()

# current()
# visited()
# move_forward()
# current()
# turn_right()
# current()
# move_forward()
# current()
# move_forward()
# current()
# turn_left()
# current()

# move("moveforward", ["off", "off", "off", "off", "off", "off"])
# visited()
# # safe()
# move("moveforward", ["off", "on", "off", "off", "off", "off"])
# visited()
# safe()

# move("moveforward", ["on", "off", "off", "off", "off", "off"])

# print("After confounded")
# reposition(["on", "on", "on", "on", "off", "off"])

# visited()
# safe()

# localisation()


