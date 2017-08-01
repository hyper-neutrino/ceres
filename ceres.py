import sys
import interpreter

usage = '''

Ceres - A sequence-oriented recreational golfing language

ceres.py e <code> [arguments...] - Evaluate Ceres code from the third command line argument

ceres.py f <file> [arguments...] - Evaluate Ceres code from the contents of the file whose path is the third command line argument

'''

def unbool(array):
	if isinstance(array, list):
		return list(map(unbool, array))
	return 1. if array is True else 0. if array is False else array

def cut(array):
	if isinstance(array, list):
		return list(map(cut, array))
	return int(array) if isinstance(array, (int, float, complex)) and array % 1 == 0 else array

if __name__ == '__main__':
	if len(sys.argv) < 3 or sys.argv[1] not in 'ef': raise SystemExit(usage)
	if sys.argv[1] == 'e':
		code = sys.argv[2]
	else:
		code = open(sys.argv[2]).read()
	arguments = list(map(interpreter.floatify, map(eval, sys.argv[3:])))
	result = interpreter.evaluate(code, arguments)
	if result: print(cut(unbool(result.pop())))
