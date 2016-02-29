class SearchAgent(object):

	def __init__(self, x, y):
		self.position = (x,y)

	def __repr__(self):
		return "( " + str(self.position) + " )"
		