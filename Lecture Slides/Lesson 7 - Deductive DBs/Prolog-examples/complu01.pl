% FACTS
father(tom, amy).
father(jack, fred).
father(tony,carolII).
father(fred,carolIII).

mother(graceI, amy).
mother(amy, fred).
mother(carolI, carolII).
mother(carolII, carolIII).

% RULES
parent(X,Y) :- father(X,Y).
parent(X,Y) :- mother(X,Y).

% Adding recursion
ancestor(X,Y) :- parent(X,Y).
ancestor(X,Y) :- parent(X,Z),ancestor(Z,Y).


