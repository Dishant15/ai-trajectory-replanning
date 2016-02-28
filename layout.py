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

	def __repr__(self):
		return "( " + str(self.x) + ' , ' + str(self.y) + " )"

	def block_node(self, color="brown"):
		self.blocked = True
		x1 = (self.x * self.size)
		y1 = (self.y * self.size)
		x2 = x1 + self.size
		y2 = y1 + self.size
		self.canvas.create_rectangle(x1, y1, x2, y2, outline="white", fill=color)
		


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

		self.canvasframe = Frame(self.root, padx=40, pady=40, bd=2, relief=GROOVE)
		self.canvasframe.pack( side = TOP )

		self.canvas = Canvas(self.canvasframe, width=self.width, height=self.height, background='bisque')
		self.canvas.pack()

		for x in range(col):
			temp = []
			for y in range(row):
				temp.append(GridNodes(x,y,self))
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
		

		maze_generator(self)

		# self.canvas.delete("square")

		self.root.geometry("1200x900")  #Set starting window size
		self.root.mainloop() 			#starts event loop of the program

	def fill_box(self,x,y, color="brown"):
		"""
		Add color/highlight to the box given by x,y coordinated
		"""
		x1 = (x * self.size)
		y1 = (y * self.size)
		x2 = x1 + self.size
		y2 = y1 + self.size
		self.canvas.create_rectangle(x1, y1, x2, y2, outline="white", fill=color, tags="square")


if __name__ == '__main__':
	gameWorld = GridWorld()
		