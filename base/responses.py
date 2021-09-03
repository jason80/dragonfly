from PyQt5.QtXml import QDomDocument, QDomElement, QDomNode
from dfexcept import DragonflyException

import action
import entities
from output.console import Console

class Message(action.ActionResponse):

	def __init__(self) -> None:
		self.message = ""
		self.style = ""
		self.newLine = True

	def execute(self, action: "action.Action") -> None:
		if self.newLine: Console.println(self.message, self.style)
		else: Console.print(self.message, self.style)

	def load(self, element: QDomElement) -> None:

		self.style = element.attribute("style")
		nl = element.attribute("new-line", defaultValue = "true")
		if nl == "true": self.newLine = True
		elif nl == "false": self.newLine = False
		else:
			# Error
			pass

		for i in range(element.childNodes().count()):
			node = element.childNodes().at(i)
			if node.nodeType() == QDomNode.TextNode:
				self.message = node.toText().data().strip()

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("style", self.style)
		element.setAttribute("new-line", "true" if self.newLine else "false")

		element.appendChild(doc.createTextNode(self.message))

		return element

class Attr(action.ActionResponse):
	def __init__(self) -> None:
		self.instance = ""
		self.set = ""
		self.unset = ""

	def execute(self, action: "action.Action") -> None:
		objList = action.dictionary.nouns(self.instance)
		if not objList:
			raise DragonflyException(f'On Set response: noun "{self.instance}" not found in dictionary.')

		obj = objList[0]

		sets = []
		for s in self.set.split(","):
			sets.append(s.strip())

		unsets = []
		for u in self.__unset.split(","):
			unsets.append(u.strip())

		obj.set(sets)
		obj.unset(unsets)

	def load(self, element: QDomElement) -> None:
		self.instance = element.attribute("instance")
		self.set = element.attribute("set", defaultValue="")
		self.unset = element.attribute("unset", defaultValue="")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)

		element.setAttribute("instance", self.instance)
		if self.set: element.setAttribute("set", self.set)
		if self.unset: element.setAttribute("unset", self.unset)

		return element

class AppendName(action.ActionResponse):
	def __init__(self) -> None:
		self.instance = ""
		self.name = ""

	def execute(self, action: "action.Action") -> None:
		objList = action.dictionary.nouns(self.instance)
		if not objList:
			raise DragonflyException(f'On AppendName response: noun "{self.instance}" not found in dictionary.')
		
		obj = objList[0]
		obj.appendName(self.name)

	def load(self, element: QDomElement) -> None:
		self.instance = element.attribute("instance", defaultValue="")
		self.name = element.attribute("name", defaultValue="")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("instance", self.instance)
		element.setAttribute("name", self.name)

		return element

class Move(action.ActionResponse):
	def __init__(self) -> None:
		self.instance = ""
		self.destiny = ""

	def getObj(self, action: "action.Action", name: str) -> "entities.Noun":
		objList = action.dictionary.nouns(name)
		if not objList: return None
		return objList[0]

	def execute(self, action: "action.Action") -> None:
		obj = self.getObj(action, self.instance)
		if not obj: raise DragonflyException(f'On Move response: noun "{self.instance}" not found in dictionary.')

		dest = self.getObj(action, self.destiny)
		if not dest: raise DragonflyException(f'On Move response: destiny "{self.destiny}" not found in dictionary.')

		obj.container = dest

	def load(self, element: QDomElement) -> None:
		self.instance = element.attribute("instance", defaultValue="")
		self.destiny = element.attribute("destiny", defaultValue="")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("instance", self.instance)
		element.setAttribute("destiny", self.destiny)
		
		return element