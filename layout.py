from Tkinter import *

from utils import random_generation, manhattan_distance
from search import SearchAgent

class GridNodes(object):
	"""Represents the data inside each node of GridWorld"""
	def __init__(self, x, y, grid):
		self.x = x
		self.y = y
		self.grid = grid
		self.canvas = grid.canvas
		self.size = grid.size
		self.blocked = False
		self.visited = False
		self.goal = False
		self.pos = (x * self.size, y * self.size)
		self.xy = (x ,y)

		self.h_val = None
		self.g_val = None
		self.f_val = None
		# Heap values
		self.i = None

	def __repr__(self):
		try:
			rep_str = str(self.f_val) + " - ( " + str(self.x) + ' , ' + str(self.y) + " )"
		except Exception, e:
			rep_str = "( " + str(self.x) + ' , ' + str(self.y) + " )"
		return rep_str

	def is_blocked(self):
		return self.blocked

	def is_visited(self):
		return self.visited

	def fill_box(self,color):
		x1 = self.pos[0]
		y1 = self.pos[1]
		x2 = x1 + self.size
		y2 = y1 + self.size
		self.canvas.create_rectangle(x1, y1, x2, y2, outline="white", fill=color)

	def block_node(self, color="brown"):
		self.blocked = True
		self.fill_box(color)
		
	def place_agent(self, color="orange"):
		self.fill_box(color)
		# put text item above newly created rectangle
		self.canvas.tag_raise(self.g_text)
		self.canvas.tag_raise(self.h_text)
		self.canvas.tag_raise(self.f_text)
		# self.canvas.itemconfigure(self.g_text, fill="yellow")

	def make_goal(self,color="green"):
		self.fill_box(color)
		self.goal = True
		self.g_val = self.grid.col * self.grid.row
		self.set_val("g", self.g_val)
		self.set_val("f", self.g_val)
		# put text item above newly created rectangle
		self.canvas.tag_raise(self.g_text)
		self.canvas.tag_raise(self.h_text)
		self.canvas.tag_raise(self.f_text)

	def set_val(self, item, val):
		text = str(val)
		if item == "g":
			obj = self.g_text
			self.g_val = val
		elif item == "h":
			obj = self.h_text
			self.h_val = val
		else:
			obj = self.f_text
			self.f_val = val
		self.canvas.itemconfigure(obj, text=text)

	def get_cost(self):
		if self.blocked:
			return self.grid.col * self.grid.row + 10
		else:
			return 1

	def get_neighbours(self):
		all_actions = [ (1,0), (0,1), (-1,0), (0,-1) ]
		actions = [ (self.x+x[0], self.y+x[1]) for x in all_actions if self.x+x[0]>=0 and self.y+x[1]>=0 and self.x+x[0]<self.grid.col and self.y+x[1]<self.grid.row]
		return [ self.grid.get_node(xy) for xy in actions ]
		


class GridWorld(object):
	"""Grid World creation class"""
	def __init__(self, col=5, row=5, size=100, maze_generator=random_generation):
		self.col = col
		self.row = row
		self.size = size
		self.width = col*size
		self.height = row*size
		self.nodes = []

		self.root = Tk()
		self.root.title("Grid World")

		self.canvasframe = Frame(self.root, padx=40, pady=40)
		self.canvasframe.pack( side = TOP )

		self.canvas = Canvas(self.canvasframe, width=self.width, height=self.height, background='bisque')
		self.canvas.pack()

		# positions on tiles for text
		g_margin = (int(self.size*0.25) , int(self.size*0.25))
		h_margin = (int(self.size*0.25) , int(self.size*0.75))
		f_margin = (int(self.size*0.75) , int(self.size*0.25))
		for x in range(col):
			temp = []
			for y in range(row):
				node = GridNodes(x,y,self)
				node.g_text = self.canvas.create_text((x*size)+g_margin[0],(y*size)+g_margin[1],fill="darkblue",font="Times 18 italic bold",text="g")
				node.h_text = self.canvas.create_text((x*size)+h_margin[0],(y*size)+h_margin[1],fill="darkblue",font="Times 18 italic bold",text="h")
				node.f_text = self.canvas.create_text((x*size)+f_margin[0],(y*size)+f_margin[1],fill="brown",font="Times 18 italic bold",text="f")
				temp.append(node)
			self.nodes.append(temp)

		# Draw grid on canvas
		x = 0
		y = 0
		while x < self.width:
			while y < self.height:
				self.canvas.create_line(0,y,self.width,y,fill = 'white')
				y = y + size
			self.canvas.create_line(x,0,x,self.height,fill = 'white')
			x = x + size
		
		if hasattr(maze_generator, '__call__'):
			agent, goal = maze_generator(self)
			self.agent = self.get_node(agent)
			self.agent.place_agent()
			self.goal = self.get_node(goal)
			self.goal.make_goal()
		else:
			# maze generator is a list of tiles to block
			# list = [ (agent pos), (goal pos), [ (x1,y1), ... ] ]
			self.agent_node = self.get_node(maze_generator[0])
			self.agent_node.place_agent()
			self.goal_node = self.get_node(maze_generator[1])
			self.goal_node.make_goal()
			for tile in maze_generator[2]:
				self.get_node(tile).block_node()

		self.root.after(1000,self.start_search)

		self.root.geometry("1200x900")  #Set starting window size
		self.root.mainloop() 			#starts event loop of the program

	def get_node(self, xy):
		return self.nodes[xy[0]][xy[1]]

	def get_h_val(self, node):
		return manhattan_distance(node.xy, self.goal_node.xy)

	def start_search(self):
		# Calculate all the h values before starting the search
		for x in range(self.col):
			for y in range(self.row):
				node = self.get_node((x,y))
				h_val = self.get_h_val(node)
				node.set_val("h", h_val)
		# create a search agent and implement search
		self.search_agent = SearchAgent(self.agent_node, self.goal_node, self)

	def fill_box(self,xy, color="brown"):
		"""
		Add color/highlight to the box given by x,y coordinated
		"""
		x1 = (xy[0] * self.size)
		y1 = (xy[1] * self.size)
		x2 = x1 + self.size
		y2 = y1 + self.size
		self.canvas.create_rectangle(x1, y1, x2, y2, outline="white", fill=color, tags="square")


if __name__ == '__main__':
	block_list = [ (2,4) , (4,4) ,[ (2,2), (2,1), (3,2), (3,3), (2,3), (3,4)] ]

	gameWorld = GridWorld(maze_generator=block_list)
		