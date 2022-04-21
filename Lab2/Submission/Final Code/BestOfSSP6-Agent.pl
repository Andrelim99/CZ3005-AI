% Variables that can be changed
:- dynamic fired/1,
pickedCoin/1,
current/3,
reborn/0,
gameStart/1,
stench/2,
tingle/2,
confounded/1,
percept/1,
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
% Updated as at 13/4/2021
update_safe/2,
remove_all_in_wall/2,
confirm_not_wumpus/2,
confirm_not_portal/2,
explore/1,
% Updated as at 15/4/2021
numcoins/1,

confirm_wumpus/2,
first_stench/1,
more_likely_wumpus/2.




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
    retractall(numcoins(_)),
    retractall(confirm_not_wumpus(_, _)),
    retractall(confirm_not_portal(_, _)),
    retractall(first_stench(_)),
    retractall(more_likely_wumpus(_,_)),
               
    % Not to be reset in reposition-----
    assert(has_coin(false)),
    assert(numcoins(0)),
    assert(fired(false)),
    assert(wumpus_dead(false)),    
    % ----------------------------------
    
    assert(first_stench(true)),
    assert(safe(0,0)),
    assert(visited(0,0)),
    assert(direction(rnorth)),
    assert(relative_position(0, 0)).
    
    

reposition(L):-
    retractall(visited(_, _)),
    retractall(wumpus(_, _)),
    retractall(portal(_, _)),
    retractall(confounded(_)),
    retractall(tingle(_, _)),
    retractall(glitter(_, _)),
    retractall(stench(_, _)),
    retractall(safe(_, _)),
    % retractall(wumpus_dead(_)),
    % retractall(has_coin(_)),
    % retractall(fired(_)),
    retractall(direction(_)),
    retractall(relative_position(_, _)),
    retractall(wall(_, _)),
    % retractall(numcoins(_)),
    retractall(first_stench(_)),
    retractall(more_likely_wumpus(_,_)),

    retractall(confirm_not_wumpus(_, _)),
    retractall(confirm_not_portal(_, _)),

    assert(first_stench(true)),
    assert(safe(0,0)),
    assert(visited(0,0)),
    assert(direction(rnorth)),
    assert(relative_position(0, 0)),
    percept(L).

retract_portal_wumpus(X, Y) :-
    portal(X, Y), wumpus(X, Y) -> retract(portal(X, Y)), retract(wumpus(X, Y));
    portal(X, Y) -> retract(portal(X, Y));
    wumpus(X, Y) -> retract(wumpus(X, Y)).



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
    relative_position(X, Y),
    (\+visited(X, Y), assert(visited(X, Y))),
    (\+safe(X, Y), assert(safe(X, Y))),
    retract_portal_wumpus(X, Y).

% If Bump -> Wall
moveforward([_, _, _, _, B|_]) :-
    B == on, current(CurX, CurY, CurDir),
    (
        (CurDir == rnorth, NewY is CurY + 1, NewX is CurX);
        % Go Relative Right
        (CurDir == reast, NewX is CurX + 1, NewY is CurY);
        % Go Relative Down
        (CurDir == rsouth, NewY is CurY - 1, NewX is CurX);
        % Go Relative Left
        (CurDir == rwest, NewX is CurX - 1, NewY is CurY)
    ),

    \+wall(NewX, NewY), assert(wall(NewX, NewY)), remove_all_in_wall(NewX, NewY).%, (portal(NewX, NewY) -> retract(portal(NewX, NewY))), (wumpus(NewX, NewY) -> retract(wumpus(NewX, NewY))).

remove_all_in_wall(X, Y) :-
    safe(X, Y) -> retract(safe(X, Y));
    retract_portal_wumpus(X, Y).


% Pick up
pickup([_, _, _, G|_]) :-
    current(X, Y, _),
    G == on, retract(glitter(X, Y)),
    numcoins(N), NewN is N+1, retractall(numcoins(_)), assert(numcoins(NewN)).


% Fire arrow
shoot :-
    hasarrow, retractall(fired(_)), assert(fired(true)),
    current(X, Y, CurDir),
    (
        (CurDir == rnorth, NewX is X, NewY is Y + 1);
        (CurDir == rsouth, NewX is X, NewY is Y - 1);
        (CurDir == reast, NewX is X+1, NewY is Y);
        (CurDir == rwest, NewX is X-1, NewY is Y)
    ),
    retract(wumpus(NewX, NewY)), assert(confirm_not_wumpus(NewX, NewY)), \+portal(NewX, NewY), \+safe(NewX, NewY), assert(safe(NewX, NewY)).
    

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
    A == moveforward, (moveforward(L); true), percept(L).

% Pickup
move(A, L) :-
    A == pickup, pickup(L).

move(A, L) :-
    A == turnleft, turnleft, percept(L).

move(A, L) :-
    A == turnright, turnright, percept(L).

move(A, L) :-
    A == shoot, shoot, percept(L).

% Percept Confundus
percept([_, S, T, G, _, Sc]) :-
    current(X, Y, CurDir), (
    
    % Stench?
    (S == on, (\+stench(X, Y), assert(stench(X, Y))));
    % Tingle?
    (T == on, (\+tingle(X, Y),assert(tingle(X, Y))));
    % Glitter?
    (G == on, (\+glitter(X, Y),assert(glitter(X, Y))));
    % Scream?
    (Sc == on, assert(wumpus_dead(true)), retract(wumpus_dead(false)), update_safe, retractall(wumpus(_,_)))
    ).

    
update_safe :-
    wumpus(X, Y), \+portal(X, Y), \+safe(X,Y), assert(safe(X, Y)).

percept([C|_]) :-
    % Confundus?
    C == on -> \+confounded(true), (assert(confounded(true)));
    C == off ->  confounded(true), retract(confounded(true)).

percept([_, S, T|_]) :-
    current(X, Y, CurDir),
    S == off, T == off,
    (
        UpY is Y+1, DownY is Y-1, UpX is X+1, DownX is X-1,
        (
            (\+wall(X, UpY), \+safe(X, UpY), assert(safe(X, UpY)), retract_portal_wumpus(X, UpY));
            (\+wall(X, DownY), \+safe(X, DownY), assert(safe(X, DownY)), retract_portal_wumpus(X, DownY));
            (\+wall(UpX, Y), \+safe(UpX, Y), assert(safe(UpX, Y)), retract_portal_wumpus(UpX, Y));
            (\+wall(DownX, Y), \+safe(DownX, Y), assert(safe(DownX, Y)), retract_portal_wumpus(DownX, Y))
        )
    ).

percept([_, S, T|_]) :-
    current(X, Y, CurDir),
    S == on, T == off, wumpus_dead,
    (
        UpY is Y+1, DownY is Y-1, UpX is X+1, DownX is X-1,
        (
            (\+wall(X, UpY), \+safe(X, UpY), assert(safe(X, UpY)), retract_portal_wumpus(X, UpY));
            (\+wall(X, DownY), \+safe(X, DownY), assert(safe(X, DownY)), retract_portal_wumpus(X, DownY));
            (\+wall(UpX, Y), \+safe(UpX, Y), assert(safe(UpX, Y)), retract_portal_wumpus(UpX, Y));
            (\+wall(DownX, Y), \+safe(DownX, Y), assert(safe(DownX, Y)), retract_portal_wumpus(DownX, Y))
        )
    ).


percept([_, S|_]) :-
    current(X, Y, CurDir),  UpY is Y+1, DownY is Y-1, UpX is X+1, DownX is X-1,
        (
            S == off, 
            (           
                (\+confirm_not_wumpus(X, UpY), assert(confirm_not_wumpus(X, UpY)), retract(wumpus(X, UpY)));
                (\+confirm_not_wumpus(X, DownY), assert(confirm_not_wumpus(X, DownY)), retract(wumpus(X, DownY)));
                (\+confirm_not_wumpus(UpX, Y), assert(confirm_not_wumpus(UpX, Y)), retract(wumpus(UpX, Y)));
                (\+confirm_not_wumpus(DownX, Y), assert(confirm_not_wumpus(DownX, Y)), retract(wumpus(DownX, Y)))
            ), add_new_safe
        ).

wumpus_found :-
    confirm_wumpus(X, Y).

% wumpus(X, Y) :-
%     confirm_wumpus(X, Y).


percept([_, S, T|_]) :-
    (\+wumpus_dead, current(X, Y, CurDir),  UpY is Y+1, DownY is Y-1, UpX is X+1, DownX is X-1, S == on),
    (
        (
            first_stench(true),
            (
                (\+wall(X, UpY), \+safe(X, UpY), \+confirm_not_wumpus(X, UpY),\+wumpus(X, UpY), assert(wumpus(X, UpY)));
                (\+wall(X, DownY), \+safe(X, DownY), \+confirm_not_wumpus(X, DownY), \+wumpus(X, DownY), assert(wumpus(X, DownY)));
                (\+wall(UpX, Y), \+safe(UpX, Y), \+confirm_not_wumpus(UpX, Y),\+wumpus(UpX, Y), assert(wumpus(UpX, Y)));
                (\+wall(DownX, Y), \+safe(DownX, Y), \+confirm_not_wumpus(DownX, Y), \+wumpus(DownX, Y), assert(wumpus(DownX, Y)))
            ), retract(first_stench(true))
        );
        (
            (
                T == off,
                (
                    (\+wumpus(X, UpY), \+portal(X, UpY), \+wall(X, UpY), \+safe(X, UpY), assert(safe(X, UpY)));
                    (\+wumpus(X, DownY), \+portal(X, DownY), \+wall(X, DownY), \+safe(X, DownY), assert(safe(X, DownY)));
                    (\+wumpus(UpX, Y), \+portal(UpX, Y), \+wall(UpX, Y), \+safe(UpX, Y), assert(safe(UpX, Y)));
                    (\+wumpus(DownX, Y), \+portal(DownX, Y), \+wall(DownX, Y), \+safe(DownX, Y), assert(safe(DownX, Y)))            
                )
            ), validate_wumpus(X, Y)
        )   
    ).


validate_wumpus(X, Y) :-
    UpY is Y+1, DownY is Y-1, UpX is X+1, DownX is X-1, retractall(more_likely_wumpus(_, _)),
    (
        (wumpus(X, UpY) -> assert(more_likely_wumpus(X, UpY)));
        (wumpus(X, DownY) -> assert(more_likely_wumpus(X, DownY)));
        (wumpus(UpX, Y) -> assert(more_likely_wumpus(UpX, Y)));
        (wumpus(DownX, Y) -> assert(more_likely_wumpus(DownX, Y)))
    ), remove_wumpus.

remove_wumpus :-
    (wumpus(X, Y), \+more_likely_wumpus(X, Y)) -> retract(wumpus(X, Y)), (\+portal(X, Y)->assert(safe(X,Y))).


percept([_, _, T|_]) :-
    current(X, Y, CurDir),  UpY is Y+1, DownY is Y-1, UpX is X+1, DownX is X-1,
        (
            T == off, 
            (           
                (\+confirm_not_portal(X, UpY), assert(confirm_not_portal(X, UpY)), retract(portal(X, UpY)));
                (\+confirm_not_portal(X, DownY), assert(confirm_not_portal(X, DownY)), retract(portal(X, DownY)));
                (\+confirm_not_portal(UpX, Y), assert(confirm_not_portal(UpX, Y)), retract(portal(UpX, Y)));
                (\+confirm_not_portal(DownX, Y), assert(confirm_not_portal(DownX, Y)), retract(portal(DownX, Y)))
            ), add_new_safe
        ).

percept([_, _, T|_]) :-
    current(X, Y, CurDir), UpY is Y+1, DownY is Y-1, UpX is X+1, DownX is X-1,
    
    (
        T == on,
        (
            (\+wall(X, UpY), \+safe(X, UpY), \+confirm_not_portal(X, UpY), \+portal(X, UpY), assert(portal(X, UpY)));
            (\+wall(X, DownY), \+safe(X, DownY), \+confirm_not_portal(X, DownY), \+portal(X, DownY), assert(portal(X, DownY)));            
            (\+wall(DownX, Y), \+safe(DownX, Y), \+confirm_not_portal(DownX, Y), \+portal(DownX, Y),  assert(portal(DownX, Y)));
            (\+wall(UpX, Y), \+safe(UpX, Y), \+confirm_not_portal(UpX, Y), \+portal(UpX, Y), assert(portal(UpX, Y)))
        )

    ).
add_new_safe :-
    confirm_not_portal(X, Y), confirm_not_wumpus(X, Y), \+safe(X, Y), assert(safe(X, Y)).


% has arrow
hasarrow :-
    fired(false).

current(X, Y, Dir) :-
    relative_position(X, Y), direction(Dir).


wumpus_dead :-
    wumpus_dead(true), retractall(wumpus(_, _)).

confounded :-
    confounded(true).


% EXPLORE - TO DO
% explore([Mov|Movs]) :-
%     explore([Mov]), explore([Movs]).



% explore([moveforward]) :-
%     front_cell_unvisited_safe, \+explore([pickup]).

front_cell_unvisited_safe :-
    current(X, Y, CurDir),
    (
        (CurDir == rnorth, NewX is X, NewY is Y + 1);
        (CurDir == rsouth, NewX is X, NewY is Y - 1);
        (CurDir == reast, NewX is X+1, NewY is Y);
        (CurDir == rwest, NewX is X-1, NewY is Y)
    ),
    safe(NewX, NewY), \+visited(NewX, NewY).

explore([pickup]) :-
    current(X, Y, _),
    glitter(X, Y).


% explore([turnleft]) :-
%     \+explore([moveforward]), \+explore([pickup]), \+explore([shoot]), left_cell_unvisited_safe.

left_cell_unvisited_safe :-
    current(X, Y, CurDir),
    (
        (CurDir == rnorth, NewX is X-1, NewY is Y);
        (CurDir == rsouth, NewX is X+1, NewY is Y);
        (CurDir == reast, NewX is X, NewY is Y+1);
        (CurDir == rwest, NewX is X, NewY is Y-1)
    ),
    safe(NewX, NewY), \+visited(NewX, NewY).

% explore([turnright]) :-
%     \+explore([moveforward]), \+explore([pickup]), \+explore([shoot]),\+explore([turnleft]), right_cell_unvisited_safe.

right_cell_unvisited_safe :-
    current(X, Y, CurDir),
    (
        (CurDir == rnorth, NewX is X+1, NewY is Y);
        (CurDir == rsouth, NewX is X-1, NewY is Y);
        (CurDir == reast, NewX is X, NewY is Y-1);
        (CurDir == rwest, NewX is X, NewY is Y+1)
    ),
    safe(NewX, NewY), \+visited(NewX, NewY).

% explore([turnleft, turnleft]) :-
%     \+explore([moveforward]), \+explore([pickup]), \+explore([shoot]), \+explore([turnleft]), \+explore([turnright]), behind_cell_unvisited_safe.


behind_cell_unvisited_safe :-
    current(X, Y, CurDir),
    (
        (CurDir == rnorth, NewX is X, NewY is Y - 1);
        (CurDir == rsouth, NewX is X, NewY is Y + 1);
        (CurDir == reast, NewX is X-1, NewY is Y);
        (CurDir == rwest, NewX is X+1, NewY is Y)
    ),
    safe(NewX, NewY), \+visited(NewX, NewY).




adjacent_unvisited_safe_cell :-
    current(X, Y, CurDir),
    UpX is X+1, DownX is X-1, UpY is Y+1, DownY is Y-1,
    (
        (safe(X, UpY), \+visited(X, UpY));
        (safe(X,DownY), \+visited(X,DownY));
        (safe(UpX, Y), \+visited(UpX, Y));
        (safe(DownX, Y), \+visited(DownX, Y))
    ).

% explore([shoot]) :-
%     \+explore([pickup]), \+adjacent_unvisited_safe_cell, hasarrow, 
%     adjacent_wumpus.

explore([shoot]) :-
    \+explore([pickup]), no_safe_unvisited_spots, facing_wumpus, hasarrow, 
    adjacent_wumpus.

adjacent_wumpus :-
    current(X, Y, CurDir),
    (
        (CurDir == rnorth, NewX is X, NewY is Y + 1);
        (CurDir == rsouth, NewX is X, NewY is Y - 1);
        (CurDir == reast, NewX is X+1, NewY is Y);
        (CurDir == rwest, NewX is X-1, NewY is Y)
    ),
    wumpus(NewX, NewY).

facing_wumpus :-
    current(CurX, CurY, CurDir), wumpus(X, Y),
    (
        (CurX == X, CurY > Y, CurDir == rsouth);
        (CurX == X, CurY < Y, CurDir == rnorth);
        (CurY == Y, CurX > X, CurDir == rwest);
        (CurY == Y, CurX < X, CurDir == reast)
    ).

explore([turnleft]) :-
    \+explore([pickup]), no_safe_unvisited_spots, hasarrow, adjacent_wumpus, \+facing_wumpus.


% BACKTRACKING... UNFINISHED
% explore([turnleft, turnleft, moveforward]) :-
%     \+adjacent_unvisited_safe_cell.

% explore([turnleft]) :-
%     \+adjacent_unvisited_safe_cell, safe_unvisited_cell, \+explore([moveforward]), \+explore([pickup]), \+explore([shoot]), random(1, 11, V), V > 3.

% explore([turnright]) :-
%     \+adjacent_unvisited_safe_cell, safe_unvisited_cell, \+explore([moveforward]), \+explore([pickup]), \+explore([shoot]).

% explore([moveforward]) :-
%     \+explore([pickup]), \+adjacent_unvisited_safe_cell, safe_unvisited_cell, front_cell_safe_visited.

front_cell_safe_visited :-
    current(X, Y, CurDir),
    (
        (CurDir == rnorth, NewX is X, NewY is Y + 1);
        (CurDir == rsouth, NewX is X, NewY is Y - 1);
        (CurDir == reast, NewX is X+1, NewY is Y);
        (CurDir == rwest, NewX is X-1, NewY is Y)
    ),
    visited(NewX, NewY).    


% explore(turnright) :-
%     \+adjacent_unvisited_safe_cell, \+explore([pickup]), \+explore([moveforward]), \+explore([shoot]), safe_unvisited_cell.

safe_unvisited_cell :-
    safe(X, Y),\+wall(X,Y), \+visited(X, Y).


    

% Pathfinding

no_safe_unvisited_spots :-
    \+safe_unvisited_cell.

explore(Actions) :-
    current(X, Y, _), solve([X, Y], Actions, Sol).


solve(Node, Actions, Solution)  :-
  depthfirst( [], [], Node, Actions, Solution).



depthfirst( Path, Actions, Node, Actions, [Node | Path] )  :-
   goal( Node).

depthfirst( Path, Actions, Node, ActionSol, Sol)  :-
  (
    adjacent_goal(Node, Node1);
    adjacent_visited_cell( Node, Node1)
  ),
  \+ member( Node1, Path),                % Prevent a cycle
  get_action(Node, Node1, Actions, Out, Path),
  depthfirst( [Node | Path], Out, Node1, ActionSol, Sol).

adjacent_visited_cell([X, Y], [A, B]) :-
    UpX is X+1, DownX is X-1, UpY is Y+1, DownY is Y-1,
    visited(A, B),
    (
        (A == UpX, B == Y);
        (A == DownX, B == Y);
        (A == X, B == UpY);
        (A == X, B == DownY)        
    ).



get_action([X1, Y1], [X2, Y2], In, Out, Path) :-   
    get_simulated_dir(Dir, [X1, Y1], Path),
    (
        (Dir == rnorth, X1 < X2) -> append(In, [turnright, moveforward], Out);
        (Dir == rnorth, X2 < X1) -> append(In, [turnleft, moveforward], Out);
        (Dir == rnorth, Y1 < Y2) -> append(In, [moveforward], Out);
        (Dir == rnorth, Y2 < Y1) -> append(In, [turnright, turnright, moveforward], Out);

        (Dir == reast, X1 < X2) -> append(In, [moveforward], Out);
        (Dir == reast, X2 < X1) -> append(In, [turnright, turnright, moveforward], Out);
        (Dir == reast, Y1 < Y2) -> append(In, [turnleft, moveforward], Out);
        (Dir == reast, Y2 < Y1) -> append(In, [turnright, moveforward], Out);

        (Dir == rwest, X1 < X2) -> append(In, [turnright, turnright, moveforward], Out);
        (Dir == rwest, X2 < X1) -> append(In, [moveforward], Out);
        (Dir == rwest, Y1 < Y2) -> append(In, [turnright, moveforward], Out);
        (Dir == rwest, Y2 < Y1) -> append(In, [turnleft, moveforward], Out);

        (Dir == rsouth, X1 < X2) -> append(In, [turnleft, moveforward], Out);
        (Dir == rsouth, X2 < X1) -> append(In, [turnright, moveforward], Out);
        (Dir == rsouth, Y1 < Y2) -> append(In, [turnright, turnright, moveforward], Out);
        (Dir == rsouth, Y2 < Y1) -> append(In, [moveforward], Out)
    ).


get_simulated_dir(Dir, Cur, Path) :-
    \+member(_, Path) -> direction(Dir);
    get_dir(Dir, Cur, Path).


get_dir(Dir, Cur, [Pre|_]) :-
    simulated_north(Dir, Cur, Pre);
    simulated_south(Dir, Cur, Pre);
    simulated_west(Dir, Cur, Pre);
    simulated_east(Dir, Cur, Pre).

simulated_north(rnorth, [X1, Y1], [X0, Y0]) :-
    Y1 > Y0.

simulated_south(rsouth, [X1, Y1], [X0, Y0]) :-
    Y1 < Y0.

simulated_west(rwest, [X1, Y1], [X0, Y0]) :-
    X1 < X0.

simulated_east(reast, [X1, Y1], [X0, Y0]) :-
    X1 > X0.



adjacent_goal([X, Y], [A, B]) :-
    UpX is X+1, DownX is X-1, UpY is Y+1, DownY is Y-1,
    goal([A, B]),
    (
        (A == UpX, B == Y);
        (A == DownX, B == Y);
        (A == X, B == UpY);
        (A == X, B == DownY)        
    ).

    

goal([0, 0]) :-
    no_safe_unvisited_spots, \+hasarrow.

goal([X, Y]) :-
    no_safe_unvisited_spots, hasarrow, visited(X, Y), adjacent_wumpus(X, Y).

adjacent_wumpus(X, Y) :-
    UpX is X+1, DownX is X-1, UpY is Y+1, DownY is Y-1,
    (
        wumpus(UpX, Y);
        wumpus(DownX, Y);
        wumpus(X, UpY);
        wumpus(X, DownY)
    ).



goal([X, Y]) :-
    safe_unvisited_cell(X, Y); glitter(X,Y).

safe_unvisited_cell(X, Y) :-
    safe(X, Y), \+visited(X, Y), \+wall(X, Y).