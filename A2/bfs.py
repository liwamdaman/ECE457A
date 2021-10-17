import collections
from point import Point
from utils import children

def bfs(maze, start, end):
	q = collections.deque()

	# set uses constant look up time, use to ensure we ignore repeated positions
	checked = set([start])
	# queue of paths, paths are growing lists of points
	q.append([start])

	expandedCount = 0
	curr = None

	while(True):
		qLength = len(q)
		for i in range(qLength):
			# pop and get the last position of the path
			currPath = q.popleft()
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
					q.append(newPath)
					checked.add(child)
