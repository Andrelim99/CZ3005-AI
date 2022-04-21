/* position(x, y, orientation) */
:- dynamic(position/3).
position(0,0,north).

set_position(position(X, Y, Z)) :-
    call(position(OldX, OldY, OldZ)),
    retract(position(OldX, OldY, OldZ)),
    assertz(position(X, Y, Z)),
    /* When agent changes position, assert that the new position is visited */
    assertz(visited(X, Y)).

/* Whether X, Y in the grid is visited. In the beginning, (0,0) is visited */
:- dynamic(visited/2).
visited(0, 0). 

/* 
Sensory inputs, [confounded, stench, tingle, glitter, bump, scream] 
confounded is true at the start of the game
*/
:- dynamic(senses/6).
senses(true, false, false, false, false, false).

set_senses(senses(Confounded, Stench, Tingle, Glitter, Bump, Scream)) :-
    call(senses(X1,X2,X3,X4,X5,X6)),
    retract(senses(X1,X2,X3,X4,X5,X6)),
    assertz(senses(Confounded, Stench, Tingle, Glitter, Bump, Scream)).

hasarrow.

turn_left :-
    position(X, Y, Orientation),
    (
        Orientation == north -> set_position(position(X,Y,west)) ;
        Orientation == west -> set_position(position(X,Y,south)) ;
        Orientation == south -> set_position(position(X,Y,east)) ;
        set_position(position(X,Y,north))
    ).

turn_right :-
    position(X, Y, Orientation),
    (
        Orientation == north -> set_position(position(X,Y,east)) ;
        Orientation == east -> set_position(position(X,Y,south)) ;
        Orientation == south -> set_position(position(X,Y,west)) ;
        set_position(position(X,Y,north))
    ).

move_forward :-
    position(X, Y, Orientation),
    (
        Orientation == north -> 
            NewY is Y + 1,
            NewX is X ;
        Orientation == east -> 
            NewX is X + 1,
            NewY is Y ;
        Orientation == south -> 
            NewX is X,
            NewY is Y - 1 ;
        NewX is X - 1,
        NewY is Y
    ),
    set_position(position(NewX, NewY, Orientation)).

/* Functions required for assignment */
reborn :- set_position(0, 0, north).
    
move(A, L) :-
    A = moveforward.

reposition(L) :-
    write(L).

wumpus(X,Y) :-
    \+ visited(X,Y),
    (   
      Y is Y-1,stench(X,Y);
      Y is Y+1,stench(X,Y);
      X is X-1,stench(X, Y);
      X is X+1,stench(X, Y)
    ).

confoundus(X,Y) :-
    \+ visited(X,Y),
    (   
      DownY is Y-1,tingle(X,DownY);
      UpY is Y+1,tingle(X,UpY);
      LeftX is X-1,tingle(LeftX, Y);
      RightX is X+1,tingle(RightX, Y)
    ).

new_position(X,Y,Z) :-
    position(OldX,OldY,OldZ),
    (   
    	Z == north ->  X is OldX, Y is OldY+1, Z is OldZ ;
    	Z == south ->  X is OldX, Y is OldY-1, Z is OldZ ;
        Z == east ->  X is OldX+1, Y is OldY, Z is OldZ ;
        X is OldX-1, Y is OldY, Z is OldZ
    ).

move(A) :-
    new_position(X,Y,Z).
	A = moveforward,
		\+ wumpus(X,Y),
		\+ confoundus(X,Y) ;
	A = turnleft.
    
position(0,0,north).
stench(1,1).
visited(0,1).