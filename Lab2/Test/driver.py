from pyswip import Prolog
# import pyswip



prolog = Prolog()

prolog.consult("agent.pl")

# Boolean data
# c = bool(list(prolog.query("boy(a)")))

# Dictionary Data 
# c = list(prolog.query("boy(a)"))

# c = list(prolog.query("move(What, [no, no, no, on, no, no, no])"))

prolog.query("reborn")
c = bool(list(prolog.query("hasarrow")))
print(c)