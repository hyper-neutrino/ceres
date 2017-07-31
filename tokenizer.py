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

modes = {
	'≺': (1, 1, lambda value, argument: value < argument),
	'≻': (1, 1, lambda value, argument: value > argument),
	'≼': (1, 1, lambda value, argument: value <= argument),
	'≽': (1, 1, lambda value, argument: value >= argument)
}

def force_literal_eval(token):
	if token[0] == 'literal':
		return token[1]
	else:
		raise RuntimeError('force_literal_eval can only process literals')

class Tokenizer:
	def __init__(self, code, index = 0):
		self.code = code
		self.index = index
	def __iter__(self):
		return self
	def __next__(self):
		if self.index >= len(self.code): raise StopIteration
		if self.code[self.index] == ' ': self.index += 1; return self.__next__()
		if self.code[self.index] in '0123456789-.ıȷ':
			decimals = self.code[self.index] == '.'
			rcurrent = self.code[self.index]
			specials = self.code[self.index] in 'ıȷ'
			newliter = self.code[self.index] in 'ıȷ'
			self.index   += 1
			while self.index < len(self.code) and (self.code[self.index] in '0123456789' or self.code[self.index] == '.' and not decimals or self.code[self.index] in '-.' and newliter or self.code[self.index] in 'ıȷ' and not specials):
				specials |= self.code[self.index] in 'ıȷ'
				newliter = self.code[self.index] in 'ıȷ'
				decimals |= self.code[self.index] in '.ȷ'
				rcurrent += self.code[self.index]
				self.index += 1
			return ('literal', parseNumber(rcurrent))
		elif self.code[self.index] in '[':
			sections = []
			brackets = 1
			self.index += 1
			while brackets and self.index < len(self.code):
				if self.code[self.index] == ',' and brackets == 1:
					sections = (sections or ['']) + ['']
				else:
					if self.code[self.index] == ']':
						brackets -= 1
						if not brackets: self.index += 1; break
					elif self.code[self.index] == '[':
						brackets += 1
					sections = (sections or [''])
					sections[-1] += self.code[self.index]
				self.index += 1
			return ('literal', [item[0][1] for item in map(tokenize, sections) if len(item) == 1 and item[0][0] == 'literal'])
		elif self.code[self.index] in 'ÆæŒœ':
			self.index += 2
			return ('atom', functions.safeGetFunction(self.code[self.index - 2:self.index]))
		elif self.code[self.index] in modes:
			mode = modes[self.code[self.index]]
			self.index += 1
			arguments = [force_literal_eval(self.__next__()) for i in range(mode[0])]
			return ('mode', (mode[1], lambda value: mode[2](value, *arguments)))
		elif self.code[self.index] in functions.atoms:
			self.index += 1
			return  ('atom', functions.safeGetFunction(self.code[self.index - 1]))
		elif self.code[self.index] in functions.quicks:
			self.index += 1
			return ('quick', functions.safeGetFunction(self.code[self.index - 1]))
		else:
			raise RuntimeError('Unknown token\n%s\n%s' % (self.code, ' ' * self.index + '^'))

def tokenize(code):
	return list(Tokenizer(code))

if __name__ == '__main__':
	while True:
		print(tokenize(input()))
