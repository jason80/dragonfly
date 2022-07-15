def getClass(className: str, defaultModule: str = ""):
	"""Create and return a new instance from a classname string."""
	parts = className.split(".")
	module = ".".join(parts[:-1])
	if not module:
		module = defaultModule
		parts.insert(0, defaultModule)
	
	try:
		m = __import__(module)
		for comp in parts[1:]:
			m = getattr(m, comp)

		return m, ""
	except:
		return None, f'Class "{module}.{className}" not found.'
