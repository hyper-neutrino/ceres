import functions

class Section:
	def __init__(self, matcher, priority, function):
		self.matcher = matcher
		self.priority = priority
		self.function = function
	def matches(self, index):
		return self.matcher(index)
	def __call__(self, index):
		return self.function(index)
	def priority(self):
		return self.priority
