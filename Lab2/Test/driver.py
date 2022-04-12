
import random
from matplotlib.pyplot import get
from numpy import flip, transpose
from pyswip import Prolog
# import pyswip

prolog = Prolog()

prolog.consult("agent.pl")



# NEED CHANGE DEPENDING ON THE PROPER ORDER
NUMROW = 7
NUMCOL = 6
ENTITIES = ['W', 'P', 'C', '#']
DIRECTIONS = ['n', 'e', 's', 'w']
# Map - Row by Column (7 x 6)
MAP = [  #0   1    2    3    4    5
       ['#', '#', '#', '#', '#', '#'],  #0
       ['#', '', '', '', '', '#'],      #1
       ['#', 'P', '', 'P', '', '#'],    #2
       ['#', 'W', '', '', 'C', '#'],    #3
       ['#', '', '', '', '', '#'],      #4
       ['#', 'P', '', '', '', '#'],     #5
       ['#', '#', '#', '#', '#', '#']]  #6

# MAP = transpose([
#        ['#', '#', '#', '#', '#', '#'],
#        ['#', '', '', '', '', '#'],
#        ['#', 'P', '', 'P', '', '#'],
#        ['#', 'W', '', '', 'C', '#'],
#        ['#', '', '', '', '', '#'],
#        ['#', 'P', '', '', '', '#'],
#        ['#', '#', '#', '#', '#', '#']])

# Create 7 x 6 x 9 [] * 7 
absMap = [ [ ['.', '.', '.', ' ', '?', ' ', '.', '.', '.'] for b in range(NUMCOL)] for a in range(NUMROW) ]
agent_abs_map = [ [ ['.', '.', '.', ' ', '?', ' ', '.', '.', '.'] for b in range(NUMCOL)] for a in range(NUMROW) ]


# To call upon populate helper
first_start = 0

# Agent variables - X is column, Y is rows!

# offsets to account for relative positioning
xOffset = 1
yOffset = -1
flipped = False



rDir = 'rnorth'
rX =  0
rY = 0


spawnX = ''
spawnY = ''

absDir = ''
absX = ''
absY = ''

stench_pos = set()
tingle_pos = set()
glitter_pos = set()
wumpus_pos = set()
portal_pos = set()
wall_pos = set()
safe_pos = set()
visited_pos = set()



senses = ["on", "off", "off", "off", "off", "off"]

# AGENT FUNCTIONS
# Reborn to reset agent
def reborn():
    list(prolog.query("reborn"))


def stench_at():
    return list(prolog.query(f"stench(X, Y)"))

def tingle_at():
    return list(prolog.query(f"tingle(X, Y)"))

def glitter_at():
    return list(prolog.query(f"glitter(X, Y)"))

def wall_at():
    return list(prolog.query(f"wall(X, Y)"))

def wumpus_at():
    return list(prolog.query(f"wumpus(X, Y)"))

def portal_at():
    return list(prolog.query(f"portal(X, Y)"))

def visited_at():
    return list(prolog.query(f"visited(X, Y)"))

def safe_at():
    return list(prolog.query(f"safe(X, Y)"))


def localisation():
    global stench_pos, tingle_pos, glitter_pos, wumpus_pos, portal_pos, wall_pos, safe_pos, visited_pos
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
    c = list(prolog.query(f"wall(X, Y)"))
    print()
    print("Wall at: ", c)

    # Scream
    c = list(prolog.query(f"wumpus_dead(What)"))
    print()
    print("Wumpus dead: ", c)


    # Wumpus Position
    c = list(prolog.query(f"wumpus(X, Y)"))
    print()
    print("Wumpus maybe at: ", c)

    # Portal Position
    c = list(prolog.query(f"portal(X, Y)"))
    print()
    print("Portal maybe at: ", c)



# Move Forward
def move_forward():
    print("\nMoving Forward")
    c = list(prolog.query("moveforward([off, off, off, off, off, off])"))

def turn_left():
    # print("\nTurning Left")
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
    global rX, rY, rDir
    c = list(prolog.query("current(X, Y, Dir)"))
    # print("\nCurrent Position: ", c[0])
    rX = c[0]['X']
    rY = c[0]['Y']
    rDir = c[0]['Dir']



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


# DRIVER FUNCTIONS
# Initialisation

# Get spawnable spots
def spawn_spots():
    spawns = []
    for (r, row) in enumerate(MAP):
        for (c, col) in enumerate(row):
            if col == '' or col == 'C':
                spawns.append((r, c))
    return spawns

# Spawn
def random_spawn():
    global spawnX, spawnY, absX, absY
    (spawnY, spawnX) = random.choice(spawn_spots())
    absY, absX = spawnY, spawnX
    

# random Direction
def random_direction():
    global absDir, flipped, xOffset, yOffset
    absDir = random.choice(DIRECTIONS)
    if absDir == 'e' or absDir == 'w':
        flipped = True
        if absDir == 'w':
            xOffset = -1
        else:
            xOffset = 1
    
    else:
        flipped = False
        if absDir == 'n':
            yOffset = -1

        else:
            yOffset = 1

# Symbol Populater for default map - made my own modifications
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

    elif col == "C":
            # for i in range(9):
                absMap[rIndex][cIndex][6] = '*'       


    # Scream
    # Walls
    if col == '#':
        for i in range(9):
            absMap[rIndex][cIndex][i] = '#'
    


def create_abs_map():
    global absMap
    
    for (rIndex, row) in enumerate(MAP):
        for (cIndex, col) in enumerate(row):
            populate_helper(absMap, rIndex, cIndex, col)

def print__map():
    for z in range(7):
        for j in range(3):
            for col in absMap[z]:
                for i in range(3):
                    print(col[i + j*3], end='')
                print(' | ', end='')
            print()
        print('-'*35)

def set_abs_agent_location():
    global absX, absY, absDir, agent_abs_map, senses
    facing = ''
    if absDir == 'n':
        facing = '∧'
    elif absDir == 's':
        facing = '∨'
    elif absDir == 'e':
        facing = '>'
    else:
        facing = '<'
    agent_abs_map[absY][absX][3] = '-'
    agent_abs_map[absY][absX][5] = '-'
    agent_abs_map[absY][absX][4] = facing


    # set senses
    for i, el in enumerate(senses):
        if(el == 'on'):
            if(i == 0):
                agent_abs_map[absY][absX][0] = '%'
            elif(i == 1):
                agent_abs_map[absY][absX][1] = '='
            elif(i == 2):
                agent_abs_map[absY][absX][2] = 'T'
            elif(i == 3):
                agent_abs_map[absY][absX][6] = '*'
            elif(i == 4):
                agent_abs_map[absY][absX][7] = 'B'
            elif(i == 5):
                agent_abs_map[absY][absX][8] = '@'

    




def update_absolute_agent_map():
    global agent_abs_map, stench_pos, tingle_pos, glitter_pos, wumpus_pos, portal_pos, wall_pos
    agent_abs_map = [ [ ['.', '.', '.', ' ', '?', ' ', '.', '.', '.'] for b in range(NUMCOL)] for a in range(NUMROW) ]
    for (y, x) in wumpus_pos:
        if  (y, x) not in portal_pos:
            agent_abs_map[y][x][5] = '-'
            agent_abs_map[y][x][3] = '-'
            agent_abs_map[y][x][4] = 'W'
        else:
            agent_abs_map[y][x][5] = '-'
            agent_abs_map[y][x][3] = '-'
            agent_abs_map[y][x][4] = 'U'

    for (y, x) in portal_pos:
        if (y, x) not in wumpus_pos:
            agent_abs_map[y][x][4] = 'O'

    # Set safe/visited cells
    for (y, x) in safe_pos:
        agent_abs_map[y][x][4] = 's'
    
    for (y, x) in visited_pos:
        agent_abs_map[y][x][4] = 'S'

    # Set walls
    for (y, x) in wall_pos:
        for i in range(9):
            agent_abs_map[y][x][i] = '#'


    # Set absolute agent position and senses
    set_abs_agent_location()


def print_Absolute_Map():
    global agent_abs_map
    update_absolute_agent_map()
       
    print()
    
    # Printing the default map - made my own modifications
    for z in range(7):
        for j in range(3):
            for col in agent_abs_map[z]:
                for i in range(3):
                    print(col[i + j*3], end='')
                print(' | ', end='')
            print()
        print('-'*35)




def pretend_moveforward():
    global rX, rY, rDir
    newX, newY  = rX, rY
    if(rDir == 'rnorth'):
        newY += 1
    elif rDir == 'rsouth':
        newY -= 1
    elif rDir == 'reast':
        newX += 1
    else:
        newX -= 1

    return newY, newX

def get_abs_coord(relativeXY):
    if not flipped:
        return spawnY + yOffset*relativeXY[0], spawnX - yOffset*relativeXY[1]
    else:
        return spawnY + xOffset*relativeXY[1], spawnX + xOffset * relativeXY[0]

def redefine_abs_coord():
    global absX, absY, rX, rY, spawnX, spawnY
    current()
    absY, absX = get_abs_coord((rY, rX))
    
def update_current_senses():
    global senses, absMap, absX, absY, first_start
    senses = ["off", "off", "off", "off", "off", "off"] 
    # Confounded??
    if(first_start == 0):
        senses[0] = 'on'

    # Turn on stench
    if(absMap[absY][absX][1] == '='):
        senses[1] = 'on'
    # Turn on tingle
    if(absMap[absY][absX][2] == 'T'):
        senses[2] = 'on'
    # Turn on glitter
    if(absMap[absY][absX][6] == '*'):
        senses[3] = 'on'
    # Turn on scream??
    # if(absMap[newY][newX][1] == 'T'):
    #     senses[1] = 'on'


# Linking agent and driver functions
def get_next_senses():
    global senses, absMap
    current()
    newY, newX = get_abs_coord(pretend_moveforward())
    # If bump, all senses remain the same except bump turned on
    if(absMap[newY][newX][1] == '#'):
        senses[4] = 'on'
        return

    senses = ["off", "off", "off", "off", "off", "off"] 
    

    # Confounded??
    # if(absMap[newY][newX][1] == 'T'):
    #     senses[1] = 'on'

    # Turn on stench
    if(absMap[newY][newX][1] == '='):
        senses[1] = 'on'
    # Turn on tingle
    if(absMap[newY][newX][2] == 'T'):
        senses[2] = 'on'
    # Turn on glitter
    if(absMap[newY][newX][6] == '*'):
        senses[3] = 'on'
    # Turn on scream??
    # if(absMap[newY][newX][1] == 'T'):
    #     senses[1] = 'on'



# TO DO
def query_agent():
    global stench_pos, tingle_pos, glitter_pos, wumpus_pos, portal_pos, wall_pos, safe_pos, visited_pos 
    # Reset all sets:
    wumpus_pos = set()
    portal_pos = set()



    # print("Stench: ", stench_at())
    for sol in stench_at():
        stench_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    print("STENCH POS: ", stench_pos)

    # print("Tingle: ", tingle_at())
    for sol in tingle_at():
        tingle_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    print("TINGLE POS: ", tingle_pos)

    # print("Glitter: ", glitter_at())
    for sol in glitter_at():
        glitter_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    print("GLITTER POS: ", glitter_pos)

    # print("Walls: ", wall_at())
    for sol in wall_at():
        wall_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    print("WALLS POS: ", wall_pos)

    # print("Wumpus: ", wumpus_at())
    for sol in wumpus_at():
        wumpus_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    print("WUMPUS POS: ", wumpus_pos)

    print("Portal: ", portal_at())
    for sol in portal_at():
        portal_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    print("PORTAL POS: ", portal_pos)

    # print("Visited: ", visited_at())
    for sol in visited_at():
        visited_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    print("VISITED POS: ", visited_pos)

    # print("Safe: ", safe_at())
    for sol in safe_at():
        safe_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    print("SAFE POS: ", safe_pos)


    
def update_all():
    redefine_abs_coord()
    query_agent()





def controls():
    print__map()
    print_Absolute_Map()
    global absDir, rX, rY, rDir, first_start
    choice = 1
    first_start = 1
    while choice != 6:
        print(f"Relative Y: {rY} Relative X: {rX} Relative Dir: {rDir}")
        print('''
            1) Move Forward
            2) Turn Left
            3) Turn Right
            4) Pick Up Coin
            5) Shoot
                ''')
        choice = int(input("Choice: "))
        if choice == 1:
            print("Attempting to move forward...")
            # Check if front is a wall
            get_next_senses()            
            print(senses)
            move('moveforward', senses)
            # update_current_senses()

        elif choice == 2:
            # turn_left()
            update_current_senses()
            move("turnleft", senses)
            absDir = DIRECTIONS[(DIRECTIONS.index(absDir)-1)%4]
            print("Turning Left")
        
        elif choice == 3:
            # turn_right()
            update_current_senses()
            move("turnright", senses)
            absDir = DIRECTIONS[(DIRECTIONS.index(absDir)+1)%4]
            print("Turning Right")
        
        elif choice == 4:
            update_current_senses()
            print("Attempting to pick up coin...")
        
        elif choice == 5:
            update_current_senses()
            print("Attempting to shot arrow...")

        print("BEFORE")
        update_all()

        print("AFTER")
        print__map()
        print_Absolute_Map()
        
        

    # Check if entered portal or WUMPUS


def start_wumpus():
    reborn()
    create_abs_map()
    random_spawn()
    random_direction()
    update_current_senses()


start_wumpus()

controls()

# print("WUMPUS: ", wumpus_at())


# reborn()
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


