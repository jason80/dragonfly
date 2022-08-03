import typing
from abc import ABC, abstractmethod

from PyQt5.QtXml import QDomDocument, QDomElement, QDomNode

import dragonfly
import dragonfly.helper
import dragonfly.syntax
from dragonfly.output import Console

class Action(ABC):
	"""Represents an action performed by the player.
	When the verb is parser, the associated action is executed by execute() method.
	"""
	def __init__(self) -> None:
		self.__game = None
		self.__verb = None
		self.__sendingEvents = []

	@property
	def game(self) -> "dragonfly.Game":
		"""Returns the game instance
		"""
		return self.__game

	@game.setter
	def game(self, game: "dragonfly.Game") -> None:
		"""Sets the game instance
		"""
		self.__game = game

	@property
	def dictionary(self) -> "dragonfly.Dictionary":
		"""Returns the dictionary instance
		"""
		return self.__game.dictionary

	@property
	def parser(self) -> "dragonfly.syntax.Parser":
		"""Returns the parser instance.
		"""
		return self.__game.parser

	@property
	def verb(self) -> "dragonfly.Verb":
		"""Returns the associated verb.
		"""
		return self.__verb

	@verb.setter
	def verb(self, verb: "dragonfly.Verb") -> None:
		"""(Used by the parser) sets the associated verb.
		"""
		self.__verb = verb

	@abstractmethod
	def init(self) -> bool:
		"""Initialize the action. Behavior depends on the type of action.
		Direct and indirect objects are usually looked up in the dictionary and 
		if these objects are not found, False is returned for cancel the action.

		Returns:
			bool: False: causes the action to be cancelled.
		"""
		pass

	@abstractmethod
	def check(self) -> bool:
		"""The action check consists in verifying if an object
		complies with the norm of the action. Example:
		LookInside checks if the direct object is not "closed".
		"the player will not be able to see inside the chest if it is closed"

		Returns:
			bool: False: causes the action to be cancelled.
		"""
		pass

	@abstractmethod
	def carryOut(self) -> None:
		"""Perform the action. Example:
		If the action is TakeObject, the direct object is moved to player's inventory.
		"""
		pass

	@abstractmethod
	def report(self) -> None:
		"""Report occurs after when action has been performed. Usually show a message.
		Example:
		"you get a flashlight"
		"""
		pass

	def execute(self) -> None:
		"""The execute() method has the following steps:
		1)	Abstract method init(): initialize the action. If False is
			returned from init(), action is cancelled.
		1a)	Execute before event on objects handled by the action. If False is returned
			from doBefore() method, action is cancelled.
		2)	Abstract method check(): check the action. False: action is cancelled.
		3)	Abstract method carryOut(): perform the action.
		3b)	Execute after event on objects handled by the action. If False is returned
			from doAfter() method, action is cancelled in this point.
		4)	Abstract method report(): report the action after performed.
		"""
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

	def sendEventLater(self, noun: "dragonfly.Noun") -> None:
		"""Add the target object to list. This list will be used to send before
		and after events.

		Args:
			noun (dragonfly.Noun): Target object
		"""
		self.__sendingEvents.append(noun)

	def fireResponse(self, id: str) -> bool:
		"""Execute a verb's response. The response may exists in the verb and show
		the response message. The verb is associated with the current action.

		Args:
			id (str): response id declared in the verb.

		Raises:
			dragonfly.DragonflyException: The response not exists.

		Returns:
			bool: ALWAYS returns false for programming convenience.
		"""
		if not self.__verb.hasResponse(id):
			raise dragonfly.DragonflyException(f"Verb {self.__verb} has not response: {id}.")

		Console.println(self.__verb.getResponse(id))
		return False

	@abstractmethod
	def responses(self) -> typing.Tuple[str]:
		"""Return a list of all responses that may occurs.
		"""
		pass

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

	@property
	def responses(self) -> typing.List["ActionResponse"]:
		return self.__responses

	@property
	def conditions(self) -> typing.List["Condition"]:
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
