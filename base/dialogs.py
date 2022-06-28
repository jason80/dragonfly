
from output.console import Console
from PyQt5.QtXml import QDomElement
import typing
import entities

class ListDialog:
	def __init__(self, initialMessage: str, separator: str, andSeparator: str) -> None:
		self.__initialMessage = initialMessage
		self.__separator = separator
		self.__andSeparator = andSeparator

	def execute(self, nouns: typing.List["entities.Noun"]):
		result = f"{self.__initialMessage} "

		for i in range(len(nouns)):
			if i != 0:
				if i == len(nouns) - 1:
					result += self.__andSeparator
				else:
					result += self.__separator

			result += nouns[i].article

		Console.println(result)
		
class ObjectChooserDialog:
	def __init__(self, message: str, cancel: str, error: str) -> None:
		self.__message = message
		self.__cancel = cancel
		self.__error = error

	def execute(self, objects: typing.List["entities.Noun"]) -> "entities.Noun":
		if len(objects) == 1: return objects[0]

		success = False
		opt = 0
		result = None

		while not success:
			Console.println(f"{self.__message}:")
			for i in range(len(objects)):
				Console.println(f"{i + 1}) {objects[i].article}.")
			Console.println(f"0) {self.__cancel}.")

			input = Console.input()

			try:
				opt = int(input.strip())
			except:
				self.printError()
				continue

			if opt < 0 or opt > len(objects):
				self.printError()
				continue

			if opt:
				result = objects[opt - 1]
			else:
				Console.println("")
				Console.println(self.__cancel)

			success = True

		return result

	def printError(self):
		Console.println("")
		Console.println(self.__error)

def loadListDialog(element: QDomElement) -> ListDialog:
	return ListDialog(element.attribute("initial-message"),
		element.attribute("separator"), element.attribute("and-separator"))

def loadObjectChooserDialog(element: QDomElement) -> ObjectChooserDialog:
	return ObjectChooserDialog(element.attribute("message"),
		element.attribute("cancel"), element.attribute("error"))
