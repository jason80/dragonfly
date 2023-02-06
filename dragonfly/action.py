import typing
from abc import ABC, abstractmethod

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
