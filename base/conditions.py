from dfexcept import DragonflyException
from PyQt5.QtXml import QDomDocument, QDomElement
import action

class IsSet(action.Condition):
	def __init__(self) -> None:
		super().__init__()

		self.__instance = ""
		self.__attr = ""

	def check(self, action: "action.Action") -> bool:
		# Gets the noun
		noun = action.dictionary.nouns(self.__instance)
		if not noun:
			raise DragonflyException(f'On IsSet condition: instance "{self.__instance}" not found in dictionary.')
	
		return noun[0].isSet(self.__attr)

	def load(self, element: QDomElement):
		self.__instance = element.attribute("instance")
		self.__attr = element.attribute("attr")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("instance", self.__instance)
		element.setAttribute("attr", self.__attr)
		return element

class DirectEqualsExit(action.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.__exit = ""


	def check(self, action: "action.Action") -> bool:
		e = action.dictionary.exit(self.__exit)
		if not e:
			raise DragonflyException(f'On DirectEqualsExit condition: exit "{self.__exit}" not found in dictionary.')

		return e.responds(action.parser.directObjectString)

	def load(self, element: QDomElement):
		self.__exit = element.attribute("exit")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("exit", self.__exit)
		return element
		
class Contains(action.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.__container = ""
		self.__instance = ""

	def check(self, action: "action.Action") -> bool:
		cont = action.dictionary.nouns(self.__container)
		if not cont:
			raise DragonflyException(f'On Contains condition: container "{self.__container}" not found in dictionary.')

		return cont[0].contains(self.__instance)

	def load(self, element: QDomElement):
		self.__instance = element.attribute("instance", defaultValue="")
		self.__container = element.attribute("container", defaultValue="")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)

		element.setAttribute("instance", self.__instance)
		element.setAttribute("container", self.__container)

		return element