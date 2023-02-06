import typing

import dragonfly

from PyQt5.QtXml import QDomElement, QDomNode

class ActionEvent:
	def __init__(self) -> None:
		self.__actions = []
		self.__cancel = False

		self.__responses = []
		self.__conditions = []

	def __str__(self) -> str:
		lst = []
		for a in self.__actions:
			if a.__module__ != "actions":
				lst.append(f"{a.__module__}.{a.__name__}")
			else: lst.append(f"{a.__name__}")

		return ", ".join(lst)

	@property
	def actions(self) -> typing.List:
		return self.__actions

	@property
	def cancel(self) -> bool:
		return self.__cancel

	@cancel.setter
	def cancel(self, cancel: bool) -> None:
		self.__cancel = cancel

	def match(self, action: "dragonfly.Action") -> bool:
		return action.__class__ in self.__actions

	def addResponse(self, response: "dragonfly.ActionResponse") -> None:
		self.__responses.append(response)

	def addCondition(self, condition: "dragonfly.Condition") -> None:
		self.__conditions.append(condition)

	def checkConditions(self, action: "dragonfly.Action") -> bool:
		check = True
		for cond in self.__conditions:
			if not cond.check(action): check = False

		return check

	def execute(self, action: "dragonfly.Action") -> None:
		for r in self.__responses:
			r.execute(action)

	@property
	def responses(self) -> typing.List["dragonfly.ActionResponse"]:
		return self.__responses

	@property
	def conditions(self) -> typing.List["dragonfly.Condition"]:
		return self.__conditions

	def load(self, element: QDomElement) -> None:
		# Load action list
		for a in element.attribute("actions").split(","):
			aClass, error = dragonfly.helper.getClass(a.strip(), defaultModule="dragonfly.actions")
			if not aClass:
				raise dragonfly.DragonflyException(error)
			self.__actions.append(aClass)
			
		self.__cancel = element.attribute("cancel") == "true"
		
		# Load responses and conditions
		for i in range(element.childNodes().count()):
			child = element.childNodes().at(i)

			# simple text found: create a message response:
			if child.nodeType() == QDomNode.TextNode:
				text = child.toText().data().strip()
				if not text: continue

				messageClass, error = dragonfly.helper.getClass("Message", defaultModule="responses")
				if not messageClass:
					raise dragonfly.DragonflyException(error)
				
				message = messageClass()
				message.message = text
				self.addResponse(message)

			# condition and response found:
			if child.nodeType() == QDomNode.ElementNode:
				e = child.toElement()
				if e.nodeName() == "response":
					responseClass, error = dragonfly.helper.getClass(e.attribute("class"), defaultModule="responses")
					if not responseClass:
						raise dragonfly.DragonflyException(error)
					response = responseClass()
					response.load(e)
					self.addResponse(response)

				if e.nodeName() == "if":
					condClass, error = dragonfly.helper.getClass(e.attribute("class"), defaultModule="conditions")
					if not condClass:
						raise dragonfly.DragonflyException(error)
					cond = condClass()
					cond.load(e)
					self.addCondition(cond)
