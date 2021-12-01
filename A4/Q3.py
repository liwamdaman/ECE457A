## Solving "6-multiplexer" problem using a genetic programming algorithm
## DEAP python library was a huge help, as well as this example they provide: https://deap.readthedocs.io/en/master/examples/gp_multiplexer.html

import random
import operator

from deap import gp
from deap import creator
from deap import tools
from deap import base

MUX_SELECT_LINES = 2
MUX_IN_LINES = 2 ** MUX_SELECT_LINES
MUX_TOTAL_LINES = MUX_SELECT_LINES + MUX_IN_LINES

## Create full test set: 2^6 = 64 possible cases
# input : [a0 a1 d0 d1 d2 d3] for 2-4 MUX
# if a0=0 and a1=1, the address is 01 and the answer is the value of d1. Likewise, if a0=1 and if a0=1
inputs = [[0] * MUX_TOTAL_LINES for i in range(2 ** MUX_TOTAL_LINES)]
outputs = [0] * (2 ** MUX_TOTAL_LINES)
for i in range(2 ** MUX_TOTAL_LINES):
	for j in range(MUX_TOTAL_LINES):
		if i & (1 << j) :
			inputs[i][MUX_TOTAL_LINES-1-j] = 1
		else:
			inputs[i][MUX_TOTAL_LINES-1-j] = 0
for i in range(2 ** MUX_TOTAL_LINES):
	# Determine the corresponding output
	selectedIndex = MUX_SELECT_LINES
	for j, selectBit in enumerate(reversed(inputs[i][:MUX_SELECT_LINES])):
		selectedIndex += selectBit * 2**j
		outputs[i] = inputs[i][selectedIndex]
#print(inputs)
#print(outputs)


def ifFunction(condition, out1, out2):
    return out1 if condition else out2

pset = gp.PrimitiveSet("MAIN", MUX_TOTAL_LINES, "IN")
pset.addPrimitive(operator.and_, 2)
pset.addPrimitive(operator.or_, 2)
pset.addPrimitive(operator.not_, 1)
pset.addPrimitive(ifFunction, 3)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=4)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def fitness(individual):
	func = toolbox.compile(expr=individual)
	return (sum(func(*in_) == out for in_, out in zip(inputs, outputs))/(2 ** MUX_TOTAL_LINES) , )
toolbox.register("evaluate", fitness)

# GP Crossover: Randomly select one point on parents and swap subtrees
toolbox.register("mate", gp.cxOnePoint)

toolbox.register("expr_mut", gp.genGrow, min_=2, max_=4)
# GP Mutation: Randomly select point in tree and replace subtree at that point as a root by the expression generated using expr_mut
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

# Tournament based selection function
toolbox.register("select", tools.selTournament, tournsize=10)

def main():
	pop = toolbox.population(n=50)
	# As we learned in class, Pm should be kept small
	mutationProb = 0.05
	crossoverProb = 0.5
	numGen = 50

	# Evaluate the entire population
	fitnesses = map(toolbox.evaluate, pop)
	for ind, fit in zip(pop, fitnesses):
		ind.fitness.values = fit
		#print(fit)

	for g in range(numGen):

		offspring = list(map(toolbox.clone, pop))

		# Following the GP flowchart used in the notes
		i = 1
		while (i < len(offspring)):
			if i == len(offspring) - 1:
				# perform mutation, we only have room for one more offspring for the next generation
				selected = toolbox.select(offspring, 1)
				toolbox.mutate(selected[0])
				del selected[0].fitness.values
				i = i + 1
			else:
				# Choose to perform crossover or mutation probabilistically
				if random.random() < mutationProb:
					selected = toolbox.select(offspring, 1)
					toolbox.mutate(selected[0])
					del selected[0].fitness.values
					i = i + 1
				else:
					selected = toolbox.select(offspring, 2)
					toolbox.mate(selected[0], selected[1])
					del selected[0].fitness.values
					del selected[1].fitness.values
					i = i + 2

		# Update fitnesses and print best fitness of population each generation
		bestFitness = 0
		fitnesses = map(toolbox.evaluate, offspring)
		for ind, fit in zip(offspring, fitnesses):
			ind.fitness.values = fit
			if fit[0] > bestFitness:
				bestFitness = fit[0]
		print(bestFitness)

		pop[:] = offspring

if __name__ == "__main__":
    main()