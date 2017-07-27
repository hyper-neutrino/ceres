#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Tokenizer for 
'''

import functions

def parseNumber(string, default = 0):
	if 'ȷ' in string:
		left, right = tuple(string.split('ȷ'))
		return parseNumber(left, 1) * 10 ** parseNumber(right, 3)
	elif 'ı' in string:
		left, right = tuple(string.split('ı'))
		return parseNumber(left, 0) + parseNumber(right, 1) * 1j
	elif string == '-':
		return -1
	elif string == '.':
		return 0.5
	elif string == '-.':
		return -0.5
	elif string.endswith('.'):
		return float(string) + 0.5
	elif string:
		return float(string)
	else:
		return default

def tokenize(code):
	index = 0
	tokens = []
	while index < len(code):
		if code[index] == ' ': index += 1; continue
		if code[index] in '0123456789-.ıȷ':
			decimals = code[index] == '.'
			rcurrent = code[index]
			specials = code[index] in 'ıȷ'
			newliter = code[index] in 'ıȷ'
			index   += 1
			while index < len(code) and (code[index] in '0123456789' or code[index] == '.' and not decimals or code[index] in '-.' and newliter or code[index] in 'ıȷ' and not specials):
				specials |= code[index] in 'ıȷ'
				newliter = code[index] in 'ıȷ'
				decimals |= code[index] in '.ȷ'
				rcurrent += code[index]
				index += 1
			tokens.append(('literal', parseNumber(rcurrent)))
		elif code[index] in '[':
			sections = []
			brackets = 1
			index += 1
			while brackets:
				if code[index] == ',' and brackets == 1:
					sections = (sections or ['']) + ['']
				else:
					if code[index] == ']':
						brackets -= 1
						if not brackets: index += 1; break
					elif code[index] == '[':
						brackets += 1
					sections = (sections or [''])
					sections[-1] += code[index]
				index += 1
			tokens.append(('literal', [item[0][1] for item in map(tokenize, sections) if len(item) == 1 and item[0][0] == 'literal']))
		elif code[index] in 'ÆæŒœ':
			tokens.append(('operator', functions.safeGetFunction(code[index:index + 2])))
			index += 2
		else:
			tokens.append(('operator', functions.safeGetFunction(code[index])))
			index += 1
	return tokens

if __name__ == '__main__':
	while True:
		print(tokenize(input()))
