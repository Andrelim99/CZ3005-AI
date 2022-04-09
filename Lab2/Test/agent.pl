% Variables that can be changed
:- dynamic fired/1,
pickedCoin/1,
current/3,
reborn/0,
gameStart/1,
stench/2,
tingle/2,
confounded/1,
percept/3,
wumpus_dead/1,
moveforward/1,
glitter/2,
bump/2,
wall/2,
has_coin/1,
relative_position/2,
direction/1,
safe/2,
visited/2,
reposition/1.




reborn:-
    retractall(visited(_, _)),
    retractall(wumpus(_, _)),
    retractall(confounded(_)),
    retractall(tingle(_, _)),
    retractall(glitter(_, _)),
    retractall(stench(_, _)),
    retractall(safe(_, _)),
    retractall(wumpus_dead(_)),
    retractall(has_coin(_)),
    retractall(fired(_)),
    retractall(direction(_)),
    retractall(relative_position(_, _)),
    retractall(wall(_, _)),



    assert(has_coin(false)),
    assert(fired(false)),
    assert(wumpus_dead(false)),
    assert(confounded(true)),
    
    assert(direction(rnorth)),
    assert(relative_position(0, 0)),
    assert(safe(0,0)),
    assert(visited(0,0)).
    

reposition(L):-
        retractall(visited(_, _)),
        retractall(wumpus(_, _)),
        retractall(confounded(_)),
        retractall(tingle(_, _)),
        retractall(glitter(_, _)),
        retractall(stench(_, _)),
        retractall(safe(_, _)),
        retractall(direction(_)),
        retractall(relative_position(_, _)),
        retractall(wall(_, _)),

        assert(direction(rnorth)),
        assert(relative_position(0, 0)),
        assert(safe(0,0)),
        assert(visited(0,0)),
        percept(0,0, L).

% No wall
moveforward([_, _, _, _, B|_]) :-
    B == off, current(CurX, CurY, CurDir), retractall(relative_position(_, _)),    
    (
        ((CurDir == rnorth, NewY is CurY + 1) -> assert(relative_position(CurX, NewY)));
        % Go Relative Right
        ((CurDir == reast, NewX is CurX + 1) -> assert(relative_position(NewX, CurY)));
        % Go Relative Down
        ((CurDir == rsouth, NewY is CurY - 1) -> assert(relative_position(CurX, NewY)));
        % Go Relative Left
        ((CurDir == rwest, NewX is CurX - 1) -> assert(relative_position(NewX, CurY)))
    ), relative_position(X, Y),(\+visited(X, Y), assert(visited(X, Y))), (\+safe(X, Y), assert(safe(X, Y))).

% Certain there is a wall - Not sure yet
% moveforward(_) :-
%     current(CurX, CurY, CurDir),    
%     (
%         ((CurDir == rnorth, NewY is CurY + 1), wall(CurX, NewY));
%         % Go Relative Right
%         ((CurDir == reast, NewX is CurX + 1), wall(NewX, CurY));
%         % Go Relative Down
%         ((CurDir == rsouth, NewY is CurY - 1), wall(CurX, NewY));
%         % Go Relative Left
%         ((CurDir == rwest, NewX is CurX - 1), wall(NewX, CurY))
%     ).

% If Bump -> Wall
moveforward([_, _, _, _, B|_]) :-
    B == on, current(CurX, CurY, CurDir),
    (
        ((CurDir == rnorth, NewY is CurY + 1) ->(\+wall(CurX, NewY), assert(wall(CurX, NewY)), retractall(safe(CurX, NewY))));
        % Go Relative Right
        ((CurDir == reast, NewX is CurX + 1) -> (\+wall(NewX, CurY), assert(wall(NewX, CurY)) , retractall(safe(NewX, CurY))));
        % Go Relative Down
        ((CurDir == rsouth, NewY is CurY - 1) ->(\+wall(CurX, NewY), assert(wall(CurX, NewY)), retractall(safe(CurX, NewY))));
        % Go Relative Left
        ((CurDir == rwest, NewX is CurX - 1) -> (\+wall(NewX, CurY), assert(wall(NewX, CurY)), retractall(safe(NewX, CurY))))
    ).

% Pick up
pickup([_, _, _, G|_]) :-
    G == on, assert(has_coin(true)).


% Fire arrow
shoot :-
    hasarrow, retractall(fired(_)), assert(fired(true)).
    

% Turn left
turnleft :-
    direction(CurDir), retractall(direction(_)),
    (
        (CurDir == rnorth, assert(direction(rwest)));
        (CurDir == reast, assert(direction(rnorth)));
        (CurDir == rsouth, assert(direction(reast)));
        (CurDir == rwest, assert(direction(rsouth)))
    ).

% Turn right
turnright :-
    direction(CurDir), retractall(direction(_)),
    (
        (CurDir == rnorth, assert(direction(reast)));
        (CurDir == reast, assert(direction(rsouth)));
        (CurDir == rsouth, assert(direction(rwest)));
        (CurDir == rwest, assert(direction(rnorth)))
    ).

% Move reasoning?
% Forward
move(A, L) :-
    (A == moveforward, moveforward(L), current(CurX, CurY, CurDir), percept(CurX, CurY, L)).

% Pickup
move(A, L) :-
    A == pickup, pickup(L).


% Percept Confundus
percept(X, Y, [C, S, T, G, B, Sc]) :-
    % Confundus?
    (C == on, (\+confounded(true), (assert(confounded(true)))));
    % Stench?
    (S == on, (\+stench(X, Y), assert(stench(X, Y))));
    % Tingle?
    (T == on, (\+tingle(X, Y),assert(tingle(X, Y))));
    % Glitter?
    (G == on, (\+glitter(X, Y),assert(glitter(X, Y))));
    % Bump? - Handled in moveforward
    % (B == on, (\+wall(X, Y), assert(wall(X, Y)))));
    % Scream?
    (Sc == on, (\+wumpus_dead(true), assert(wumpus_dead(true)))).

percept(X, Y, [_, S, T|_]) :-
    S == off, T == off,
    (
        UpY is Y+1, DownY is Y-1, UpX is X+1, DownX is X-1,
        (
            (\+wall(X, UpY), \+safe(X, UpY), assert(safe(X, UpY)));
            (\+wall(X, DownY), \+safe(X, DownY), assert(safe(X, DownY)));
            (\+wall(UpX, Y), \+safe(UpX, Y), assert(safe(UpX, Y)));
            (\+wall(DownX, Y), \+safe(DownX, Y), assert(safe(DownX, Y)))
        )
    ).
    
% has arrow
hasarrow :-
    fired(false).

current(X, Y, Dir) :-
    relative_position(X, Y), direction(Dir).






