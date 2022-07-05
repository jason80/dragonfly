import typing

class ConsoleStyles:
	def __init__(self) -> None:
		self.__defaults = {
							"family": "Sans",
							"size": 14,
							"bold": False,
							"italic": False,
							"color": "#000"
						}

		self.__current = {}
		self.reset()

	def __str__(self) -> str:
		return str(self.__current)

	@property
	def current(self) -> typing.Dict:
		return self.__current

	def reset(self) -> None:
		self.__current = self.__defaults.copy()

	def parse(self, style: str) -> None:
		members = style.split(";")
		for m in members:
			self.__parseMember(m.strip())

	def __parseMember(self, m: str) -> None:
		member = m.split(":")
		if len(member) != 2:
			# error
			return None

		key, value = member[0].strip(), member[1].strip()

		if not value:
			# error
			return None

		# Parse string
		if value.startswith("'") or value.startswith('"'):
			if len(value) == 1:
				# error
				return None

			if not value.endswith(value[0]):
				# error
				return None
			
			self.__current[key] = value[1:-1] # Estract the string characters

		# Parse boolean
		if value == "False" or value == "false":
			self.__current[key] = False
		if value == "True" or value == "true":
			self.__current[key] = True

		# Parse integer
		try:
			integer = int(value)
			self.__current[key] = integer
		except:
			# error
			return None
