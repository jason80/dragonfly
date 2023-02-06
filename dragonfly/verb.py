import typing
import dragonfly

from PyQt5.QtXml import QDomElement, QDomNode

class Verb(dragonfly.Entity):
	"""Represents the multi-name command wich is associated to Action.
	"""
	def __init__(self) -> None:
		super().__init__()

		self.__action = None
		self.__syntax = []

		self.__responses = {}

	def __str__(self) -> str:
		return f"{super().__str__()} ({self.__action})"

	@property
	def action(self) -> typing.Type["dragonfly.Action"]:
		"""Return the action associated with this verb."""
		return self.__action

	@action.setter
	def action(self, action: typing.Type["dragonfly.Action"]) -> None:
		"""Set the associated action"""
		self.__action = action

	@property
	def syntax(self) -> typing.List[str]:
		"""Return the verb's syntax."""
		return self.__syntax

	@syntax.setter
	def syntax(self, syntax: typing.List[str]) -> None:
		"""Set the verb's syntax."""
		self.__syntax = syntax

	@property
	def responses(self) -> typing.Dict:
		"""Return a dictionary with the responses of the verb.

		Returns:
			typing.Dict: responses of the verb.
		"""
		return self.__responses

	def getResponse(self, id: str) -> str:
		"""Return the response indicating the if of self. The responses are quieried by the
		action associated.

		Args:
			id (str): the response's id.

		Returns:
			str: the response.
		"""
		return self.__responses[id] if id in self.__responses else ""

	def setResponse(self, id: str, response: str) -> None:
		"""Set a response to the verb.

		Args:
			id (str): the id of the response.
			response (str): the response text.
		"""
		self.__responses[id] = response

	def hasResponse(self, id: str) -> bool:
		"""Check if response exists.

		Args:
			id (str): the id of the response.

		Returns:
			bool: True if and only if the verb contains the response.
		"""
		return id in self.__responses

	def load(self, element: QDomElement):
		"""Load verb from xml element.

		Args:
			element (QDomElement): the xml element.
		"""
		super().load(element)

		# Verb base
		actionString = element.attribute("action")
		self.action, error = dragonfly.helper.getClass(actionString, defaultModule = "dragonfly.actions")
		if not self.action:
			raise dragonfly.DragonflyException(error)
		if element.attribute("syntax"):
			for member in element.attribute("syntax").split(","):
				self.syntax.append(member.strip())

		# Responses
		for i in range(element.childNodes().count()):
			node = element.childNodes().at(i)
			if node.nodeType() == QDomNode.ElementNode:
				child = node.toElement()
				if child.nodeName() == "response":
					self.setResponse(child.attribute("id"), child.attribute("string"))
