from utils import children

def dfs(maze, start, end):

	# stack of paths, paths are growing lists of points
	stack = []
	stack.append([start])

	# set uses constant look up time, use to ensure we ignore repeated positions
	checked = set([start])

	expandedCount = 0

	while(True):
		currPath = stack.pop()
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
				stack.append(newPath)
				checked.add(child)
