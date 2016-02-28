import random

def random_generation(grid):
	cols = grid.col
	rows = grid.row

	for x in range(cols):
		for y in range(rows):
			if random.random() < 0.3:
				grid.nodes[x][y].block_node()


class Heap(object):
	"""
	using max heap as priority que
	"""
	def __init__(self):
		self.heap = [None]
		self.length = 0

	def __repr__(self):
		return str(self.heap[1:self.length])

	def swap(self, a, b):
		self.heap[a] , self.heap[b] = self.heap[b] , self.heap[a]


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
		self.heap.append(element)
		element.key = key
		self.length += 1
		self.update(self.length)

	def update(self, i):
		p = self.parent(i)
		if p > 0:
			if self.get_key(p) < self.get_key(i):
				self.swap(p,i)
				self.update(p)

	def max_heapify(self, i):
		r = self.right(i)
		l = self.left(i)

		if l <= self.length and self.get_key(l) > self.get_key(i):
			largest = l
		else:
			largest = i

		if r <= self.length and self.get_key(r) > self.get_key(largest):
			largest = r

		if largest != i:
			self.swap(largest, i)
			self.max_heapify(largest)

	def pop(self):
		"""get the largest priority element"""
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

	for x in xrange(1,10):
		l.append(Test(random.randint(1,100)))

	print l

	heap = Heap()
			
	for x in l:
		heap.add(x,x.val)
		
	print heap

	print heap.pop()

	print heap
		