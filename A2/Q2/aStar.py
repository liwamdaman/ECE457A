from queue import PriorityQueue
from utils import children

from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)

def aStar(maze, start, end):

	# priority queue of PrioritizedItem(priority: evaluation_function_value, item: path of points)
	q = PriorityQueue()
	q.put(PrioritizedItem(evaluate([start], end), [start]))

	# set uses constant look up time, use to ensure we ignore repeated positions
	checked = set([start])

	expandedCount = 0

	while(True):
		currPath = q.get().item
		curr = currPath[-1]
		expandedCount = expandedCount + 1

		if curr == end:
			print("Solution path is: " + str(currPath))
			print("Solution cost is: " + str(len(currPath)))
			print("Number of nodes explored: " + str(expandedCount))
			return

		for child in children(maze, curr):
			if child not in checked:
				newPath = list(currPath)
				newPath.append(child)
				q.put(PrioritizedItem(evaluate(newPath, end), newPath))
				checked.add(child)

def evaluate(currPath, end):
	return pathCost(currPath) + estimatedCostToGoal(currPath, end)

def pathCost(currPath):
	return len(currPath)

def estimatedCostToGoal(currPath, end):
	# use manhattan distance for estimating, this is an admissable heuristic
	curr = currPath[-1]
	return abs(curr.x - end.x) + abs(curr.y - end.y)
