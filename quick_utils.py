from preprocessor import Atom

def _(function):
	return lambda atoms: atoms.append(Atom(function(atoms.pop().function)))
