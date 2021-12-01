## Solving "6-multiplexer" problem using a genetic programming algorithm
## DEAP python library was a huge help, as well as this example they provide: https://deap.readthedocs.io/en/master/examples/gp_multiplexer.html

import random
import operator
import numpy
import matplotlib.pyplot as plt
import pygraphviz as pgv

from deap import gp
from deap import creator
from deap import algorithms
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

pset = gp.PrimitiveSet("MAIN", MUX_TOTAL_LINES, "MUX")
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
toolbox.register("select", tools.selTournament, tournsize=50)

def main():
	pop = toolbox.population(n=500)
	mutationProb = 0.1
	crossoverProb = 0.8
	numGen = 50

	hof = tools.HallOfFame(1)
	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("avg", numpy.mean)
	stats.register("std", numpy.std)
	stats.register("min", numpy.min)
	stats.register("max", numpy.max)

	log = algorithms.eaSimple(pop, toolbox, crossoverProb, mutationProb, numGen, stats, halloffame=hof, verbose=True)

	# Graph the final result
	nodes, edges, labels = gp.graph(hof[0])
	g = pgv.AGraph()
	g.add_nodes_from(nodes)
	g.add_edges_from(edges)
	g.layout(prog="dot")
	for i in nodes:
		n = g.get_node(i)
		n.attr["label"] = labels[i]
	g.draw("tree.pdf")

	# Plot best fitness each iteration
	print(log[1].select("max"))
	plt.plot(log[1].select("max"))
	plt.ylabel("Best program fitness each generation")
	plt.xlabel("Generation")
	plt.show()

if __name__ == "__main__":
    main()