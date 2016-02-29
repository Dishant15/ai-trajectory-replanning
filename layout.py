from Tkinter import *

from utils import random_generation

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

	def __repr__(self):
		return "( " + str(self.x) + ' , ' + str(self.y) + " )"

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
		
	def place_agent(self, color="blue"):
		self.fill_box(color)
		# put text item above newly created rectangle
		self.canvas.tag_raise(self.g_text)
		self.canvas.tag_raise(self.h_text)
		self.canvas.tag_raise(self.f_text)
		# self.canvas.itemconfigure(self.g_text, fill="yellow")

	def make_goal(self,color="green"):
		self.fill_box(color)
		self.goal = True
		# put text item above newly created rectangle
		self.canvas.tag_raise(self.g_text)
		self.canvas.tag_raise(self.h_text)
		self.canvas.tag_raise(self.f_text)

	def change_text(self, item, text):
		if item == "g":
			obj = self.g_text
		elif item == "h":
			obj = self.h_text
		else:
			obj = self.f_text
		self.canvas.itemconfigure(obj, text=text)
		


class GridWorld(object):
	"""Grid World creation class"""
	def __init__(self, col=5, row=5, size=150, maze_generator=random_generation):
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
			self.get_node(agent).place_agent()
			self.get_node(goal).make_goal()
		else:
			# maze generator is a list of tiles to block
			# list = [ (agent pos), (goal pos), [ (x1,y1), ... ] ]
			self.get_node(maze_generator[0]).place_agent()
			self.get_node(maze_generator[1]).make_goal()
			for tile in maze_generator[2]:
				self.get_node(tile).block_node()


		self.root.geometry("1200x900")  #Set starting window size
		self.root.mainloop() 			#starts event loop of the program

	def get_node(self, xy):
		return self.nodes[xy[0]][xy[1]]

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
		