class Stack:
	def __init__(self, stack = None, extras = None, evalr = None, index = 0):
		self.stack = stack and list(stack) or []
		self.extras = extras and list(extras) or []
		self.evalr = evalr if isinstance(evalr, (type(print), type(lambda:0))) else lambda *a: evalr
		self.index = index
	def pop(self):
		if not self.stack and self.extras: return self.extras.pop(0)
		return self.stack.pop()
	def peek(self):
		if self.stack:
			return self.stack[-1]
		return self.extras[0]
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
	def getIterable(self):
		if not self.stack or not isinstance(self.stack[-1], list):
			stack = self.stack
			self.stack = []
			return stack
		return self.pop()
	def peekIterable(self):
		if not self.stack or not isinstance(self.stack[-1], list):
			return self.stack
		return self.stack[-1]
	def  __str__(self): return str(self.stack)
	def __repr__(self): return str(self.stack)
	def __len__(self): return len(self.stack)
