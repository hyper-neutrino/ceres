def safe(generator, default):
	try:
		return generator()
	except:
		return default
