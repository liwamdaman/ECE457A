import collections
from point import Point
from utils import children

def bfs(maze, start, end):
	q = collections.deque()

	explored = set([start])
	q.append(start)

	cost = 0
	curr = start

	while(len(q)>0):
		qLength = len(q)
		for i in range(qLength):
			curr = q.popleft()
			print(curr)
			if curr == end:
				break
			for child in children(maze, curr):
				if child not in explored:
					q.append(child)
					explored.add(child)
		cost = cost + 1
			


	print(len(explored))
	print(cost)
