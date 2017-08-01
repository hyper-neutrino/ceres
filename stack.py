class Stack:
	def __init__(self, stack = None):
		self.stack = stack and list(stack) or []
	def pop(self):
		return self.stack.pop()
	def peek(self):
		value = self.pop()
		self.push(value)
		return value
	def __bool__(self):
		return self.stack != []
	def empty(self):
		values = self.stack[::-1]
		self.stack = []
		return values
	def get(self):
		return [x for x in self.stack]
	def push(self, *values):
		for value in values: self.stack.append(value)
	def  __str__(self): return str(self.stack)
	def __repr__(self): return str(self.stack)
	def __len__(self): return len(self.stack)
