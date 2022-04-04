from pyswip import Prolog
# import pyswip

prolog = Prolog()

prolog.consult("Agent.pl")

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
current()
visited()
move_forward()
current()
turn_right()
current()
move_forward()
current()
move_forward()
current()
turn_left()
current()

move("moveforward", ["off", "off", "off", "off", "off", "off"])
visited()
# safe()
move("moveforward", ["off", "on", "off", "off", "off", "off"])
visited()
safe()

move("moveforward", ["on", "off", "off", "off", "off", "off"])

print("After confounded")
reposition(["on", "on", "on", "on", "off", "off"])

visited()
safe()

localisation()


