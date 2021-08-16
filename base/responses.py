from PyQt5.QtXml import QDomDocument, QDomElement, QDomNode

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
