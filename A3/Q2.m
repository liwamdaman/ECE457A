rng default

% Assume that the values of the controller parameters are in the ranges: Kp ∈(2,18), Ti ∈(1.05,9.42), Td ∈(0.26,2.37).
lower_bound = [2, 1.05, 0.26];
upper_bound = [18, 9.42, 2.37];

opts = optimoptions( ...
    @ga, ...
    'PlotFcn',{@gaplotbestf}, ...
    'PopulationSize', 50, ...
    'MaxGenerations', 150, ...
    'CrossoverFraction', 0.6, ...
    'MutationFcn', {@mutationadaptfeasible, 0.25}, ...
    'EliteCount', 2, ...
    'SelectionFcn', @selectionroulette...
    );
[x,Fval,~,Output] = ga(@fitnessFunc,3,[],[],[],[], lower_bound, upper_bound,[],opts);

fprintf('Part c:\nConverged on solution Kp = %.3g, Ti = %.3g, Td = %.3g, cost = %g in %d generations.\n', x(1), x(2), x(3), Fval, Output.generations);

% e.
fprintf('Part e:\n')
maxGen = 75;
opts = optimoptions(@ga,'PopulationSize', 50,'MaxGenerations', maxGen, 'CrossoverFraction', 0.6, 'MutationFcn', {@mutationadaptfeasible, 0.25}, 'EliteCount', 2, 'SelectionFcn', @selectionroulette);
[x,Fval,~,Output] = ga(@fitnessFunc,3,[],[],[],[], lower_bound, upper_bound,[],opts);
fprintf('Converged on solution Kp = %.3g, Ti = %.3g, Td = %.3g, cost = %g in %d generations.\n', x(1), x(2), x(3), Fval, Output.generations);
maxGen = 300;
opts = optimoptions(@ga,'PopulationSize', 50,'MaxGenerations', maxGen, 'CrossoverFraction', 0.6, 'MutationFcn', {@mutationadaptfeasible, 0.25}, 'EliteCount', 2, 'SelectionFcn', @selectionroulette);
[x,Fval,~,Output] = ga(@fitnessFunc,3,[],[],[],[], lower_bound, upper_bound,[],opts);
fprintf('Converged on solution Kp = %.3g, Ti = %.3g, Td = %.3g, cost = %g in %d generations.\n', x(1), x(2), x(3), Fval, Output.generations);

% f.
fprintf('Part f:\n')
popSize = 25;
opts = optimoptions(@ga,'PopulationSize', popSize,'MaxGenerations', 150, 'CrossoverFraction', 0.6, 'MutationFcn', {@mutationadaptfeasible, 0.25}, 'EliteCount', 2, 'SelectionFcn', @selectionroulette);
[x,Fval,~,Output] = ga(@fitnessFunc,3,[],[],[],[], lower_bound, upper_bound,[],opts);
fprintf('Converged on solution Kp = %.3g, Ti = %.3g, Td = %.3g, cost = %g in %d generations.\n', x(1), x(2), x(3), Fval, Output.generations);
popSize = 100;
opts = optimoptions(@ga,'PopulationSize', popSize,'MaxGenerations', 150, 'CrossoverFraction', 0.6, 'MutationFcn', {@mutationadaptfeasible, 0.25}, 'EliteCount', 2, 'SelectionFcn', @selectionroulette);
[x,Fval,~,Output] = ga(@fitnessFunc,3,[],[],[],[], lower_bound, upper_bound,[],opts);
fprintf('Converged on solution Kp = %.3g, Ti = %.3g, Td = %.3g, cost = %g in %d generations.\n', x(1), x(2), x(3), Fval, Output.generations);

% g.
fprintf('Part g:\n')
crossoverProb = 0.3;
opts = optimoptions(@ga,'PopulationSize', 50,'MaxGenerations', 150, 'CrossoverFraction', crossoverProb, 'MutationFcn', {@mutationadaptfeasible, 0.25}, 'EliteCount', 2, 'SelectionFcn', @selectionroulette);
[x,Fval,~,Output] = ga(@fitnessFunc,3,[],[],[],[], lower_bound, upper_bound,[],opts);
fprintf('Converged on solution Kp = %.3g, Ti = %.3g, Td = %.3g, cost = %g in %d generations.\n', x(1), x(2), x(3), Fval, Output.generations);
crossoverProb = 0.9;
opts = optimoptions(@ga,'PopulationSize', 50,'MaxGenerations', 150, 'CrossoverFraction', crossoverProb, 'MutationFcn', {@mutationadaptfeasible, 0.25}, 'EliteCount', 2, 'SelectionFcn', @selectionroulette);
[x,Fval,~,Output] = ga(@fitnessFunc,3,[],[],[],[], lower_bound, upper_bound,[],opts);
fprintf('Converged on solution Kp = %.3g, Ti = %.3g, Td = %.3g, cost = %g in %d generations.\n', x(1), x(2), x(3), Fval, Output.generations);

% h.
fprintf('Part h:\n')
mutationProb = 0.1;
opts = optimoptions(@ga,'PopulationSize', 50,'MaxGenerations', 150, 'CrossoverFraction', 0.6, 'MutationFcn', {@mutationadaptfeasible, mutationProb}, 'EliteCount', 2, 'SelectionFcn', @selectionroulette);
[x,Fval,~,Output] = ga(@fitnessFunc,3,[],[],[],[], lower_bound, upper_bound,[],opts);
fprintf('Converged on solution Kp = %.3g, Ti = %.3g, Td = %.3g, cost = %g in %d generations.\n', x(1), x(2), x(3), Fval, Output.generations);
mutationProb = 0.5;
opts = optimoptions(@ga,'PopulationSize', 50,'MaxGenerations', 150, 'CrossoverFraction', 0.6, 'MutationFcn', {@mutationadaptfeasible, mutationProb}, 'EliteCount', 2, 'SelectionFcn', @selectionroulette);
[x,Fval,~,Output] = ga(@fitnessFunc,3,[],[],[],[], lower_bound, upper_bound,[],opts);
fprintf('Converged on solution Kp = %.3g, Ti = %.3g, Td = %.3g, cost = %g in %d generations.\n', x(1), x(2), x(3), Fval, Output.generations);