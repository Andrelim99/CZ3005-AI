import time
import random
from pyswip import Prolog

prolog = Prolog()
prolog.consult("agent.pl")

NUMROW = 7
NUMCOL = 6
ENTITIES = ['W', 'P', '#']
DIRECTIONS = ['n', 'e', 's', 'w'] # DO NOT CHANGE DIRECTION ORDER
# Map - Row by Column (7 x 6)
MAP = [  #0   1    2    3    4    5
       ['#', '#', '#', '#', '#', '#'],  #0
       ['#', '', '', '', 'P', '#'],      #1
       ['#', 'C', 'W', 'C', '', '#'],    #2
       ['#', '', '', '', 'P', '#'],    #3
       ['#', '', '', '#', '', '#'],      #4
       ['#', '', '', 'C', 'P', '#'],     #5
       ['#', '#', '#', '#', '#', '#']]  #6


# Create 7 x 6 x 9 [] * 7 
absMap = [ [ ['.', '.', '.', ' ', '?', ' ', '.', '.', '.'] for b in range(NUMCOL)] for a in range(NUMROW) ]
agent_abs_map = [ [ ['.', '.', '.', ' ', '?', ' ', '.', '.', '.'] for b in range(NUMCOL)] for a in range(NUMROW) ]


# World Variables
first_start = 0
actual_wumpus = set()
actual_portals = set()
actual_coin = set()

senses = ["on", "off", "off", "off", "off", "off"]

# Agent variables - X is column, Y is rows!

# offsets to account for relative positioning
xOffset = 1
yOffset = -1
flipped = False


# RELATIVE POSITION
rDir = 'rnorth'
rX =  0
rY = 0


spawnX = ''
spawnY = ''

# ABSOLUTE POSITION
absDir = ''
absX = ''
absY = ''

# SETS OF POSITION OF AGENT'S KNOWLEGE
stench_pos = set()
tingle_pos = set()
glitter_pos = set()
wumpus_pos = set()
portal_pos = set()
wall_pos = set()
safe_pos = set()
visited_pos = set()


r_stench_pos = set()
r_tingle_pos = set()
r_glitter_pos = set()
r_wumpus_pos = set()
r_portal_pos = set()
r_wall_pos = set()
r_safe_pos = set()
r_visited_pos = set()

r_map_rows = 3
r_map_cols = 3

r_x_offset = 1
r_y_offset = 1

def reset_all_positions():
    global stench_pos, tingle_pos, glitter_pos, wumpus_pos, portal_pos, wall_pos, safe_pos, visited_pos 
    global r_stench_pos, r_tingle_pos, r_glitter_pos, r_wumpus_pos, r_portal_pos, r_wall_pos, r_safe_pos, r_visited_pos
    global r_map_cols, r_map_rows, r_x_offset, r_y_offset
    stench_pos = set()
    tingle_pos = set()
    glitter_pos = set()
    wumpus_pos = set()
    portal_pos = set()
    wall_pos = set()
    safe_pos = set()
    visited_pos = set()

    r_stench_pos = set()
    r_tingle_pos = set()
    r_glitter_pos = set()
    r_wumpus_pos = set()
    r_portal_pos = set()
    r_wall_pos = set()
    r_safe_pos = set()
    r_visited_pos = set()

    r_map_rows = 3
    r_map_cols = 3

    r_x_offset = 1
    r_y_offset = 1

# AGENT FUNCTIONS
# Reborn to reset agent
def reborn():
    list(prolog.query("reborn"))

def is_confounded():
    print(bool(list(prolog.query("confounded"))))

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

def confirm_not_wumpus_at():
    return list(prolog.query(f"confirm_not_wumpus(X, Y)"))

def confirm_not_portal_at():
    return list(prolog.query(f"confirm_not_portal(X, Y)"))

def numcoins():
    c = list(prolog.query("numcoins(N)"))
    n = c[0]['N']
    return n

def hasarrow():
    c = bool(list(prolog.query("hasarrow")))
    # print("\nHas arrow: ", c)
    return c

def wumpus_dead():
    # print(list(prolog.query('wumpus_dead(WHAT)')))
    return bool(list(prolog.query('wumpus_dead')))

def current():
    global rX, rY, rDir
    c = list(prolog.query("current(X, Y, Dir)"))
    # print("\nCurrent Position: ", c[0])
    rX = c[0]['X']
    rY = c[0]['Y']
    rDir = c[0]['Dir']

def move(A, L):
    list(prolog.query(f"move({A}, {L})"))

def explore():
    # print("MOVES: ", list(prolog.query("explore(L)")))
    return list(prolog.query("explore(L)"))

def reposition(L):
    list(prolog.query(f"reposition({L})"))


# ACTIONS TESTING - Not actually used for calling
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
    c = list(prolog.query("moveforward([off, off, off, off, off, off])"))

def turn_left():
    # print("\nTurning Left")
    c = list(prolog.query("turnleft"))

def turn_right():
    print("\nTurning Right")
    c = list(prolog.query("turnright"))

def pickup():
    list(prolog.query("pickup"))

def has_coin():
    c = list(prolog.query("has_coin(Result)"))
    result = (c[0]['Result'] == 'true')
    # print(result)
    return result

def shoot():
    c = bool(list(prolog.query("shoot")))
    if(c):
        print("Shot arrow!")
    else:
        print("Cannot shoot!")

def visited():
     c = list(prolog.query("visited(X, Y)"))
     print("\nVisited Cells: ", c)

def safe():
    c = list(prolog.query("safe(X, Y)"))
    print("\nSafe Cells: ", c)


def solve():
    global rX, rY
    c = list(prolog.query(f"solve([{rX}, {rY}], Action, Sol)"))
    print("\nPath: ", c)
# -----------------------------------------------

# DRIVER FUNCTIONS

# INITIALISATION
# Get spawnable spots
def spawn_spots():
    spawns = []
    for (r, row) in enumerate(MAP):
        for (c, col) in enumerate(row):
            if col == '' or col == 'C':
                spawns.append((r, c))
    return spawns

# Spawn - Currently has a default spawn location
def random_spawn():
    global spawnX, spawnY, absX, absY
    (spawnY, spawnX) = random.choice(spawn_spots())
    # spawnY, spawnX = 4, 1
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
    global actual_wumpus, actual_portals, actual_coin
    newRight = cIndex + 1
    newLeft = cIndex - 1
    newUp = rIndex + 1
    newDown = rIndex - 1
    # Confounded

    # Stench
    if col == "W":
        actual_wumpus.add((rIndex, cIndex))
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
        actual_portals.add((rIndex, cIndex))       
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
        actual_coin.add((rIndex, cIndex))
        # if not has_coin(): 
            # print('\nPlacing Coin..')
            # for i in range(9):
        absMap[rIndex][cIndex][6] = '*'       
        # else:
            # absMap[rIndex][cIndex][6] = '.'


    # Scream
    # Walls
    if col == '#':
        for i in range(9):
            absMap[rIndex][cIndex][i] = '#'

# ----------------------------

# WORLD MAP
def create_abs_map():
    global absMap    
    for (rIndex, row) in enumerate(MAP):
        for (cIndex, col) in enumerate(row):
            populate_helper(absMap, rIndex, cIndex, col)

def print__map():
    global absMap
    print("\n"+'#'*16 + " WORLD MAP " + '#'*16 +"\n")
    for z in range(7):
        for j in range(3):
            for col in absMap[z]:
                for i in range(3):
                    print(col[i + j*3], end='')
                print('  ', end='')
            print()
        print()
    print('#'*46)
# ----------------------------

# PRINT AGENT'S ABSOLUTE MAP FUNCTIONS
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
            # elif(i == 1):
            #     agent_abs_map[absY][absX][1] = '='
            # elif(i == 2):
            #     agent_abs_map[absY][absX][2] = 'T'
            # elif(i == 3):
            #     agent_abs_map[absY][absX][6] = '*'
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

    for (y, x) in glitter_pos:
        # if not has_coin():
        agent_abs_map[y][x][6] = '*'

    for (y, x) in stench_pos:
        agent_abs_map[y][x][1] = '='
    
    for (y, x) in tingle_pos:
        agent_abs_map[y][x][2] = 'T'

        


    # Set walls
    for (y, x) in wall_pos:
        for i in range(9):
            agent_abs_map[y][x][i] = '#'


    # Set absolute agent position and senses
    set_abs_agent_location()


def print_Absolute_Map():
    global agent_abs_map
    update_absolute_agent_map()
    print('#'*12 + " AGENT'S ABSOLUTE MAP " + '#'*12 +"\n")
    # Printing the default map - made my own modifications
    for z in range(7):
        for j in range(3):
            for col in agent_abs_map[z]:
                for i in range(3):
                    print(col[i + j*3], end='')
                print('  ', end='')
            print()
        print()

    print("\n"+'#'*46)

# ----------------------------
# PRINT AGENT'S RELATIVE MAP FUNCTIONS - TO DO!
agent_relative_map = [ [ ['.', '.', '.', ' ', '?', ' ', '.', '.', '.'] for b in range(r_map_cols)] for a in range(r_map_rows) ]

def recalulate_numRC():
    global r_map_rows, r_map_cols, rY, rX

    if (rY, rX) in r_visited_pos or (rY, rX) == (0, 0):
        return

    if rDir == 'rnorth' or rDir == 'rsouth':
        r_map_rows += 2

    else:
        r_map_cols += 2

def calulate_r_offset():
    global r_y_offset, r_x_offset
    r_y_offset = int(r_map_rows/2)
    r_x_offset = int(r_map_cols/2)


def calculate_r_postion(y, x):
    return r_y_offset - y, x + r_x_offset


def set_relative_agent_location():
    global rX, rY, rDir, agent_relative_map, senses
    y, x = calculate_r_postion(rY, rX)
    facing = ''
    if rDir == 'rnorth':
        facing = '∧'
    elif rDir == 'rsouth':
        facing = '∨'
    elif rDir == 'reast':
        facing = '>'
    else:
        facing = '<'
    agent_relative_map[y][x][3] = '-'
    agent_relative_map[y][x][5] = '-'
    agent_relative_map[y][x][4] = facing


    # set senses
    for i, el in enumerate(senses):
        if(el == 'on'):
            if(i == 0):
                agent_relative_map[y][x][0] = '%'
            # elif(i == 1):
            #     agent_relative_map[y][x][1] = '='
            # elif(i == 2):
            #     agent_relative_map[y][x][2] = 'T'
            # elif(i == 3):
            #     agent_relative_map[y][x][6] = '*'
            elif(i == 4):
                agent_relative_map[y][x][7] = 'B'
            elif(i == 5):
                agent_relative_map[y][x][8] = '@'


def update_relative_agent_map():
    global r_map_cols, r_map_rows, agent_relative_map, r_stench_pos, r_tingle_pos, r_glitter_pos, r_wumpus_pos, r_portal_pos, r_wall_pos, r_safe_pos, r_visited_pos
    agent_relative_map = [ [ ['.', '.', '.', ' ', '?', ' ', '.', '.', '.'] for b in range(r_map_cols)] for a in range(r_map_rows) ]
    for (y, x) in r_wumpus_pos:
        if  (y, x) not in r_portal_pos:
            y, x = calculate_r_postion(y, x)
            agent_relative_map[y][x][5] = '-'
            agent_relative_map[y][x][3] = '-'
            agent_relative_map[y][x][4] = 'W'
        else:
            y, x = calculate_r_postion(y, x)
            agent_relative_map[y][x][5] = '-'
            agent_relative_map[y][x][3] = '-'
            agent_relative_map[y][x][4] = 'U'

    for (y, x) in r_portal_pos:
        if (y, x) not in r_wumpus_pos:
            y, x = calculate_r_postion(y, x)
            agent_relative_map[y][x][4] = 'O'

    # Set safe/visited cells
    for (y, x) in r_safe_pos:
        y, x = calculate_r_postion(y, x)
        # print(y,x)
        agent_relative_map[y][x][4] = 's'
    
    for (y, x) in r_visited_pos:
        y, x = calculate_r_postion(y, x)
        agent_relative_map[y][x][4] = 'S'

    for (y, x) in r_glitter_pos:
        # if not has_coin():
        y, x = calculate_r_postion(y, x)
        agent_relative_map[y][x][6] = '*'

    for (y, x) in r_stench_pos:
        y, x = calculate_r_postion(y, x)
        agent_relative_map[y][x][1] = '='
    
    for (y, x) in r_tingle_pos:
        y, x = calculate_r_postion(y, x)
        agent_relative_map[y][x][2] = 'T'
    
        


    # Set walls
    for (y, x) in r_wall_pos:        
        y, x = calculate_r_postion(y, x)
        for i in range(9):
            agent_relative_map[y][x][i] = '#'


    # Set absolute agent position and senses
    set_relative_agent_location()


def print_Relative_Map():
    global agent_relative_map, r_map_rows
    update_relative_agent_map()
    print('#'*12 + " AGENT'S RELATIVE MAP " + '#'*12 +"\n")
    # Printing the default map - made my own modifications
    for z in range(r_map_rows):
        for j in range(3):
            for col in agent_relative_map[z]:
                for i in range(3):
                    print(col[i + j*3], end='')
                print('  ', end='')
            print()
        # print('-'*35)
        print()

    print("\n"+'#'*46)



# ----------------------------


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


# Convert relative to absolute coords
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
    global senses, absMap, absX, absY, first_start, actual_coin
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
    if(absMap[absY][absX][6] == '*' and (absY, absX) in actual_coin):
        senses[3] = 'on'


# Used with move forward to see if agent bumps into wall
def get_next_senses():
    global senses, absMap
    current()
    newY, newX = get_abs_coord(pretend_moveforward())
    # If bump, all senses remain the same except bump turned on
    if(absMap[newY][newX][1] == '#'):
        senses[4] = 'on'
        return

    senses = ["off", "off", "off", "off", "off", "off"] 
    
    # Turn on stench
    if(absMap[newY][newX][1] == '='):
        senses[1] = 'on'
    # Turn on tingle
    if(absMap[newY][newX][2] == 'T'):
        senses[2] = 'on'
    # Turn on glitter
    
    if(absMap[newY][newX][6] == '*' and (newY, newX) in actual_coin):
        senses[3] = 'on'


# CHECK FOR ARROW FIRED - IF WUMPUS IS DEAD
def facing_wumpus():
    global absX, absY, absDir, actual_wumpus
    
    for (y, x) in actual_wumpus:
        # If same col
        if x == absX:
            # Check if agent above or below
            # Wumpus Below, so agent shd face south
            if y > absY:
                if absDir == 's':
                    return True
            else:
                if absDir == 'n':
                    return True
        # OR IF SAME ROW
        elif y == absY:
            if x > absX:
                # Wumpus To the right, so agent shd face east
                if absDir == 'e':
                    return True
            else:
                if absDir == 'w':
                    return True
        
    return False

# Function to check if wumpus got killed after shooting
def check_if_wumpus_killed():
    global senses, actual_wumpus
    if facing_wumpus():
        senses[5] = 'on'
        print("Wumpus has been slain!")
        actual_wumpus = set()

# ----------------------------

def get_move():
    c = explore()
    # print(c)
    # print("GOALS: ", list(prolog.query("goal(G)")))
 
    return c[0]['L']


# Update driver's knowledge of Agent's knowledge.. lmao
def query_agent():
    global stench_pos, tingle_pos, glitter_pos, wumpus_pos, portal_pos, wall_pos, safe_pos, visited_pos
    global r_stench_pos, r_tingle_pos, r_glitter_pos, r_wumpus_pos, r_portal_pos, r_wall_pos, r_safe_pos, r_visited_pos
    # Reset all sets:
    wumpus_pos = set()
    portal_pos = set()
    safe_pos = set()
    glitter_pos = set()

    r_wumpus_pos = set()
    r_portal_pos = set()
    r_safe_pos = set()
    r_glitter_pos = set()



    # print("Stench: ", stench_at())
    for sol in stench_at():
        r_stench_pos.add((sol['Y'], sol['X']))
        stench_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    # print("STENCH POS: ", stench_pos)

    # print("Tingle: ", tingle_at())
    for sol in tingle_at():
        r_tingle_pos.add((sol['Y'], sol['X']))
        tingle_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    # print("TINGLE POS: ", tingle_pos)

    # print("Glitter: ", glitter_at())
    for sol in glitter_at():
        r_glitter_pos.add((sol['Y'], sol['X']))
        glitter_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    # print("GLITTER POS: ", glitter_pos)

    # print("Walls: ", wall_at())
    for sol in wall_at():
        r_wall_pos.add((sol['Y'], sol['X']))
        wall_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    # print("WALLS POS: ", wall_pos)

    # print("Wumpus: ", wumpus_at())
    for sol in wumpus_at():
        r_wumpus_pos.add((sol['Y'], sol['X']))
        wumpus_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    # print("WUMPUS POS: ", wumpus_pos)

    # print("Portal: ", portal_at())
    for sol in portal_at():
        r_portal_pos.add((sol['Y'], sol['X']))
        portal_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    # print("PORTAL POS: ", portal_pos)

    # print("Visited: ", visited_at())
    for sol in visited_at():
        r_visited_pos.add((sol['Y'], sol['X']))
        visited_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    # print("VISITED POS: ", visited_pos)

    # print("Safe: ", safe_at())
    for sol in safe_at():
        r_safe_pos.add((sol['Y'], sol['X']))
        safe_pos.add((get_abs_coord((sol['Y'], sol['X']))))
    # print("SAFE POS: ", safe_pos)

    # print("Not Wumpus at: ", list(prolog.query("confirm_not_wumpus(X, Y)")))
    # tmp = set()
    # for sol in confirm_not_wumpus_at():
    #     tmp.add((get_abs_coord((sol['Y'], sol['X']))))
    # print("NOT WUMPUS POS: ", tmp)

    # tmp = set()
    # for sol in confirm_not_portal_at():
    #     tmp.add((get_abs_coord((sol['Y'], sol['X']))))
    # print("NOT PORTAL POS: ", tmp)

    
def print_senses():
    global senses
    
    if senses[0] =="on":
        print("Confounded-", end='')
    else:
        print("C-", end="")

    if  senses[1] =="on":
        print("Stench-", end='')
    else:
        print("S-", end="")

    if senses[2] =="on":
        print("Tingle-", end='')
    else:
        print("T-", end="")

    if senses[3] =="on":
        print("Glitter-", end='')
    else:
        print("G-", end="")

    if senses[4] =="on":
        print("Bump-", end='')
    else:
        print("B-", end="")

    if senses[5] =="on":
        print("Scream")
    else:
        print("S")

        
    print()


def update_all():
    redefine_abs_coord()
    recalulate_numRC()
    calulate_r_offset()

    query_agent()





def controls():
    global absDir, rX, rY, rDir, senses, actual_coin, actual_wumpus
    moves = []
    choice = 1
    explore_flag = False
    while choice != -1:
        # print(f"Relative Y: {rY} Relative X: {rX} Relative Dir: {rDir}")
        print('''
Pick an action for the agent:
1) Move Forward
2) Turn Left
3) Turn Right
4) Pick Up Coin
5) Shoot
6) Let the agent explore!
''')
        if(explore_flag):
            if len(moves) == 0:
                moves = get_move()
                print("Next Move: ", moves)

                    
            try:
                mov = moves.pop(0)
                if mov == 'moveforward':
                    choice = 1
                elif mov == 'turnleft':
                    choice = 2
                elif mov == 'turnright':
                    choice = 3
                elif mov == 'pickup':
                    choice = 4
                elif mov == 'shoot':
                    choice = 5
                
            except:
                explore_flag = False                    
                print("Agent has returned to origin, all safe cells explored!")
                choice = int(input("Choice: "))
                
            
        else:
            try:
                print("Agent thinks it should do: ", get_move())
            except:
                print("Agent doesn't know what to do or has returned to origin...")
            
            choice = int(input("Choice: "))    
        
        # time.sleep(1) 
        
        # print("Agent thinks it should do: ", get_move())
       
        
        if choice == 1:
            print("Attempting to move forward...")
            # Check if forward is wall
            get_next_senses()            

            # print(bool(list(prolog.query(f"moveforward({senses})"))))
            move('moveforward', senses)
            move("turnright", senses)
            move("turnleft", senses)
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
            move("pickup", senses)
            # create_abs_map()
            try:
                actual_coin.remove((absY, absX))
            except:
                pass
            update_current_senses()
                
            
        
        elif choice == 5:
            update_current_senses()
        
            print("Attempting to shoot arrow...")

            # Check if has arrow
            if hasarrow():
                # Check if wumpus in direction of arrow shot and is killed
                check_if_wumpus_killed()
                move("shoot", senses)
                # print("WUMPUS DEAD: ", wumpus_dead())
            else:
                print("No arrows to shoot")

        elif choice == 6:
            explore_flag = True
            print("Agent shall begin Exploring...")

        else:
            "Invalid Option!"
            continue

        update_all()
        # Check if entered wumpus cell
        if  (absY, absX) in actual_wumpus:
            print("Oops... Agent has been devoured! Game Over!")
            break

        # check if entered portal
        elif (absY, absX) in actual_portals:
            print("Entered Portal. Repositioning...")
            world_reposition()

        # Else
        else:        
            # print__map()
            print("Has arrow: ", hasarrow())
            # print("Number of coins: ", numcoins())
            print("Senses after action: ", end='')            
            print_senses()
            print_Absolute_Map()
            print_Relative_Map()
            
        

def world_reposition():
    global senses, first_start
    first_start = 0
    # Initialise Agent
    random_spawn()
    random_direction()
    reset_all_positions()
    update_current_senses()
    reposition(senses)
    update_all()
    
    
    print_Absolute_Map()
    print_Relative_Map()   
    print("Current Senses: ", end='')
    print_senses()
    first_start = 1

def start_wumpus():
   # Set Agent start and print initial map
    reborn()
    create_abs_map()
    print__map()

    # Call reposition
    world_reposition()

    # Loop controls
    controls()


# Start Game
start_wumpus()





