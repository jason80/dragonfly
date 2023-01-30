from PyQt5.QtXml import QDomDocument, QDomElement

class Connection:
	def __init__(self) -> None:
		self.__exit = ""
		self.__destiny = ""

	def __str__(self) -> str:
		return f"{self.__exit} --> {self.__destiny}"

	@property
	def exit(self) -> str:
		return self.__exit

	@exit.setter
	def exit(self, exit: str) -> None:
		self.__exit = exit

	@property
	def destiny(self) -> str:
		return self.__destiny

	@destiny.setter
	def destiny(self, dest: str) -> None:
		self.__destiny = dest
	
	def load(self, element: QDomElement) -> None:
		self.__exit = element.attribute("exit")
		self.__destiny = element.attribute("destiny")
