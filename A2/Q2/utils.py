from point import Point

def children(maze, node):
	rightMax = len(maze[0])-1
	upMax = len(maze)-1

	children = []

	if node.x > 0 and maze[node.y][node.x-1] == 0:
		children.append(Point(node.x-1, node.y))
	if node.y > 0 and maze[node.y-1][node.x] == 0:
		children.append(Point(node.x, node.y-1))
	if node.x < rightMax and maze[node.y][node.x+1] == 0:
		children.append(Point(node.x+1, node.y))
	if node.y < upMax and maze[node.y+1][node.x] == 0:
		children.append(Point(node.x, node.y+1))

	return children