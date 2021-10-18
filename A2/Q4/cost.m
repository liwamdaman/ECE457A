function cost = cost(newfval)
% For the easom function, the global minimum is 1, and all values are in
% between 1 and 0. We will define the cost as 1 - newfval.
% In the best case, the cost is 0.
% In the worst case, the cost is 1.
cost = 1-newfval;
end

