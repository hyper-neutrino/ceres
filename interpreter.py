import primes
import operator
import math
import functions

from tokenizer import tokenize
from preprocessor import preprocess
from modeselector import select

from stack import Stack

from copy import deepcopy

def interpret(functions, arguments, evalr):
	stack = Stack([], deepcopy(arguments), evalr, arguments[0])
	while functions:
		value = functions.pop(0)(stack, arguments)
		if value == None: continue
		if not isinstance(value, tuple): value = (value,)
		stack.push(*value)
	return stack

def evaluate(code, arguments):
	return interpret(select(preprocess(tokenize(code)), arguments).funclist, arguments, lambda vals: evaluate(code, vals))

def floatify(val):
	if isinstance(val, (list, tuple)): return list(map(floatify, list(val)))
	return float(val)

def IN(prompt = ''):
	print(prompt, end = '')
	inp = input().strip()
	if not inp: return [0]
	val = eval(inp)
	return floatify(val if isinstance(val, list) else [val])

if __name__ == '__main__':
	while True:
		print(evaluate(input(), IN()))
