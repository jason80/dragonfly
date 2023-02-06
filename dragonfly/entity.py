import typing

from PyQt5.QtXml import QDomElement

import dragonfly
import dragonfly.helper

class Entity():
	"""Base of the nouns, verbs and exits.
	Contains the multi-name property, and game and dictionary instances."""
	def __init__(self) -> None:
		self.__names = []
		self.__game = None
		self.__dictionary = None

	def __str__(self) -> str:
		return str(self.__names)

	@property
	def game(self) -> "dragonfly.Game":
		"""Return the game instance.
		"""
		return self.__game

	@game.setter
	def game(self, g: "dragonfly.Game") -> None:
		"""Set the game instance."""
		self.__game = g
		self.__dictionary = g.dictionary

	@property
	def dictionary(self) -> "dragonfly.Dictionary":
		"""Return the dictionary instance.
		"""
		return self.__dictionary

	@property
	def names(self) -> typing.List[str]:
		"""Return the complete name list.
		"""
		return self.__names

	@names.setter
	def names(self, n: typing.List[str]) -> None:
		"""Set the complete name list.
		"""
		self.__names = n

	@property
	def name(self) -> str:
		"""Return the first name of the entity."""
		return self.__names[0] if self.__names else ""

	def responds(self, name: str) -> bool:
		"""Returns True if the entity responds to the name."""
		for n in self.__names:
			if dragonfly.helper.isEquals(n, name): return True

		return False

	def appendName(self, name: str) -> None:
		"""Add a new name at top of the list of names if it not responds to the name."""
		if not self.responds(name):
			self.__names.insert(0, name)

	def load(self, element: QDomElement) -> None:
		"""Load the entity from xml element.
		"""
		self.names.clear()
		for n in element.attribute("names").split(","):
			self.names.append(n.strip())
		