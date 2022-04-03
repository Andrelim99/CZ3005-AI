% ∧
% reborn/0 - Reset all -> Met WUMPUS or Starting new exploration
reborn:-
    retractall(visited(_, _)),
    retractall(wumpus(_, _)),
    retractall(confundus(_, _)),
    retractall(tingle(_, _)),
    retractall(glitter(_, _)),
    retractall(stench(_, _)),
    retractall(safe(_, _)),
    assert(hasarrow),
    current(0, 0, rnorth).

% move(A, L)
% A = {shoot,moveforward,turnleft,turnright,pickup}
% L = Confounded, Stench, Tingle, Glitter, Bump, Scream. In that order. Each indicator can have one of the two values {on, off}. Given by driver

% Pick up coin
move(pickup, [_,_,_, on|_]).

% Turn left

% Turn right

% Shoot

% Move forward if space is (maybe) safe
move(forward, L):-
    


% reposition(L) - Agent's reset due to Confundus Portal. L's CP indicator shd be on.


% localisation and mapping
% visited(X,Y) 
% wumpus(X,Y) - W cell
% confundus(X,Y) - CP Cell
% tingle(X,Y) - CP adjacent
% glitter(X,Y) - Coin cell 
% stench(X,Y) - W adjacent
% safe(X,Y)



% explore(L) - true if there's a new space that can be explored OR if all accessible parts have been eplored and Coin has been taken,
% return true on action sequence in which agent is back to relative origin


% current(X,Y,D) - true if (X,Y) is the current relative position and D is the relative orientation(rnorth,rwest,reast,rsouth)



% hasarrow/0 - true if agent has arrow