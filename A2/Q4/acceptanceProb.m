function acceptPoint = acceptanceProb(optimValues,newx,newfval)
% Uses the probability/acceptance function we learned in class
deltaCost = cost(newfval) - cost(optimValues.fval);

if deltaCost <= 0
    % Simply accept the new point
    acceptPoint = true;
else
    acceptProb = exp(-1*deltaCost / optimValues.temperature);
    if rand < acceptProb
        acceptPoint = true;
    else
        acceptPoint = false;
    end
end

end

