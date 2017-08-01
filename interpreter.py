from tokenizer import tokenize
from preprocessor import preprocess
from modeselector import select

from stack import Stack

class Interpreter:
	def __init__(self, functions, arguments):
		self.functions = functions
		self.arguments = arguments
		self.argument_index = 0
		self.stack = Stack(None)
		self.queued = []
		self.lowest_arity = -1
	def next(self):
		if self.queued and self.lowest_arity <= len(self.stack):
			for function in self.queued:
				if function[0] <= len(self.stack):
					function[1](self.stack, self.arguments)
					self.queued.remove(function)
					return
		elif self.functions:
			function = self.functions.pop(0)
			if function[0] <= len(self.stack):
				function[1](self.stack, self.arguments)
			else:
				self.queued.append(function)
				if self.lowest_arity == -1 or self.lowest_arity > function[0]:
					self.lowest_arity = function[0]
		elif self.argument_index < len(self.arguments):
			self.stack.push(self.arguments[self.argument_index])
			self.argument_index += 1
		else:
			raise RuntimeError('Arguments and stack exhausted and unterminated commands exist')

def interpret(functions, arguments):
	interpreter = Interpreter(functions, arguments)
	while interpreter.functions or interpreter.queued:
		interpreter.next()
	return interpreter.stack

def evaluate(code, arguments):
	return interpret(select(preprocess(tokenize(code)), arguments).funclist, arguments)

def IN(prompt = ''):
	print(prompt, end = '')
	inp = input().strip()
	if not inp: return [0]
	val = eval(inp)
	return val if isinstance(val, list) else [val]

if __name__ == '__main__':
	while True:
		print(evaluate(input(), IN()))
