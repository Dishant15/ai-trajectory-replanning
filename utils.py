import random

def random_generation(grid):
	cols = grid.col
	rows = grid.row

	for x in range(cols):
		for y in range(rows):
			if random.random() < 0.3:
				grid.nodes[x][y].block_node()