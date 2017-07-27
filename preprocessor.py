class Atom:
	def __init__(self, function):
		self.function = function
	def __call__(self, arguments):
		return self.function(arguments)

class Quick:
	def __init__(self, function):
		self.function = function
	def __call__(self, function):
		return self.function(function)

def preprocess(tokens):
	components = []
	# TODO
	return components
