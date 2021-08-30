import typing
from abc import ABC, abstractmethod

from PyQt5.QtXml import QDomDocument, QDomElement, QDomNode

import dfbase
import entities
import helper.forname
import syntax.parser
from dfexcept import DragonflyException
from output.console import Console


class Action(ABC):
	def __init__(self) -> None:
		self.__game = None
		self.__verb = None
		self.__sendingEvents = []

	@property
	def game(self) -> "dfbase.Game":
		return self.__game

	@game.setter
	def game(self, game: "dfbase.Game") -> None:
		self.__game = game

	@property
	def dictionary(self) -> "dfbase.Dictionary":
		return self.__game.dictionary

	@property
	def parser(self) -> "syntax.Parser":
		return self.__game.parser

	@property
	def verb(self) -> "entities.Verb":
		return self.__verb

	@verb.setter
	def verb(self, verb: "entities.Verb") -> None:
		self.__verb = verb

	@abstractmethod
	def init(self) -> bool:
		pass

	@abstractmethod
	def check(self) -> bool:
		pass

	@abstractmethod
	def carryOut(self) -> None:
		pass

	@abstractmethod
	def report(self) -> None:
		pass

	def execute(self) -> None:
		self.__sendingEvents.clear()

		# Initialize action
		if not self.init(): return None

		# BEFORE EVENT
		for n in self.__sendingEvents:
			if not n.doBefore(self): return None

		# Check action
		if not self.check(): return None

		self.__sendingEvents.clear()

		# Action performs the changes
		self.carryOut()

		# AFTER EVENT
		for n in self.__sendingEvents:
			if not n.doAfter(self): return None

		# Report the result
		self.report()

	def sendEventLater(self, noun: "entities.Noun") -> None:
		self.__sendingEvents.append(noun)

	def fireResponse(self, id: str) -> bool:
		if not self.__verb.hasResponse(id):
			raise DragonflyException(f"Verb {self.__verb} has not response: {id}.")

		Console.println(self.__verb.getResponse(id))
		return False

class ActionEvent:
	def __init__(self) -> None:
		self.__actions = []
		self.__cancel = False

		self.__responses = []
		self.__conditions = []

	def __str__(self) -> str:
		lst = []
		for a in self.__actions:
			lst.append(str(a))

		return ", ".join(lst)

	@property
	def actions(self) -> typing.List:
		return self.__actions

	@property
	def cancel(self) -> bool:
		return self.__cancel

	def match(self, action: Action) -> bool:
		return action.__class__ in self.__actions

	def addResponse(self, response: "ActionResponse") -> None:
		self.__responses.append(response)

	def addCondition(self, condition: "Condition") -> None:
		self.__conditions.append(condition)

	def checkConditions(self, action: Action) -> bool:
		check = True
		for cond in self.__conditions:
			if not cond.check(action): check = False

		return check

	def execute(self, action: Action) -> None:
		for r in self.__responses:
			r.execute(action)


	def load(self, element: QDomElement) -> None:
		# Load action list
		for a in element.attribute("actions").split(","):
			aClass = helper.forname.getClass(a.strip(), defaultModule="actions")
			self.__actions.append(aClass)
			
		self.__cancel = element.attribute("cancel") == "true"
		
		# Load responses and conditions
		for i in range(element.childNodes().count()):
			child = element.childNodes().at(i)
			if child.nodeType() == QDomNode.ElementNode:
				e = child.toElement()
				if e.nodeName() == "response":
					responseClass = helper.forname.getClass(e.attribute("class"), defaultModule="responses")
					response = responseClass()
					response.load(e)
					self.addResponse(response)

				if e.nodeName() == "if":
					condClass = helper.forname.getClass(e.attribute("class"), defaultModule="conditions")
					cond = condClass()
					cond.load(e)
					self.addCondition(cond)

	def save(self, doc: QDomDocument, nodeName: str) -> QDomElement:
		element = doc.createElement(nodeName)
		
		# Save action class names
		aNames = []
		for a in self.__actions:
			aNames.append(a.__name__)

		element.setAttribute("actions", ", ".join(aNames))

		# Cancel
		element.setAttribute("cancel", "true" if self.__cancel else "false")

		# Conditions
		for c in self.__conditions:
			element.appendChild(c.save(doc))

		# Responses
		for r in self.__responses:
			element.appendChild(r.save(doc))

		return element

		
class ActionResponse(ABC):
	def __init__(self) -> None:
		pass

	@abstractmethod
	def execute(self, action: Action) -> None:
		pass

	@abstractmethod
	def load(self, element: QDomElement) -> None:
		pass

	@abstractmethod
	def save(self, doc: QDomDocument) -> QDomElement:
		element = doc.createElement("response")
		element.setAttribute("class", self.__class__.__name__)
		return element

class Condition(ABC):
	def __init__(self) -> None:
		pass

	@abstractmethod
	def check(self, action: Action) -> bool:
		pass

	@abstractmethod
	def load(self, element: QDomElement):
		pass

	@abstractmethod
	def save(self, doc: QDomDocument) -> QDomElement:
		element = doc.createElement("if")
		element.setAttribute("class", self.__class__.__name__)

		return element
