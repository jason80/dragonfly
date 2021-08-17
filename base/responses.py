from PyQt5.QtXml import QDomDocument, QDomElement, QDomNode
from dfexcept import DragonflyException

import action
from output.console import Console

class Message(action.ActionResponse):

	def __init__(self) -> None:
		self.__message = ""
		self.__style = ""
		self.__newLine = True

	def execute(self, action: "action.Action") -> None:
		if self.__newLine: Console.println(self.__message, self.__style)
		else: Console.print(self.__message, self.__style)

	def load(self, element: QDomElement) -> None:

		self.__style = element.attribute("style")
		nl = element.attribute("new-line", defaultValue = "true")
		if nl == "true": self.__newLine = True
		elif nl == "false": self.__newLine = False
		else:
			# Error
			pass

		for i in range(element.childNodes().count()):
			node = element.childNodes().at(i)
			if node.nodeType() == QDomNode.TextNode:
				self.__message = node.toText().data().strip()

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("style", self.__style)
		element.setAttribute("new-line", "true" if self.__newLine else "false")

		element.appendChild(doc.createTextNode(self.__message))

		return element

class Attr(action.ActionResponse):
	def __init__(self) -> None:
		self.__instance = ""
		self.__set = ""
		self.__unset = ""

	def execute(self, action: "action.Action") -> None:
		objList = action.dictionary.nouns(self.__instance)
		if not objList:
			raise DragonflyException(f'On Set response: noun "{self.__instance}" not found in dictionary.')

		obj = objList[0]

		sets = []
		for s in self.__set.split(","):
			sets.append(s.strip())

		unsets = []
		for u in self.__unset.split(","):
			unsets.append(u.strip())

		obj.set(sets)
		obj.unset(unsets)

	def load(self, element: QDomElement) -> None:
		self.__instance = element.attribute("instance")
		self.__set = element.attribute("set", defaultValue="")
		self.__unset = element.attribute("unset", defaultValue="")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)

		element.setAttribute("instance", self.__instance)
		if self.__set: element.setAttribute("set", self.__set)
		if self.__unset: element.setAttribute("unset", self.__unset)

		return element

class AppendName(action.ActionResponse):
	def __init__(self) -> None:
		self.__instance = ""
		self.__name = ""

	def execute(self, action: "action.Action") -> None:
		objList = action.dictionary.nouns(self.__instance)
		if not objList:
			raise DragonflyException(f'On AppendName response: noun "{self.__instance}" not found in dictionary.')
		
		obj = objList[0]
		obj.appendName(self.__name)

	def load(self, element: QDomElement) -> None:
		self.__instance = element.attribute("instance", defaultValue="")
		self.__name = element.attribute("name", defaultValue="")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("instance", self.__instance)
		element.setAttribute("name", self.__name)

		return element