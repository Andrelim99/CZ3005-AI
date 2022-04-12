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
reposition/1,
wumpus/2,
portal/2,
update_safe/2.




reborn:-
    retractall(visited(_, _)),
    retractall(wumpus(_, _)),
    retractall(portal(_, _)),
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
    assert(safe(0,0)),
    assert(visited(0,0)),
    
    assert(direction(rnorth)),
    assert(relative_position(0, 0)).
    
    

reposition(L):-
        retractall(visited(_, _)),
        retractall(wumpus(_, _)),
        retractall(confounded(_)),
        retractall(portal(_, _)),
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
moveforward([_, _, _, _, B, _]) :-
    B == off, current(CurX, CurY, CurDir), retractall(relative_position(_, _)),  
    (
        ((CurDir == rnorth, NewY is CurY + 1) -> assert(relative_position(CurX, NewY)));
        % Go Relative Right
        ((CurDir == reast, NewX is CurX + 1) -> assert(relative_position(NewX, CurY)));
        % Go Relative Down
        ((CurDir == rsouth, NewY is CurY - 1) -> assert(relative_position(CurX, NewY)));
        % Go Relative Left
        ((CurDir == rwest, NewX is CurX - 1) -> assert(relative_position(NewX, CurY)))
    ),
    relative_position(X, Y),(\+visited(X, Y), assert(visited(X, Y))), (\+safe(X, Y), assert(safe(X, Y))),(portal(X, Y) -> retract(portal(X, Y))), (wumpus(X, Y) -> retract(wumpus(X, Y))).

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
        ((CurDir == rnorth, NewY is CurY + 1) -> (assert(relative_position(CurX, CurY))) , (safe(CurX, NewY) -> retract(safe(CurX, NewY))));
        % Go Relative Right
        ((CurDir == reast, NewX is CurX + 1) -> assert(relative_position(CurX, CurY)));
        % Go Relative Down
        ((CurDir == rsouth, NewY is CurY - 1) -> assert(relative_position(CurX, CurY)));
        % Go Relative Left
        ((CurDir == rwest, NewX is CurX - 1) -> assert(relative_position(CurX, CurY)))
    ),

    (\+wall(CurX, NewY), assert(wall(CurX, NewY))), (portal(CurX, NewY) -> retract(portal(CurX, NewY))), (wumpus(CurX, NewY) -> retract(wumpus(CurX, NewY))).


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
    A == moveforward, moveforward(L), percept(L).

% Pickup
move(A, L) :-
    A == pickup, pickup(L).


move(A, L) :-
    A == turnleft, turnleft, percept(L).

move(A, L) :-
    A == turnright, turnright, percept(L).

% Percept Confundus
percept([C, S, T, G, _, Sc]) :-
    current(X, Y, CurDir), (
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
    (Sc == on, (\+wumpus_dead(true), assert(wumpus_dead(true))))
    ).




percept([_, S, T|_]) :-
    current(X, Y, CurDir),
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


percept([_, S|_]) :-
    current(X, Y, CurDir),  UpY is Y+1, DownY is Y-1, UpX is X+1, DownX is X-1,
    (
        S == on, 
        (           
            (\+wall(X, UpY), \+safe(X, UpY), \+wumpus(X, UpY), assert(wumpus(X, UpY)));
            (\+wall(X, DownY), \+safe(X, DownY), \+wumpus(X, DownY), assert(wumpus(X, DownY)));
            (\+wall(UpX, Y), \+safe(UpX, Y), \+wumpus(UpX, Y), assert(wumpus(UpX, Y)));
            (\+wall(DownX, Y), \+safe(DownX, Y), \+wumpus(DownX, Y), assert(wumpus(DownX, Y))) 
        )
    ).

percept([_, _, T|_]) :-
    current(X, Y, CurDir), UpY is Y+1, DownY is Y-1, UpX is X+1, DownX is X-1,
    
    (
        T == on,
        (
            (\+wall(X, UpY), \+safe(X, UpY), \+portal(X, UpY), assert(portal(X, UpY)));
            (\+wall(X, DownY), \+safe(X, DownY), \+portal(X, DownY), assert(portal(X, DownY)));            
            (\+wall(DownX, Y), \+safe(DownX, Y), \+portal(DownX, Y),  assert(portal(DownX, Y)));
            (\+wall(UpX, Y), \+safe(UpX, Y), \+portal(UpX, Y), assert(portal(UpX, Y)))
        )

    ).






% Maybe Wumpus
% wumpus(X, Y) :-
%     stench(X, Y) X is X+1, Y is Y + 1.
% current(X, Y),
%     UpY is Y+1, DownY is Y-1, UpX is X+1, DownX is X-1, \+wall(X, Y), \+safe(X, Y),
%     (stench(X, UpY); stench(X, DownY); stench(UpX, Y); stench(DownX, Y)), assert(wumpus(X, Y)).

% Maybe Portal
% portal(X, Y) :-
%     tingle(TX, TY),
%     (UpY is TY+1, DownY is TY-1, UpX is TX+1, DownX is TX-1),
%     (
%         \+wall(UpX, TY), \+safe(UpX, TY), assert(portal(UpX, TY));
%         \+wall(DownX, TY), \+safe(DownX, TY), assert(portal(DownX, TY));
%         \+wall(TX, DownY), \+safe(TX, DownY), assert(portal(TX, DownY));
%         \+wall(TX, UpY), \+safe(TX, UpY), assert(portal(TX, UpY));
%    ).
    % (tingle(X, UpY); tingle(X, DownY); tingle(UpX, Y); tingle(DownX, Y)), assert(portal(X, Y)).



% has arrow
hasarrow :-
    fired(false).

current(X, Y, Dir) :-
    relative_position(X, Y), direction(Dir).



