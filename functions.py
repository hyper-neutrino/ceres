import primes

def _(function):
	def internal(functions):
		func = functions.pop()
		functions.append(function(func))
	return internal

def __(function):
	def internal(functions):
		func1 = functions.pop()
		func2 = functions.pop()
		functions.append(function(func2, func1))
	return internal

atoms = {
	'P': lambda stack, arguments: stack.push(primes.Primes.isPrime(stack.pop()))
}

quicks = {
	'$': __(lambda func1, func2: lambda stack, arguments: bool(func1(stack, arguments)) ^ bool(func2(stack, arguments)))
}

def safeGetFunction(key):
	if key in atoms:
		return atoms[key]
	elif key in quicks:
		return quicks[key]
	else:
		return key
