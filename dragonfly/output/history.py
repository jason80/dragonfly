class History:
	def __init__(self) -> None:
		self.__content = []
		self.__index = 0

	def store(self, line: str) -> None:
		self.__index = 0
		self.__content.append(line)

	def up(self) -> str:
		if not self.__content: return ""

		self.__index -= 1
		if self.__index < 0: self.__index = len(self.__content) - 1

		return self.__content[self.__index]

	def down(self) -> str:
		if not self.__content: return ""

		self.__index += 1
		if self.__index >= len(self.__content): self.__index = 0

		return self.__content[self.__index]
	