function cost = fitnessFunc(x)
%FITNESSFUNC
% x contains Kp, Ti, Td
[ISE,t_r,t_s,M_p] = perfFCN(x'); % ga inputs row vectors, perfFCN expects column vectors

% For the cost, normalize and add.
% Very rough numbers used to divide and normalize.
% Cost is in between 0 and 1.
% We will consider settling time and ISE as more important measures, and weight accordingly.
cost = 0.3*(ISE/100) + 0.15*(t_r/1) + 0.4*(t_s/15) + 0.15*(M_p/50);
end

