% Set bounds -100 <= x(1)/x(2) <= 100
lb = [-100, -100];
ub = [100, 100];

rng default

bestMinimumLocation = [0, 0];
bestMinimumValue = 1000;
bestInitialPoint = [0, 0];
bestInitialTemp = 0;
bestScheduleType = "";
bestScheduleValue = 0;
for i = 1:10
    x0 = 200*rand(1,2) - 100;   % Random starting point with values in between -100 and 100
    for j = 1:10
        initialTemp = 100*rand; % Random intial temperature between 0 and 100

        % Linear annealing schedules
        for k = 1:3
            alpha = 2*rand;
            tempFnHandle = @(optimValues,options) optimValues.temperature - alpha;
            options = optimoptions(@simulannealbnd,'display', 'off', 'InitialTemperature', initialTemp, 'TemperatureFcn', tempFnHandle, 'AcceptanceFcn', @acceptanceProb);
            [x,fval,exitFlag,output] = simulannealbnd(@easom, x0, lb, ub, options);
            %fprintf('Minimum found at : (%g, %g)\n', x(1), x(2));
            if fval < bestMinimumValue
                bestMinimumValue = fval;
                bestMinimumLocation = x;
                bestInitialPoint = x0;
                bestInitialTemp = initialTemp;
                bestScheduleType = "linear";
                bestScheduleValue = alpha;
            end
        end

        % Exponential annealing schedules
        for k = 1:3
            alpha = 0.5 + 0.5*rand;
            tempFnHandle = @(optimValues,options) optimValues.temperature*alpha;
            options = optimoptions(@simulannealbnd,'display', 'off', 'InitialTemperature', initialTemp, 'TemperatureFcn', tempFnHandle, 'AcceptanceFcn', @acceptanceProb);
            [x,fval,exitFlag,output] = simulannealbnd(@easom, x0, lb, ub, options);
            %fprintf('Minimum found at : (%g, %g)\n', x(1), x(2));
            if fval < bestMinimumValue
                bestMinimumValue = fval;
                bestMinimumLocation = x;
                bestInitialPoint = x0;
                bestInitialTemp = initialTemp;
                bestScheduleType = "exponential";
                bestScheduleValue = alpha;
            end
        end

        % Slow annealing schedules
        for k = 1:3
            beta = 0.5 * rand;
            tempFnHandle = @(optimValues,options) [optimValues.temperature(1)/(beta*optimValues.temperature(1) + 1); optimValues.temperature(2)/(beta*optimValues.temperature(2) + 1)];
            options = optimoptions(@simulannealbnd,'display', 'off', 'InitialTemperature', initialTemp, 'TemperatureFcn', tempFnHandle, 'AcceptanceFcn', @acceptanceProb);
            [x,fval,exitFlag,output] = simulannealbnd(@easom, x0, lb, ub, options);
            %fprintf('Minimum found at : (%g, %g)\n', x(1), x(2));
            if fval < bestMinimumValue
                bestMinimumValue = fval;
                bestMinimumLocation = x;
                bestInitialPoint = x0;
                bestInitialTemp = initialTemp;
                bestScheduleType = "slow";
                bestScheduleValue = beta;
            end
        end
    end
end
fprintf('Best solution found used an initial point (%g, %g) and an initial temperature of %g, outputting a minimum value of %g located at (%g, %g)\n', ...
    bestInitialPoint(1), bestInitialPoint(2), bestInitialTemp, bestMinimumValue, bestMinimumLocation(1), bestMinimumLocation(2));
fprintf('The annealing schedule used was of %s type with an alpha/beta value of %g', bestScheduleType, bestScheduleValue);


