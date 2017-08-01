import tokenizer
from copy import deepcopy
from core import chain

class Mode:
	def __init__(self, priority, verifier, funclist):
		self.priority, self.verifier, self.funclist = priority, verifier, funclist
	def priority(self): return self.priority
	def verifier(self): return self.verifier
	def funclist(self): return self.funclist

def preprocess(tokens):
	components = []
	for index in range(len(tokens)):
		token = tokens[index]
		if token[0] == 'mode':
			components.append((token[1][0], token[1][1], []))
		else:
			if not components: components.append((0, lambda arguments: True, []))
			if token[0] == 'literal':
				value = deepcopy(token[1])
				def pusher(value):
					def get(stack, arguments):
						return value
					return get
				components[-1][2].append(pusher(value))
			elif token[0] == 'atom':
				components[-1][2].append(token[1])
			elif token[0] == 'quick':
				token[1](components[-1][2])
	return [Mode(*component) for component in components]

if __name__ == '__main__':
	while True:
		print(preprocess(tokenizer.tokenize(input())))
