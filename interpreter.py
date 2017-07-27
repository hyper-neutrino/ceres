from parser import Section
from sympy import *

PHI = (1 + sqrt(5)) / 2

def fibonacci(index):
	return (PHI ** index - ((-PHI) ** (-index))) / sqrt(5)

cache = {}

def evaluate(codetree):
	pass

def _interpret(sections, index, *args):
	matching = []
	maxpriority = max(map(Section.priority, sections))
	selected = None
	for section in sections:
		if section.matches(index):
			if section.priority == maxpriority:
				selected = section
				break
			else:
				matching.append(section)
	if not selected:
		if not matching:
			return fibonacci(index)
		else:
			maxpriority = max(map(Section.priority, matching))
			selected = [match for match in matching if match.priority == maxpriority]

def interpret(sections, index, *args):
	key = (sections, index) + tuple(args)
	if key in cache:
		return cache[key]
	else:
		result = _interpret(sections, index)
		cache[key] = result
		return result
