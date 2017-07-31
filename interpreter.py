from tokenizer import tokenize
from preprocessor import preprocess
from modeselector import select

from stack import Stack

def interpret(functions, arguments):
	stack = Stack(arguments)
	print(stack)
	for function in functions:
		function(stack, arguments)
	return stack

def evaluate(code, arguments):
	return interpret(select(preprocess(tokenize(code)), arguments[0]).funclist, arguments)

def IN(prompt = ''):
	print(prompt, end = '')
	inp = input().strip()
	if not inp: return [0]
	return [eval(inp)]

if __name__ == '__main__':
	while True:
		print(evaluate(input(), IN()))
