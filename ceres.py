import sys
import interpreter

code_page  = '''................................ !"#$%&'()*+,-./0123456789:;<=>?'''
code_page += '''@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~.'''
code_page += '''................................................................'''
code_page += '''............................................................≺≻≼≽'''

usage = '''

Ceres - A sequence-oriented recreational golfing language

ceres.py e <code> [arguments...] - Evaluate Ceres code from the third command line argument

ceres.py f <file> [arguments...] - Evaluate Ceres code from the contents of the file whose path is the third command line argument

'''

if __name__ == '__main__':
	if len(sys.argv) < 3 or sys.argv[1] not in 'ef': raise SystemExit(usage)
	if sys.argv[1] == 'e':
		code = sys.argv[2]
	else:
		code = open(sys.argv[2]).read()
	arguments = list(map(eval, sys.argv[3:]))
	result = interpreter.evaluate(code, arguments)
	if result: print(result.pop())
