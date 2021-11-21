import csv
import heapq
from permutation import Permutation
import random

## Import distance and flow data ##
distances = []
flows = []
with open('Distance.csv') as distance_file:
	csv_reader = csv.reader(distance_file, delimiter=',')
	for row in csv_reader:
		distances.append([int(value) for value in row])
#print(distances)
with open('Flow.csv') as flow_file:
	csv_reader = csv.reader(flow_file, delimiter=',')
	for row in csv_reader:
		flows.append([int(value) for value in row])
#print(flows)

## Initialize tabu list ##
tabu = []
for i in range(20):
	tabu.append([])
	for j in range(20):
		tabu[i].append(0)

## update the tabu list ##
def updateTabu(mostRecentSwap, tabuTenure):
	for i in range(20):
		for j in range(i+1, 20):
			if tabu[i][j] > 0:
				tabu[i][j] = tabu[i][j] - 1
	# default tabu tenure is 15
	tabu[mostRecentSwap[0]][mostRecentSwap[1]] = tabuTenure

## Calculates cost for a given permutation ##
def cost(permutation):
	cost = 0
	for i in range(20):
		for j in range(i+1, 20):
			distance = distances[i][j]
			flow = flows[permutation[i]-1][permutation[j]-1]
			cost = cost + (distance * flow)
	return cost

## Computes the neighboring solutions for a given solution/iteration, and sorts in ascending order of cost ##
def neighborhood(currPermutation):
	heap = []
	for i in range(20):
		for j in range(i+1, 20):
			newSolution = currPermutation.assignments.copy()
			newSolution[i], newSolution[j] = newSolution[j], newSolution[i]
			# Items on heap are of the form (cost of new solution, new solution, (swapped index i, swapped index j))
			heapq.heappush(heap, (cost(newSolution), newSolution, (i, j)))
	return heap

## Returns the next permutation to use, and also updates tabu list ##
def nextSolution(neighborhood, tabuTenure):
	curr = heapq.heappop(neighborhood)
	while(tabu[curr[2][0]][curr[2][1]] != 0):
		# print("Tabu found! At " + str(curr[2]))
		curr = heapq.heappop(neighborhood)
	updateTabu(curr[2], tabuTenure)
	# print(curr[0], curr[1])
	# print(tabu)
	return Permutation(curr[0], curr[1])

def part2():
	# Start with an intial solution, solutions are in the form of Permutation class
	initialAssignments = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
	currPermutation = Permutation(cost(initialAssignments), initialAssignments)

	bestPermutation = currPermutation
	numIterSinceLastImprovement = 0
	while (numIterSinceLastImprovement <= 100):
		# Check the neighborhood of solutions
		neighboringSolutions = neighborhood(currPermutation)
		currPermutation = nextSolution(neighboringSolutions, 15)
		if currPermutation.cost < bestPermutation.cost:
			numIterSinceLastImprovement = 0
			bestPermutation = currPermutation
		else:
			numIterSinceLastImprovement = numIterSinceLastImprovement + 1

	print("Initial starting point: " + str(initialAssignments))
	print("The best solution found: " + str(bestPermutation.assignments) + " with a cost of " + str(bestPermutation.cost))

def part3i():
	# Start with an intial solution, solutions are in the form of Permutation class
	initialAssignments = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
	# Randomize the initial solution
	random.shuffle(initialAssignments)
	currPermutation = Permutation(cost(initialAssignments), initialAssignments)

	bestPermutation = currPermutation
	numIterSinceLastImprovement = 0
	while (numIterSinceLastImprovement <= 100):
		# Check the neighborhood of solutions
		neighboringSolutions = neighborhood(currPermutation)
		currPermutation = nextSolution(neighboringSolutions, 15)
		if currPermutation.cost < bestPermutation.cost:
			numIterSinceLastImprovement = 0
			bestPermutation = currPermutation
		else:
			numIterSinceLastImprovement = numIterSinceLastImprovement + 1

	print("Initial starting point: " + str(initialAssignments))
	print("The best solution found: " + str(bestPermutation.assignments) + " with a cost of " + str(bestPermutation.cost))

def part3ii():
	tabuTenures = [5, 25]

	for tabuTenure in tabuTenures:
		# Start with an intial solution, solutions are in the form of Permutation class
		initialAssignments = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
		currPermutation = Permutation(cost(initialAssignments), initialAssignments)

		bestPermutation = currPermutation
		numIterSinceLastImprovement = 0
		while (numIterSinceLastImprovement <= 100):
			# Check the neighborhood of solutions
			neighboringSolutions = neighborhood(currPermutation)
			currPermutation = nextSolution(neighboringSolutions, tabuTenure)
			if currPermutation.cost < bestPermutation.cost:
				numIterSinceLastImprovement = 0
				bestPermutation = currPermutation
			else:
				numIterSinceLastImprovement = numIterSinceLastImprovement + 1

		print("Tabu list size/tenure used: " + str(tabuTenure))
		print("The best solution found: " + str(bestPermutation.assignments) + " with a cost of " + str(bestPermutation.cost))

def part3iii():
	initialAssignments = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
	currPermutation = Permutation(cost(initialAssignments), initialAssignments)

	bestPermutation = currPermutation
	numIterSinceLastImprovement = 0
	tabuTenure = random.randint(0, 50)
	tabuTenures = [tabuTenure]
	iterCount = 0
	while (numIterSinceLastImprovement <= 100):
		# Dynamically change the tabu tenure every 50 iterations
		iterCount = iterCount + 1
		if iterCount >= 50:
			iterCount = 0
			tabuTenure = random.randint(0, 50)
			tabuTenures.append(tabuTenure)

		neighboringSolutions = neighborhood(currPermutation)
		currPermutation = nextSolution(neighboringSolutions, tabuTenure)
		if currPermutation.cost < bestPermutation.cost:
			numIterSinceLastImprovement = 0
			bestPermutation = currPermutation
		else:
			numIterSinceLastImprovement = numIterSinceLastImprovement + 1

	print("Tabu tenures used: " + str(tabuTenures))
	print("The best solution found: " + str(bestPermutation.assignments) + " with a cost of " + str(bestPermutation.cost))

def part3iv():

	def nextSolutionUsingAspirationCriterion1(neighborhood, tabuTenure, bestPermutationSoFar):
		curr = heapq.heappop(neighborhood)
		# Select curr if it has 0 in tabu list or if its cost is lower than any permutation so far
		while(tabu[curr[2][0]][curr[2][1]] != 0 and curr[0] >= bestPermutationSoFar.cost):
			curr = heapq.heappop(neighborhood)
		updateTabu(curr[2], tabuTenure)
		return Permutation(curr[0], curr[1])

	def nextSolutionUsingAspirationCriterion2(neighborhood, tabuTenure):
		# Always return the best solution in the neighborhood
		curr = heapq.heappop(neighborhood)
		updateTabu(curr[2], tabuTenure)
		return Permutation(curr[0], curr[1])

	initialAssignments = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
	currPermutation = Permutation(cost(initialAssignments), initialAssignments)

	bestPermutation = currPermutation
	numIterSinceLastImprovement = 0
	while (numIterSinceLastImprovement <= 100):
		# Check the neighborhood of solutions
		neighboringSolutions = neighborhood(currPermutation)
		currPermutation = nextSolutionUsingAspirationCriterion1(neighboringSolutions, 15, bestPermutation)
		if currPermutation.cost < bestPermutation.cost:
			numIterSinceLastImprovement = 0
			bestPermutation = currPermutation
		else:
			numIterSinceLastImprovement = numIterSinceLastImprovement + 1

	print("Tabu Search using aspiration criterion 1: best solution so far")
	print("The best solution found: " + str(bestPermutation.assignments) + " with a cost of " + str(bestPermutation.cost))

	initialAssignments = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
	currPermutation = Permutation(cost(initialAssignments), initialAssignments)

	bestPermutation = currPermutation
	numIterSinceLastImprovement = 0
	while (numIterSinceLastImprovement <= 100):
		# Check the neighborhood of solutions
		neighboringSolutions = neighborhood(currPermutation)
		currPermutation = nextSolutionUsingAspirationCriterion2(neighboringSolutions, 15)
		if currPermutation.cost < bestPermutation.cost:
			numIterSinceLastImprovement = 0
			bestPermutation = currPermutation
		else:
			numIterSinceLastImprovement = numIterSinceLastImprovement + 1

	print("Tabu Search using aspiration criterion 2: best solution in the neighborhood")
	print("The best solution found: " + str(bestPermutation.assignments) + " with a cost of " + str(bestPermutation.cost))

def part3v():

	def neighborhoodLimited(currPermutation):
		neighborhood = []
		for i in range(20):
			for j in range(i+1, 20):
				newSolution = currPermutation.assignments.copy()
				newSolution[i], newSolution[j] = newSolution[j], newSolution[i]
				neighborhood.append((cost(newSolution), newSolution, (i, j)))
		neighborhood = random.sample(neighborhood, 50)
		heapq.heapify(neighborhood)
		return neighborhood

	initialAssignments = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
	currPermutation = Permutation(cost(initialAssignments), initialAssignments)

	bestPermutation = currPermutation
	numIterSinceLastImprovement = 0
	while (numIterSinceLastImprovement <= 100):
		# Check the limited neighborhood of solutions
		neighboringSolutions = neighborhoodLimited(currPermutation)
		currPermutation = nextSolution(neighboringSolutions, 15)
		if currPermutation.cost < bestPermutation.cost:
			numIterSinceLastImprovement = 0
			bestPermutation = currPermutation
		else:
			numIterSinceLastImprovement = numIterSinceLastImprovement + 1

	print("Using limited neighborhood of 50")
	print("The best solution found: " + str(bestPermutation.assignments) + " with a cost of " + str(bestPermutation.cost))

def part3vi():

	def updateTabuIncludingFreq(mostRecentSwap, tabuTenure):
		for i in range(20):
			for j in range(i+1, 20):
				if tabu[i][j] > 0:
					tabu[i][j] = tabu[i][j] - 1
		tabu[mostRecentSwap[0]][mostRecentSwap[1]] = tabuTenure
		# Add to the frequency count in the bottom left triangle portion of the tabu list
		tabu[mostRecentSwap[1]][mostRecentSwap[0]] = tabu[mostRecentSwap[1]][mostRecentSwap[0]] + 1

	def neighborhoodIncludingFreq(currPermutation):
		heap = []
		for i in range(20):
			for j in range(i+1, 20):
				newSolution = currPermutation.assignments.copy()
				newSolution[i], newSolution[j] = newSolution[j], newSolution[i]
				# Penalize moves based on frequency count
				heapq.heappush(heap, (cost(newSolution) + tabu[j][i], newSolution, (i, j)))
		return heap

	def nextSolutionIncludingFreq(neighborhood, tabuTenure):
		curr = heapq.heappop(neighborhood)
		while(tabu[curr[2][0]][curr[2][1]] != 0):
			curr = heapq.heappop(neighborhood)
		updateTabuIncludingFreq(curr[2], tabuTenure)
		return Permutation(curr[0], curr[1])

	initialAssignments = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
	currPermutation = Permutation(cost(initialAssignments), initialAssignments)

	bestPermutation = currPermutation
	numIterSinceLastImprovement = 0
	while (numIterSinceLastImprovement <= 100):
		neighboringSolutions = neighborhoodIncludingFreq(currPermutation)
		currPermutation = nextSolutionIncludingFreq(neighboringSolutions, 15)
		if currPermutation.cost < bestPermutation.cost:
			numIterSinceLastImprovement = 0
			bestPermutation = currPermutation
		else:
			numIterSinceLastImprovement = numIterSinceLastImprovement + 1

	print("Adding frequency component to tabu list")
	print("The best solution found: " + str(bestPermutation.assignments) + " with a cost of " + str(bestPermutation.cost))

if __name__ == '__main__':
	#part2()
	#part3i()
	#part3ii()
	#part3iii()
	#part3iv()
	#part3v()
	part3vi()