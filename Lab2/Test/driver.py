from pyswip import Prolog
# import pyswip



prolog = Prolog()

prolog.consult("test2.pl")

# Boolean data
# c = bool(list(prolog.query("boy(a)")))

# Dictionary Data 
# c = list(prolog.query("boy(a)"))

# c = list(prolog.query("move(What, [no, no, no, on, no, no, no])"))


# Confounded, Stench, Tingle, Glitter, Bump, Scream.
# c = bool(list(prolog.query("gameStart(true)")))
# print()
# print(c)

prolog.query("reborn")
sense = ['off', 'off', 'off', 'on', 'off', 'off', 'off']
# c = bool(list(prolog.query("fired(false)")))
# print()
# print(c)


# Test Shooting
def testShooting():
    c = bool(list(prolog.query(f"hasarrow")))
    print()
    print("Has Arrow?", c)


    c = bool(list(prolog.query(f"move(shoot, {sense})")))
    print()
    print("Can fire?", c)

    c = bool(list(prolog.query(f"move(shoot, {sense})")))
    print()
    print("Can fire again?", c)

def testPickup():
    # Test Pick up coins
    c = bool(list(prolog.query(f"hasCoin")))
    print()
    print("Has Coin?", c)


    c = bool(list(prolog.query(f"move(pickup, {sense})")))
    print()
    print("Should Pick Coin?", c)

    c = bool(list(prolog.query(f"move(pickup, {sense})")))
    print()
    print("Can pick coin again?", c)


def testMoveforward():
    c = list(prolog.query(f"current(WhatX, WhatY, WhatDir)"))
    print()
    print("Current Position: ", c)

    list(prolog.query("move(moveforward, [on, on, off, off])"))        # print()
    # print("IN?", c)
    # prolog.query("move(moveforward, [on, off, off, off])")

    c = list(prolog.query(f"stench(WhatX, WhatY)"))
    print()
    print("Stench Solution?", c)

    c = list(prolog.query(f"tingle(WhatX, WhatY)"))
    print()
    print("Tingle Solution?", c)



# testShooting()
# testPickup()
testMoveforward()