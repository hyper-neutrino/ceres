import primes

atoms = {
	'P': primes.Primes.isPrime
}

quicks = {
	'€': lambda function: 0
}

nilads = []

monads = ['P']

dyads = []

quicks = []

def safeGetFunction(key):
	if key in functions:
		return functions[key]
	return key
