%Facts
dog("Black Lab").
cat("Persian").

%Rules
animal(A) :- dog(A) ; cat(A).
