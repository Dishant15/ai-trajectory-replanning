import random

def random_generation(grid):
	cols = grid.col
	rows = grid.row

	for x in range(cols):
		for y in range(rows):
			if random.random() < 0.3:
				grid.nodes[x][y].block_node()

	while True:
		agent = random.randint(0, cols-1) , random.randint(0, rows-1)
		if not grid.get_node(agent).is_blocked():
			break

	while True:
		goal = random.randint(0, cols-1) , random.randint(0, rows-1)
		if not grid.get_node(goal).is_blocked():
			break

	return [agent, goal]


def manhattan_distance(pos1, pos2):
	return abs(pos2[0]-pos1[0]) + abs(pos2[1]-pos1[1])


class Heap(object):
	"""
	using max heap as priority que
	"""
	def __init__(self):
		self.heap = [None]
		self.length = 0

	def __repr__(self):
		return str(self.heap[1:self.length+1])

	def swap(self, a, b):
		self.heap[a] , self.heap[b] = self.heap[b] , self.heap[a]
		self.heap[a].i = a
		self.heap[b].i = b

	def get(self, i):
		# Maintain 1 base indexing rather than 0 base
		return self.heap[i]

	def get_key(self, i):
		return self.get(i).key

	def root(self):
		if self.length > 0:
			return self.heap[0]
		return None

	def parent(self, i):
		return i/2

	def left(self, i):
		return 2*i

	def right(self, i):
		return (2*i) + 1

	def add(self, element, key):
		self.length += 1
		try:
			self.heap[self.length] = element
		except Exception, e:
			self.heap.append(element)
		element.key = key
		element.i = self.length
		self.update(self.length)

	def update(self, i):
		p = self.parent(i)
		if p > 0:
			if self.get_key(p) > self.get_key(i):
				self.swap(p,i)
				self.update(p)

	def update_key(self, i, key):
		element = self.get(i)
		element.key = key
		self.update(i)


	def max_heapify(self, i):
		r = self.right(i)
		l = self.left(i)

		smalest = i

		if l <= self.length and self.get_key(l) < self.get_key(i):
			smalest = l
		else:
			smalest = i

		if r <= self.length and self.get_key(r) < self.get_key(smalest):
			smalest = r

		if smalest != i:
			self.swap(smalest, i)
			self.max_heapify(smalest)

	def pop(self):
		"""get the smalest priority element"""
		prio_element = self.get(1)
		self.swap(1, self.length)
		self.length -= 1
		self.max_heapify(1)
		return prio_element

if __name__ == '__main__':
	class Test(object):
		"""docstring for Test"""
		def __init__(self, val):
			self.val = val

		def __repr__(self):
			return str(self.val)

	l = []

	s = Test(5)
	temp = Test(random.randint(2,10))
	for x in xrange(1,6):
		l.append(temp)
		temp = Test(random.randint(1,10))

	print "This is l",l

	heap = Heap()
			
	for x in l:
		heap.add(x,x.val)

	heap.add(s,s.val)
		
	print "This is heap",heap

	heap.update_key(s.i,1)

	print heap
		