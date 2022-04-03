% Variables that can be changed
:- dynamic([ fired/1,
pickedCoin/1,
current/3,
reborn/0,
gameStart/1]).


gameStart(true).



reborn:-
    gameStart(true),
    retractall(visited(_, _)),
    retractall(wumpus(_, _)),
    retractall(confundus(_, _)),
    retractall(tingle(_, _)),
    retractall(glitter(_, _)),
    retractall(stench(_, _)),
    retractall(safe(_, _)),
    asserta(fired(false)).


reposition(L):-
    retractall(visited(_, _)),
    retractall(wumpus(_, _)),
    retractall(confundus(_, _)),
    retractall(tingle(_, _)),
    retractall(glitter(_, _)),
    retractall(stench(_, _)),
    retractall(safe(_, _)),
    asserta(current(0, 0, rnorth)).

shoot(shoot).
pickup(pickup).
moveforward(moveforward).




% fired(false).



% Shoot - need add more logic to decide if should shoot such as if facing wumpus
move(A, L) :-
    shoot(A),
    hasarrow,
    retract(fired(false)).



% Pick up coin
move(A, L):-
    pickup(A),
    cellContainsCoin(L),
    \+hasCoin,
    asserta(pickedCoin(true)).

cellContainsCoin([_, _, _, E | _]) :-
    E == 'on'.

hasCoin :-
    pickedCoin(true).

% has arrow
hasarrow :-
    fired(false).

    



