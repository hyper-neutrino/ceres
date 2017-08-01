from preprocessor import Mode, preprocess
import tokenizer

def select(modes, arguments):
	arguments = arguments or [0]
	matching = []
	try:
		max_priority = max(map(Mode.priority, modes))
	except ValueError:
		raise RuntimeError('Empty code is invalid')
	selected = None
	for mode in modes:
		if mode.verifier(arguments[0]):
			if mode.priority == max_priority:
				selected = mode
				break
			else:
				matching.append(mode)
	if not selected:
		if not matching:
			raise RuntimeError('No matching modes')
		else:
			max_priority = max(map(Mode.priority, matching))
			selected = [match for match in matching if match.priority == max_priority][0]
	return selected

if __name__ == '__main__':
	while True:
		modes = preprocess(tokenizer.tokenize(input()))
		selection = select(modes, tokenizer.parseNumber(input()))
		print(modes.index(selection), selection, selection.funclist)
