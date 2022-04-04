% Variables that can be changed
:- dynamic fired/1,
pickedCoin/1,
current/3,
reborn/0,
gameStart/1,
stench/2,
tingle/2.


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
    assert(fired(false)).


reposition(L):-
    retractall(visited(_, _)),
    retractall(wumpus(_, _)),
    retractall(confundus(_, _)),
    retractall(tingle(_, _)),
    retractall(glitter(_, _)),
    retractall(stench(_, _)),
    retractall(safe(_, _)),
    assert(current(0, 0, rnorth)).

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

maybe_wumpus(X, Y) :-
    \+visited(X, Y), 
    (
        downY is Y + 1, stench(downY, X);
    ).

% Stench Detection
% move(A, [_, E|_]) :-
%     current(WhatY, WhatX, WhatDir),(
%     % Go Relative Up
%     (A == moveforward, E == on, WhatDir == rnorth, UpY is WhatY + 1) -> (assert(stench(UpY, WhatX)));
%     % Go Relative Right
%     (A == moveforward, E == on, WhatDir == reast, RightX is WhatX + 1) -> (assert(stench(WhatY, RightX)));
%     % Go Relative Down
%     (A == moveforward, E == on, WhatDir == rsouth, DownY is WhatY - 1) -> (assert(stench(DownY, WhatX)));
%     % Go Relative Left
%     (A == moveforward, E == on, WhatDir == rwest, LeftX is WhatX - 1) -> (assert(stench(WhatY, LeftX)))).

% Confundus Detection
move(A, L) :-
    current(WhatY, WhatX, WhatDir),(
    % Go Relative Up
    (A == moveforward, WhatDir == rnorth, UpY is WhatY + 1) ->  percept(UpY, WhatX, L);
    % Go Relative Right
    (A == moveforward, WhatDir == reast, RightX is WhatX + 1) ->  percept(WhatY, RightX, L);
    % Go Relative Down
    (A == moveforward, WhatDir == rsouth, DownY is WhatY - 1) ->  percept(DownY, WhatX, L);
    % Go Relative Left
    (A == moveforward, WhatDir == rwest, LeftX is WhatX - 1) ->  percept(WhatY, LeftX, L)).


% Percept Confundus
percept(Y, X, [C, S|_]) :-
    % Tingle?
    (C == on -> (assert(tingle(Y, X)));
    (S == on -> (assert(stench(Y, X)))).
    

current(3, 3, rsouth).


