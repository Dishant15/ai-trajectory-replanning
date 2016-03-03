from utils import Heap
from collections import deque

class SearchAgent(object):

	def __init__(self, start_node, goal_node, grid):
		self.grid = grid
		self.position = start_node.xy
		self.start_node = start_node
		self.goal_node = goal_node

		self.open_list = Heap()
		self.start_node.set_val("g", 0)
		self.start_node.set_val("f", start_node.h_val)
		self.open_list.add(start_node, start_node.f_val)

		self.search()

	def __repr__(self):
		return "agent at - ( " + str(self.position) + " )"

	def expand(self, node):
		if node == self.goal_node:
			print "Success we got to the goal"
			self.success()
			return
		next_nodes = node.get_neighbours()
		node.visited = True
		for s_next in next_nodes:
			new_g_val = node.g_val + s_next.get_cost()
			if s_next.g_val == None:
				# First time g val setting
				s_next.set_val("g", new_g_val)
				f_val = new_g_val + s_next.h_val
				s_next.set_val("f", f_val)
				# Set this node as parent to retrace from goal
				s_next.parent = node
				self.open_list.add(s_next, f_val)

			elif s_next.g_val > new_g_val:
				# Old parent to this node is not the shortest path make new one
				s_next.set_val("g", new_g_val)
				f_val = new_g_val + s_next.h_val
				s_next.set_val("f", f_val)
				# Change parent
				s_next.parent = node
				if s_next.i == None:
					# Not in the heap yet
					self.open_list.add(s_next, f_val)
				else:
					# update key in heap
					self.open_list.update_key(s_next.i, f_val)
		# self.grid.root.after(800, self.search)
		self.search()

	def search(self):
		node = self.open_list.pop()
		if node.f_val > self.goal_node.f_val:
			print "Search Failed, path can not be reached"
			return None
		self.expand(node)

	def success(self):
		path_list = []
		node = self.goal_node
		path_list.append(node)
		while True:
			# node.fill_box("yellow")
			node = node.parent
			path_list.append(node)
			if node == self.start_node:
				break
		self.move_agent(path_list)

	def move_agent(self,path):
		# Move agent along the path provided
		# Check for changing cost
		if len(path) == 0:
			return
		next_node = path.pop()
		self.start_node.clear_agent()
		self.start_node = next_node
		next_node.place_agent()
		self.grid.root.after(800, lambda:self.move_agent(path))

		