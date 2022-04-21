import time
import random
from pyswip import Prolog

prolog = Prolog()
# prolog.consult("agent1.pl")
prolog.consult("BestOfSSP6-Agent.pl")



# ----------------------------------------------------------------------------------
# All agent.pl Functions
def reborn():
    list(prolog.query("reborn"))

def confounded():
    print(bool(list(prolog.query("confounded"))))

def stench():
    return list(prolog.query(f"stench(X, Y)"))

def tingle():
    return list(prolog.query(f"tingle(X, Y)"))

def glitter():
    return list(prolog.query(f"glitter(X, Y)"))

def wall():
    return list(prolog.query(f"wall(X, Y)"))

def wumpus():
    return list(prolog.query(f"wumpus(X, Y)"))

def portal():
    return list(prolog.query(f"portal(X, Y)"))

def visited_at():
    return list(prolog.query(f"visited(X, Y)"))

def safe_at():
    return list(prolog.query(f"safe(X, Y)"))

def numcoins():
    c = list(prolog.query("numcoins(N)"))
    numCoins = c[0]['N']
    return numCoins

def hasarrow():
    arrow = bool(list(prolog.query("hasarrow")))
    return arrow

def wumpus_dead():
    wumpus_condition = bool(list(prolog.query('wumpus_dead')))
    return wumpus_condition

def current():
    global rel_X, rel_Y, rel_Dir
    cur = list(prolog.query("current(X, Y, Dir)"))
    # print("\nCurrent Relative X: ", c[0]['X'])
    # print("\nCurrent Relative X: ", c[0]['Y'])
    # print("\nCurrent Relative X: ", c[0]['Dir'])
    rel_X = cur[0]['X']
    rel_Y = cur[0]['Y']
    rel_Dir = cur[0]['Dir']

def move(A, L):
    list(prolog.query(f"move({A}, {L})"))

def explore():
    explore_list = list(prolog.query("explore(L)"))
    return explore_list

def reposition(L):
    list(prolog.query(f"reposition({L})"))

# Agent Movements and percept actions
def move_forward():
    c = list(prolog.query("moveforward([off, off, off, off, off, off])"))

def turn_left():
    c = list(prolog.query("turnleft"))

def turn_right():
    c = list(prolog.query("turnright"))

def pickup():
    list(prolog.query("pickup"))

def has_coin():
    coin = list(prolog.query("has_coin(Result)"))
    result = (coin[0]['Result'] == 'true')
    return result

def shoot():
    shoot = bool(list(prolog.query("shoot")))
    if(shoot):
        print("Shot arrow!")
    else:
        print("Cannot shoot!")

def visited():
     visited_list = list(prolog.query("visited(X, Y)"))
     print("\nAll Visited Cells: ", visited_list)

def safe():
    safe_list = list(prolog.query("safe(X, Y)"))
    print("\nAll Safe Cells: ", safe_list)

# -------------------------------------------------------------------------
# Global Variables

ROWTOTAL = 7
COLTOTAL = 6
OBJECTS = ['W', 'P', '#']
AGENT_ORIENTATION = ['North', 'East', 'South', 'West']

# Initialise World Map: ROWTOTAL * COLTOTAL
MAP_WORLD = [['#', '#', '#', '#', '#', '#'],
            ['#', 'P', 'C', '', '', '#'],
            ['#', '', 'W', '', 'C', '#'],
            ['#', 'P', '', '', '', '#'],
            ['#', '', '', '#', '', '#'],
            ['#', 'P', '', '', 'C', '#'],
            ['#', '#', '#', '#', '#', '#']]


# Agent variables
# World Map Variables
starting_pt = 0
wumpus_location = set()
portal_locations = set()
coin_locations = set()

# Create 3x3 cells in each World Map cells 
World_MAP = [ [ 
            ['.', '.', '.', ' ', '?', ' ', '.', '.', '.']
            for b in range(COLTOTAL)] 
            for a in range(ROWTOTAL)]


# Absolute Map
abs_DIR = ''
abs_X = ''
abs_Y = ''

# ------------------------------------------------------------------------
# Perceptions used by agent
# Init with Confundus On
Perception = ["on", "off", "off", "off", "off", "off"]
# Prints Perception at current cell
def print_Perception():
    global Perception

    for index, value in enumerate(Perception):
        if (index == 0):
            match(value):
                case('on'):
                    print("Confounded-", end='')
                case('off'):
                    print("C-", end="")
        
        elif (index == 1):
            match(value):
                case('on'):
                    print("Stench-", end='')
                case('off'):
                    print("S-", end="")

        elif (index == 2):
            match(value):
                case('on'):
                    print("Tingle-", end='')
                case('off'):
                    print("T-", end="")
    
        elif (index == 3):
            match(value):
                case('on'):
                    print("Glitter-", end='')
                case('off'):
                    print("G-", end="")

        elif (index == 4):
            match(value):
                case('on'):
                    print("Bump-", end='')
                case('off'):
                    print("B-", end='')

        elif (index == 5):
            match(value):
                case('on'):
                    print("Scream", end='')
                case('off'):
                    print("S", end='')
    print()
    print()

# Creation of initial Absolute Map
agent_abs_map = [ [ 
                ['.', '.', '.', ' ', '?', ' ', '.', '.', '.']
                for b in range(COLTOTAL)]
                for a in range(ROWTOTAL)]

# Absolute Positions according to agent's knowledge
stench_abs = set()
tingle_abs = set()
wumpus_abs = set()
portal_abs = set()
glitter_abs = set()
wall_abs = set()
visited_abs = set()
safe_abs = set()

# ---------------------------------------------------------------------
# World Map functions
# Reset World characteristics
def reset_everything():
    #Reset Absolute World
    global stench_abs, tingle_abs, glitter_abs, wumpus_abs, portal_abs, wall_abs, safe_abs, visited_abs
    stench_abs = set()
    tingle_abs = set()
    wumpus_abs = set()
    portal_abs = set()
    glitter_abs = set()
    wall_abs = set()
    visited_abs = set()
    safe_abs = set()

#Called once after initialization of Overview World Map
#Display Overview of World Map
def print_Overview_World():
    global World_MAP
    
    print()
    print('<'*2 + "  Overview World Map  " + '>'*2 +"\n")
    print(' ' * 10 + '-' * 49)
    for outerRows in range(len(World_MAP)):
        for j in range(3):
            print(' ' * 10 + '|', end = '')
            for outerColumns in World_MAP[outerRows]:
                for index in range(3):
                    print(' ' + str(outerColumns[index + j*3]), end='')
                print(' |', end='')
            print()
        print(' ' * 10 + '-' * 49)

    print("\n"+'*'*75)

# -----------------------------------------------------------------------------------------
# Driver Functions
# Initialise
# Create Absolute World Map
def create_abs_map():
    global World_MAP, wumpus_location, portal_locations, coin_locations
    
    #Index, object
    for (rowIndex, row) in enumerate(MAP_WORLD):
        for (colIndex, col) in enumerate(row):
            North = rowIndex + 1
            South = rowIndex - 1
            East = colIndex + 1
            West = colIndex - 1
            
            #Add Wumpus---------------------------------------------------------------------
            if col == "W":
                for index in range(9):
                    World_MAP[rowIndex][colIndex][index] = 'W' 
                wumpus_location.add((rowIndex, colIndex))  
                #Add Stench and ensure no other objects in same cell
                #North of Wumpus
                if (North < ROWTOTAL) and MAP_WORLD[North][colIndex] not in OBJECTS:
                    World_MAP[North][colIndex][1] = '='
                #South of Wumpus
                if (South > 0) and MAP_WORLD[South][colIndex] not in OBJECTS:
                    World_MAP[South][colIndex][1] = '='
                #East of Wumpus
                if (East < COLTOTAL) and MAP_WORLD[rowIndex][East] not in OBJECTS:
                    World_MAP[rowIndex][East][1] = '='
                #West of Wumpus
                if (West > 0) and MAP_WORLD[rowIndex][West] not in OBJECTS:
                    World_MAP[rowIndex][West][1] = '='

            #Add Tingle---------------------------------------------------------------------
            elif col == "P":
                portal_locations.add((rowIndex, colIndex))       
                for index in range(9):
                    World_MAP[rowIndex][colIndex][index] = 'P'
                #North of Portal
                if (North < ROWTOTAL) and MAP_WORLD[North][colIndex] not in OBJECTS:
                    World_MAP[North][colIndex][2] = 'T'
                #South of Portal
                if (South > 0) and MAP_WORLD[South][colIndex] not in OBJECTS:
                    World_MAP[South][colIndex][2] = 'T'
                #East of Portal
                if (East < COLTOTAL) and MAP_WORLD[rowIndex][East] not in OBJECTS:
                    World_MAP[rowIndex][East][2] = 'T'
                #West of Portal
                if (West > 0) and MAP_WORLD[rowIndex][West] not in OBJECTS:
                    World_MAP[rowIndex][West][2] = 'T'

            #Coin
            elif col == "C":
                coin_locations.add((rowIndex, colIndex))
                World_MAP[rowIndex][colIndex][6] = '*'       
            
            #Wall
            if col == '#':
                for index in range(9):
                    World_MAP[rowIndex][colIndex][index] = '#'

# ------------------------------------------------------------------------------
# Agent spawn points
spawn_X = ''
spawn_Y = ''

# X_offset is the offset for columns and Y_offset is offset for rows
X_offset = 1
Y_offset = -1
EW_flag = False

# Get all valid spawn spots
def valid_spawn_locations():
    valid_locations = []
    for (r, row) in enumerate(MAP_WORLD):
        for (c, column) in enumerate(row):
            if column == '' or column == 'C':
                #print(r,c)
                valid_locations.append((r, c))
    return valid_locations

# Spawn in random location
def spawn_agent_random():
    global spawn_X, spawn_Y, abs_X, abs_Y
    # (spawn_Y, spawn_X) = random.choice(valid_spawn_locations())
    spawn_Y, spawn_X = 3,3
    abs_Y, abs_X = spawn_Y, spawn_X

    global abs_DIR, EW_flag, X_offset, Y_offset
    abs_DIR = random.choice(AGENT_ORIENTATION)
    match abs_DIR:
        case('North'):
            Y_offset = -1
            EW_flag = False
        case('South'):
            Y_offset = 1
            EW_flag = False
        case('East'):
            X_offset = 1
            EW_flag = True
        case('West'):
            X_offset = -1
            EW_flag = True

# ---------------------------------------------------------------------------
# Set agent location, Perception and Update absolute agent map
def set_Abs_Agent():
    global abs_X, abs_Y, abs_DIR, agent_abs_map, Perception
    agent_Orientation = ''
    match(abs_DIR):
        case('North'):
            agent_Orientation = '∧'
        case('South'):
            agent_Orientation = 'V'
        case('East'):
            agent_Orientation = '>'
        case('West'):
            agent_Orientation = '<'
        
    agent_abs_map[abs_Y][abs_X][3] = '-'
    agent_abs_map[abs_Y][abs_X][5] = '-'
    agent_abs_map[abs_Y][abs_X][4] = agent_Orientation

    # set Perception
    for index, percept in enumerate(Perception):
        if(percept == 'on'):
            if(index == 0):
                #set Confundus
                agent_abs_map[abs_Y][abs_X][0] = '%'
            elif(index == 4):
                #set Bump
                agent_abs_map[abs_Y][abs_X][7] = 'B'
                #set Scream
            elif(index == 5):
                agent_abs_map[abs_Y][abs_X][8] = '@'

# Update Absolute Map based on after Action
def update_Abs_Agent():
    global agent_abs_map, stench_abs, tingle_abs, glitter_abs, wumpus_abs, portal_abs, wall_abs
    agent_abs_map = [ [ 
                    ['.', '.', '.', ' ', '?', ' ', '.', '.', '.']
                    for b in range(COLTOTAL)]
                    for a in range(ROWTOTAL)]
    
    for (row, column) in wumpus_abs:
        # Check whether possible wumpus and possible portal in same cell
        # U to indicate both adjacent to agent
        if  (row, column) not in portal_abs:
            agent_abs_map[row][column][5] = '-'
            agent_abs_map[row][column][3] = '-'
            agent_abs_map[row][column][4] = 'W'
        else:
            agent_abs_map[row][column][5] = '-'
            agent_abs_map[row][column][3] = '-'
            agent_abs_map[row][column][4] = 'U'

    #Both in same cell considered above, indicate O only if possible portal
    for (row, column) in portal_abs:
        if (row, column) not in wumpus_abs:
            agent_abs_map[row][column][4] = 'O'

    # Set Stench & Tingle cells
    for (row, column) in stench_abs:
        agent_abs_map[row][column][1] = '='
    
    for (row, column) in tingle_abs:
        agent_abs_map[row][column][2] = 'T'


    for (row, column) in glitter_abs:
        agent_abs_map[row][column][6] = '*'

    # Set walls
    for (row, column) in wall_abs:
        for index in range(9):
            agent_abs_map[row][column][index] = '#'

    # Set safe & visited cells
    for (row, column) in safe_abs:
        agent_abs_map[row][column][4] = 's'
    
    for (row, column) in visited_abs:
        agent_abs_map[row][column][4] = 'S'
    
    # Set absolute agent position and Perception
    set_Abs_Agent()

# Print Agent Absolute Map
def print_Absolute_Map():
    global agent_abs_map
    update_Abs_Agent()

    print()
    print('<'*2 + "  AGENT ABSOLUTE WORLD Map " + '>'*2 +"\n")
    print(' ' * 10 + '-' * 49)
    for outerRows in range(len(agent_abs_map)):
        for j in range(3):
            print(' ' * 10 + '|', end = '')
            for outerColumns in agent_abs_map[outerRows]:
                for index in range(3):
                    print(' ' + str(outerColumns[index + j*3]), end='')
                print(' |', end='')
            print()
        print(' ' * 10 + '-' * 49)

    print("\n"+'*'*75)

# Convert relative to absolute coords
rel_Dir = 'rnorth'
rel_X =  0
rel_Y = 0

def determine_abs_position(rel_X, rel_Y):
    if not EW_flag:
        return spawn_Y + Y_offset * rel_X, spawn_X - Y_offset * rel_Y
    else:
        return spawn_Y + X_offset * rel_Y, spawn_X + X_offset * rel_X

def define_abs_position():
    global abs_X, abs_Y, rel_X, rel_Y, spawn_X, spawn_Y
    current()
    abs_Y, abs_X = determine_abs_position(rel_Y, rel_X)

# ----------------------------------------------------------------------------------
# Printing Relative Position
def transform(x,y):
    maxCOL_ROW = max(COLTOTAL,ROWTOTAL)
    return x+maxCOL_ROW, y+maxCOL_ROW

def returnlist(rel_Objects):
    list = []
    for item in rel_Objects:
        X = item.get('X')
        Y = item.get('Y')
        list.append([X,Y])
    return list

def set_relative_Agent(agent_relative_map):
    global rel_X, rel_Y, rel_Dir, Perception

    agent_Orientation = ''
    #Why?
    match(rel_Dir):
        case('rnorth'):
            agent_Orientation = '>'
        case('rsouth'):
            agent_Orientation = '<'
        case('reast'):
            agent_Orientation = 'V'
        case('rwest'):
            agent_Orientation = '∧'
        case(_):
            agent_Orientation = '.'

    rel_Y, rel_X = transform(rel_Y,rel_X)
        
    agent_relative_map[rel_X][rel_Y][3] = '-'
    agent_relative_map[rel_X][rel_Y][5] = '-'
    agent_relative_map[rel_X][rel_Y][4] = agent_Orientation


def print_Relative_Map():
    rel_column, rel_row = transform(COLTOTAL, ROWTOTAL)
    agent_relative_map = [ [ 
                         ['.', '.', '.', ' ', '?', ' ', '.', '.', '.']
                         for b in range(rel_row)]
                         for a in range(rel_column)]
    rel_wumpus = wumpus()
    rel_portal = portal()
    rel_stench = stench()
    rel_tingle = tingle()
    rel_glitter = glitter()
    rel_wall = wall()
    rel_visited = visited_at()
    rel_safe = safe_at()

    wumpus_list = returnlist(rel_wumpus)
    portal_list = returnlist(rel_portal)
    stench_list = returnlist(rel_stench)
    tingle_list = returnlist(rel_tingle)
    glitter_list = returnlist(rel_glitter)
    wall_list = returnlist(rel_wall)
    portal_list = returnlist(rel_portal)
    visited_list = returnlist(rel_visited)
    safe_list = returnlist(rel_safe)


    print("Relative Stench: ", stench_list)
    print("Relative Portal: ", portal_list)
    print("Relative Wall: ", wall_list)
    print("Relative Visited: ", visited_list)    
    print("Relative Safe: ", safe_list)

    for [y, x] in wumpus_list:
        if  [y, x] not in portal_list:
            y, x = transform(y,x)
            agent_relative_map[y][x][5] = '-'
            agent_relative_map[y][x][3] = '-'
            agent_relative_map[y][x][4] = 'W'
        else:
            y, x = transform(y,x)
            agent_relative_map[y][x][5] = '-'
            agent_relative_map[y][x][3] = '-'
            agent_relative_map[y][x][4] = 'U'

    for (y, x) in portal_list:
        if (y, x) not in wumpus_list:
            y, x = transform(y,x)
            agent_relative_map[y][x][4] = 'O'

    # Set safe/visited cells
    for [y, x] in safe_list:
        y, x = transform(y,x)
        agent_relative_map[y][x][4] = 's'
    
    for [y, x] in visited_list:
        y, x = transform(y,x)
        agent_relative_map[y][x][4] = 'S'

    for [y, x] in glitter_list:
        y, x = transform(y,x)
        agent_relative_map[y][x][6] = '*'

    for [y, x] in stench_list:
        y, x = transform(y,x)
        agent_relative_map[y][x][1] = '='
    
    for [y, x] in tingle_list:
        y, x = transform(y,x)
        agent_relative_map[y][x][2] = 'T'
    
    # Set walls
    for [y, x] in wall_list:
        y, x = transform(y,x)       
        for i in range(9):
            agent_relative_map[y][x][i] = '#'

    #Set agent location on relative map
    set_relative_Agent(agent_relative_map)

    print()
    print('<'*2 + "  AGENT'S RELATIVE WORLD MAP  " + '>'*2 +"\n")
    print('-' * 57)
    for outerRows in range(len(agent_relative_map)):
        for j in range(3):
            print('|', end = '')
            for outerColumns in agent_relative_map[outerRows]:
                for index in range(3):
                    print('' + str(outerColumns[index + j*3]), end='')
                print('|', end='')
            print()
        print('-' * 57)

    print("\n"+'*'*75)

# ----------------------------------------------------------------
# Update cell Perception
def update_current_cell_Perception():
    global Perception, World_MAP, abs_X, abs_Y, starting_pt, coin_locations
    Perception = ["off", "off", "off", "off", "off", "off"] 
    # set Confounded
    if(starting_pt == 0):
        Perception[0] = 'on'
    # set Stench
    if(World_MAP[abs_Y][abs_X][1] == '='):
        Perception[1] = 'on'
    # set Tingle
    if(World_MAP[abs_Y][abs_X][2] == 'T'):
        Perception[2] = 'on'
    # set Glitter
    if(World_MAP[abs_Y][abs_X][6] == '*' and (abs_Y, abs_X) in coin_locations):
        Perception[3] = 'on'

# Used with move forward to see if agent bumps into wall
def get_forward_cell_Perception():
    global Perception, World_MAP
    global rel_X, rel_Y, rel_Dir
    current()
    #Get forward cell coordinates
    newX, newY  = rel_X, rel_Y
    match(rel_Dir):
        case('rnorth'):
            newY += 1
        case('rsouth'):
            newY -= 1
        case('reast'):
            newX += 1
        case('rwest'):
            newX -= 1

    newY, newX = determine_abs_position(newY, newX)
    # If bump, Perception does not change except set Bump
    if(World_MAP[newY][newX][1] == '#'):
        Perception[4] = 'on'
        return

    Perception = ["off", "off", "off", "off", "off", "off"] 
    # set Stench
    if(World_MAP[newY][newX][1] == '='):
        Perception[1] = 'on'
    # set Tingle
    if(World_MAP[newY][newX][2] == 'T'):
        Perception[2] = 'on'
    # set Glitter
    if(World_MAP[newY][newX][6] == '*' and (newY, newX) in coin_locations):
        Perception[3] = 'on'


# Verify if wumpus died after firing arrow
def verify_wumpus_death():
    global abs_X, abs_Y, abs_DIR, wumpus_location
    
    # Check wumpus is in direction of agent (Shoot done in direction of agent)
    for (row, column) in wumpus_location:
        # If Wumpus in same column
        if column == abs_X:
            if row > abs_Y:
                if abs_DIR == 'South':
                    return True
            else:
                if abs_DIR == 'North':
                    return True
        # If Wumpus in same row
        elif row == abs_Y:
            if column > abs_X:
                if abs_DIR == 'East':
                    return True
            else:
                if abs_DIR == 'West':
                    return True
        
    return False

# Function to check if wumpus got killed after shooting
def check_if_wumpus_killed():
    global Perception, wumpus_location
    if verify_wumpus_death():
        # set Scream
        Perception[5] = 'on'
        print("Wumpus death!")
        wumpus_location = set()

# --------------------------------------------------------
# Agent Exploration and Steps
def get_move():
    c = explore()
    return c[0]['L']


# Update driver's knowledge of Agent's knowledge
def update_driver_KB():
    global stench_abs, tingle_abs, glitter_abs, wumpus_abs, portal_abs, wall_abs, safe_abs, visited_abs
    # Reset all sets:
    wumpus_abs = set()
    portal_abs = set()
    safe_abs = set()
    glitter_abs = set()

    # Update Stench, Tingle, Glitter, Walls, Wumpus, Portal, Visited, Safe cells
    for ST in stench():
        stench_abs.add((determine_abs_position(ST['Y'], ST['X'])))

    for T in tingle():
        tingle_abs.add((determine_abs_position(T['Y'], T['X'])))

    for G in glitter():
        glitter_abs.add((determine_abs_position(G['Y'], G['X'])))
    print("Gold location: ", glitter_abs)

    for W in wall():
        wall_abs.add((determine_abs_position(W['Y'], W['X'])))
    print("Walls location: ", wall_abs)

    for wum in wumpus():
        wumpus_abs.add((determine_abs_position(wum['Y'], wum['X'])))

    for por in portal():
        portal_abs.add((determine_abs_position(por['Y'], por['X'])))

    for visit in visited_at():
        visited_abs.add((determine_abs_position(visit['Y'], visit['X'])))
    print("Visited Cells: ", visited_abs)

    for safe in safe_at():
        safe_abs.add((determine_abs_position(safe['Y'], safe['X'])))
    print("Safe Cells: ", safe_abs)

# Update Status and Knowledge based of driver
def update_status():
    define_abs_position()
    update_driver_KB()

# ----------------------------------------------------------------------------------
# Controller for user to pick actions or explore
def controller():
    global abs_DIR, rel_X, rel_Y, rel_Dir, Perception, coin_locations, wumpus_location
    explore_flag = False
    explore_steps = []
    choice = 0
    while choice != -1:
        if choice == 0:
            print("Agent Active and ready to Move")

        print()
        print("Pick an action for the agent:")
        print("1 - Agent Explore")
        print("2 - Move Forward")
        print("3 - Turn Left")
        print("4 - Turn Right")
        print("5 - Grab Coin")
        print("6 - Shoot")
        print("7 - Continue (Searches for more coins)")
        print("8 - Exits World")


        print()
        # If user input choice 1,
        # Check if there are any steps
        if(explore_flag):
            if len(explore_steps) == 0:
                explore_steps = get_move()
                print("Next Move: ", explore_steps)
                    
            try:
                action = explore_steps.pop(0)
                if action == 'moveforward':
                    choice = 2
                elif action == 'turnleft':
                    choice = 3
                elif action == 'turnright':
                    choice = 4
                elif action == 'pickup':
                    choice = 5
                elif action == 'shoot':
                    choice = 6
                elif action == 'continue':
                    choice = 7
                elif action == 'end':
                    choice = 8
                
            except:
                explore_flag = False                    
                print("All safe cells explored! Agent currently situated at Origin!")
                choice = int(input("Choice: "))
                
            
        else:
            try:
                print("Agent suggest Actions: ", get_move())
            except:
                print("Agent has no suggestions or is at origin...")
            
            choice = int(input("Choice: "))
        

        if choice == 1:
            explore_flag = True
            print("Agent begin Exploring ")

        elif choice == 2:
            print("Agent move forward...")
            get_forward_cell_Perception()            

            move('moveforward', Perception)
            move("turnright", Perception)
            move("turnleft", Perception)

        elif choice == 3:
            update_current_cell_Perception()
            move("turnleft", Perception)
            abs_DIR = AGENT_ORIENTATION[(AGENT_ORIENTATION.index(abs_DIR)-1)%4]
            print("Agent Turning Left...")
        
        elif choice == 4:
            update_current_cell_Perception()
            move("turnright", Perception)
            abs_DIR = AGENT_ORIENTATION[(AGENT_ORIENTATION.index(abs_DIR)+1)%4]
            print("Agent Turning Right...")
        
        elif choice == 5:
            update_current_cell_Perception()
            print("Agent Pick Coin...")
            move("pickup", Perception)
            try:
                coin_locations.remove((abs_Y, abs_X))
            except:
                pass
            update_current_cell_Perception()
                
        
        elif choice == 6:
            update_current_cell_Perception()
        
            print("Agent Shoot arrow...")

            # Check if has arrow
            if hasarrow():
                # Check if wumpus in direction of arrow shot and is killed
                check_if_wumpus_killed()
                move("shoot", Perception)
            else:
                print("No arrows left")

        elif choice == 7:
            print("There are still unvisited cells")
            choice = 1

        elif choice == 8:
            print("Exited from World")
            choice = -1

        else:
            "Invalid Option!"
            continue

        update_status()

        # Check if entered Wumpus cell
        # Stop Exploration if entered Wumpus cell
        if  (abs_Y, abs_X) in wumpus_location:
            print("Yikes... Agent devoured! Game Over!")
            break

        # Check Whether Agent entered portal
        # Reposition If Agent entered portal
        elif (abs_Y, abs_X) in portal_locations:
            print("Entered Portal. Repositioning...")
            reposition_abs_map()

        # Else
        else:        
            print("\nPerception after action: ", end='')
            print_Perception()
            print("Agent Arrow: ", hasarrow())
            # print("Coins Collected: ", numcoins())          
            print_both_maps()
        
        # time.sleep(0.75)



# Remove maps here for better visualization
def print_both_maps():
    #
    print_Absolute_Map()
    print_Relative_Map()

#   Spawn agent and initialize absolute map
def reposition_abs_map():
    global Perception, starting_pt
    starting_pt = 0
    reset_everything()

    spawn_agent_random()
    
    update_current_cell_Perception()
    # Call Agent reposition
    reposition(Perception)
    update_status()
    
    print_both_maps()
    print("Current Perception: ", print_Perception())
    starting_pt = 1

def start_wumpus_game():
   # Set Agent start and print initial map
   #Call Reborn
    reborn()

    # Create Absolute Map
    create_abs_map()

    # Display Absolute Map
    print_Overview_World()

    # Call reposition
    # Spawn Randomly
    reposition_abs_map()

    # Loop controller
    controller()


# Start Game
start_wumpus_game()





