from Tkinter import *

class GridWorld(object):
	"""Grid World creation class"""
	def __init__(self, col=5, row=5, size=100,generator=None):
		self.col = col
		self.row = row
		self.size = size
		self.width = col*size
		self.height = row*size

		if generator:
			self.generator = generator
		else:
			self.generator = None

		self.root = Tk()
		self.root.title("Grid World")

		self.canvasframe = Frame(self.root)
		self.canvasframe.pack( side = LEFT )

		self.canvas = Canvas(self.canvasframe, width=self.width, height=self.height, background='bisque')
		self.canvas.pack()

		# Draw grid on canvas
		x = 0
		while x < self.width:
			self.canvas.create_line(x,0,x,self.height,fill = 'white')
			x = x + size
		y = 0
		while y < self.height:
			self.canvas.create_line(0,y,self.width,y,fill = 'white')
			y = y + size

		self.fill_box(2,3)
		self.fill_box(2,4)

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
		