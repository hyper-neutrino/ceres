import primes
import operator
import math
import codepage

from stack import Stack
from copy import deepcopy

def depth(value):
	if isinstance(value, list):
		return max(list(map(depth, value)) or [0]) + 1
	else:
		return 0

def vectorize1(monad, maxdepth = -1):
	def inner(arg, maxdepth = maxdepth):
		if maxdepth and isinstance(arg, list) and depth(arg) > maxdepth:
			return [inner(k, maxdepth - 1) for k in arg]
		else:
			return monad(arg)
	return inner

def vectorize2(dyad, maxdepth = -1):
	def inner(left, right, maxdepth = maxdepth):
		if maxdepth and isinstance(left, list) and isinstance(right, list) and depth(left) > maxdepth and depth(right) > maxdepth:
			output = []
			longer = left if len(left) > len(right) else right
			index = 0
			while index < min(map(len, [left, right])):
				output.append(inner(left[index], right[index], maxdepth - 1))
				index += 1
			return output + longer[index:]
		elif maxdepth and isinstance(left, list) and depth(left) > maxdepth:
			return [inner(arg, right, maxdepth - 1) for arg in left]
		elif maxdepth and isinstance(right, list) and depth(right) > maxdepth:
			return [inner(left, arg, maxdepth - 1) for arg in right]
		else:
			return dyad(left, right)
	return inner

def flatten(array):
	if isinstance(array, list):
		output = []
		for element in array:
			element = flatten(element)
			if isinstance(element, list):
				output.extend(element)
			else:
				output.append(element)
		return output
	return array

def mold(left, right):
	for index in range(len(right)):
		if isinstance(right[index], list):
			mold(left, right[index])
		else:
			item = left.pop(0)
			right[index] = item
			left.append(item)
	return right

def czip(filler = None):
	def zipper(array):
		columns = []
		for i in range(max(map(len, array))):
			columns.append([row[i] for row in array if len(row) > i] if filler == None else [row[i] if len(row) > i else filler for row in array])
		return columns
	return zipper

def reqInt(function):
	return lambda *values: function(*list(map(int, values)))

def reducer(dyad):
	def reduce(iterable, arguments):
		iterable = iterable.pop()
		while len(iterable) > 1:
			iterable.insert(0, dyad(Stack([iterable.pop(0), iterable.pop(0)]), arguments))
		if iterable: return iterable.pop()
		raise ValueError('reduce over empty list')
	return reduce

def cumreducer(dyad):
	def cumreduce(iterable, arguments):
		iterable = iterable.pop()
		for i in range(len(iterable) - 1):
			iterable[i + 1] = dyad(Stack([iterable[i], iterable[i + 1]]), arguments)
		if iterable: return iterable
		raise ValueError('reduce over empty list')
	return cumreduce

def smartsum(iterable, arguments):
	return reducer(__(vectorize2(operator.add)))(iterable, arguments)

def smartprod(iterable, arguments):
	return reducer(__(vectorize2(operator.mul)))(iterable, arguments)

def cumsum(iterable, arguments):
	return cumreducer(__(vectorize2(operator.add)))(iterable, arguments)

def _i(function):
	return lambda stack, arguments: function(stack.getIterable())

def _I(function):
	return lambda stack, arguments: function(stack.empty())

def _(function):
	return lambda stack, arguments: function(stack.pop())

def __(function):
	return lambda stack, arguments: function(stack.pop(), stack.pop())

def listify(function):
	return lambda *arguments: list(function(*arguments))

def incrange(left, right):
	if left == right: return []
	delta = 1 if right > left else -1
	return list(range(left, right + delta, delta))

def veclist(function):
	def inner(array):
		if depth(array) == 1: return function(array)
		if depth(array) == 0: return function([array])
		return list(map(inner, array))
	return inner

differences = _i(veclist(lambda array: [array[i] - array[i - 1] for i in range(1, len(array))]))

def Range(start, end, inclstart, inclend):
	sign = 1 if end > start else -1
	return list(range(start + sign * (1 - inclstart), end + sign * inclend, sign))

def basedigits(base):
	def inner(number):
		if number < 0: return [-x for x in inner(-number)]
		digits = []
		if number == 0: return [0]
		if number % 1:
			digits = inner(int(number))
			digits[-1] += number % 1
			return digits
		number = int(number)
		for power in range(int(math.log(number, base)), -1, -1):
			digits.append(number // base ** power)
			number %= base ** power
		return digits
	return inner

def undigits(base):
	def inner(array):
		return sum(array[-i - 1] * base ** i for i in range(len(array)))
	return _i(veclist(inner))

atoms = {
	'Ḏ': lambda stack, arguments: stack.push(stack.peek()),
	'P': _(vectorize1(reqInt(primes.Primes.isPrime))),
	'Ṗ': _(vectorize1(reqInt(primes.Primes.generatePrimesUpTo))),
	'Ṕ': _(vectorize1(reqInt(primes.Primes.nextPrime))),
	'B': _(vectorize1(basedigits(2))),
	'Ḃ': undigits(2),
	'D': _(vectorize1(basedigits(10))),
	'Ḋ': undigits(10),
	'E': _i(lambda x: all(k == x[0] for k in x)),
	'F': _(flatten),
	'I': differences,
	'J': _i(lambda x: list(range(1, len(x) + 1))),
	'K': _i(lambda x: mold(list(range(1, len(flatten(x)) + 1)), x)),
	'L': _(len),
	'Ḷ': _(vectorize1(reqInt(lambda x: Range(0, x, 1, 0)))),
	'İ': _(vectorize1(reqInt(lambda x: Range(0, x, 1, 1)))),
	'R': _(vectorize1(reqInt(lambda x: Range(0, x, 0, 1)))),
	'Ē': _(vectorize1(reqInt(lambda x: Range(0, x, 0, 0)))),
	'S': smartsum,
	'Ṡ': cumsum,
	'∘': smartprod,
	'Z': _(czip()),
	'd': lambda stack, arguments: _(vectorize1(basedigits(stack.pop())))(Stack([stack.pop()]), arguments),
	'ḋ': lambda stack, arguments: undigits(stack.pop())(stack, arguments),
	'm': __(mold),
	'r': __(vectorize2(reqInt(incrange))),
	'z': __(lambda x, y: czip(x)(y)),
	'ż': __(vectorize2(lambda x, y: [x, y], 1)),
	'ÆU': _i(vectorize1(lambda x: x[::-1] if isinstance(x, list) else [x], 1)),
	'ÆW': _I(lambda x: x),
	'Æw': _i(tuple),
	'ÆṘ': _i(lambda x: x[::-1] if isinstance(x, list) else [x]),
	'ÆP': lambda stack, arguments: ''.join(flatten(vectorize1(reqInt(chr))(stack.pop()))),
	'Æp': lambda stack, arguments: ''.join(flatten(vectorize1(reqInt(codepage.codepage.__getitem__))(stack.pop()))),
	'ŒB': _i(vectorize1(lambda x: x[:-1] + x[::-1] if isinstance(x, list) else [x], 1)),
	'ŒḂ': _i(lambda x: x[:-1] + x[::-1] if isinstance(x, list) else [x]),
	'+': __(vectorize2(operator.add)),
	'_': __(vectorize2(operator.sub)),
	'*': __(vectorize2(operator.pow)),
	'⨉': __(vectorize2(operator.mul)),
	'^': __(vectorize2(reqInt(operator.xor))),
	'&': __(vectorize2(reqInt(operator.and_))),
	'|': __(vectorize2(reqInt(operator.or_))),
	'%': __(vectorize2(operator.mod)),
	'=': __(vectorize2(lambda x, y: x == y)),
	'∈': __(lambda x, y: x in y),
	'~': _(vectorize1(reqInt(lambda x: ~x))),
	'¬': _(vectorize1(reqInt(operator.not_))),
	'⁺': _(vectorize1(lambda x: x + 1)),
	'⁻': _(vectorize1(lambda x: x - 1)),
	'⁼': __(lambda x, y: x == y),
	'!': _(vectorize1(lambda x: math.gamma(x + 1))),
	'₁': lambda stack, arguments: stack.evalr([stack.index - 1]).pop(),
	'₂': lambda stack, arguments: stack.evalr([stack.index - 2]).pop(),
	'₃': lambda stack, arguments: stack.evalr([stack.index - 3]).pop(),
	'₄': lambda stack, arguments: stack.evalr([stack.index - 4]).pop(),
	'₅': lambda stack, arguments: stack.evalr([stack.index - 5]).pop(),
	'₆': lambda stack, arguments: stack.evalr([stack.index - 6]).pop(),
	'₇': lambda stack, arguments: stack.evalr([stack.index - 7]).pop(),
	'₈': lambda stack, arguments: stack.evalr([stack.index - 8]).pop(),
	'₉': lambda stack, arguments: stack.evalr([stack.index - 9]).pop(),
	'¹': lambda stack, arguments: stack.pop(),
	'²': _(vectorize1(lambda x: x ** 2)),
}

def _p(function):
	def inner(stack, arguments):
		val = function(stack, arguments)
		if val == None: return
		if not isinstance(val, tuple): val = (val,)
		stack.push(*val)
	return inner

def _q(predicate, amount):
	def pusher(functions):
		functions.append(predicate(*[functions.pop() for i in range(amount)]))
	return pusher

def join(func1, func2):
	def inner(stack, arguments):
		return func1(Stack([func2(stack, arguments)]), arguments)
	return inner

def mapper(function):
	def inner(stack, arguments):
		return [function(Stack([val]), arguments) for val in stack.getIterable()]
	return inner

def leftmapper(function):
	def inner(stack, arguments):
		fixed_point = stack.pop()
		iterable = stack.pop()
		if isinstance(iterable, list):
			return [function(Stack([fixed_point, val]), arguments) for val in iterable]
		else:
			raise RuntimeError('Cannot left-map over non-iterable and cannot infer defaults')
	return inner

def rightmapper(function):
	def inner(stack, arguments):
		iterable = stack.pop()
		fixed_point = stack.pop()
		if isinstance(iterable, list):
			return [function(Stack([val, fixed_point]), arguments) for val in iterable]
		else:
			raise RuntimeError('Cannot right-map over non-iterable and cannot infer defaults')
	return inner

def dualmapper(function):
	def inner(stack, arguments):
		i1 = stack.pop()
		i2 = stack.pop()
		if isinstance(i1, list) and isinstance(i2, list):
			return [function(Stack([v1, v2]), arguments) for v2 in i2 for v1 in i1]
		else:
			raise RuntimeError('Cannot dual-map over non-iterable and cannot infer defaults')
	return inner

def unindexer(function):
	def inner(stack, arguments, index = None):
		index = stack.pop() if index == None else index
		if isinstance(index, list): return [inner(stack, arguments, i) for i in index]
		instances = 0
		number = 1
		while instances < index:
			if function(Stack([number]), arguments):
				instances += 1
			number += 1
		return number - 1
	return inner

def antiunindexer(function):
	return unindexer(lambda x,a: not function(x,a))

def filterer(function):
	def inner(stack, arguments):
		return [x for x in stack.getIterable() if function(Stack([x]), arguments)]
	return inner

def antifilterer(function):
	return filterer(lambda x,a: not function(x,a))

def exists(function):
	def inner(stack, arguments):
		return any(function(x) for x in stack.getIterable())
	return inner

def notexists(function):
	return exists(lambda x,a: not function(x,a))

def swapper(function):
	def inner(stack, arguments):
		value = stack.pop()
		lower = stack.pop()
		stack.push(value)
		stack.push(lower)
		return function(stack, arguments)
	return inner

quicks = {
	'$': _q(join, 2),
	'€': _q(mapper, 1),
	'₤': _q(leftmapper, 1),
	'ʀ': _q(rightmapper, 1),
	'⨰': _q(dualmapper, 1),
	'⨅': _q(unindexer, 1),
	'⨆': _q(antiunindexer, 1),
	'░': _q(filterer, 1),
	'▓': _q(antifilterer, 1),
	'/': _q(reducer, 1),
	'\\': _q(cumreducer, 1),
	'∃': _q(exists, 1),
	'∄': _q(notexists, 1),
	'@': _q(swapper, 1)
}

def safeGetFunction(key):
	if key in atoms:
		return atoms[key]
	elif key in quicks:
		return quicks[key]
	else:
		return key
