import sys
import typing
from abc import ABC, abstractmethod

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication

import dragonfly
import dragonfly.output
from dragonfly.persistence import Persistence
import dragonfly.syntax
import dragonfly.checks
import dragonfly.dialogs
import dragonfly.helper
import dragonfly.conversation
import dragonfly.gameover

class ExecWorker(QThread):
	"""ExecWorker is a thread that runs alongside the nautilus application.
	The loop expect the user input, print an echo and execute the line entered.
	Args:
		QThread ([type]): [description]
	"""
	console_print = pyqtSignal(dict)
	console_clear = pyqtSignal()
	console_quit = pyqtSignal()

	def __init__(self, game: "dragonfly.Game") -> None:
		super().__init__()
		self.game = game

	def run(self) -> None:
		"""Loop contains: expect input, print echo and execute."""
		while True:
			line = dragonfly.output.Console.input()
			dragonfly.output.Console.println("")
			dragonfly.output.console.Console.println(line, "family: 'Courier'") # Console echo
			self.game.execute(line)

class Game(ABC):
	"""Dragonfly Game base entity"""
	def __init__(self, consoleWidth: int = 1000, consoleHeight: int = 600, testMode: bool = False) -> None:

		if not testMode:
			self.__app = QApplication(sys.argv)
			self.__execWorker = ExecWorker(self)
			self.__console = dragonfly.output.Console(self, consoleWidth, consoleHeight)

		self.__title = ""
		self.__author = ""

		self.__dictionary = dragonfly.Dictionary(self)
		self.__parser = dragonfly.syntax.Parser(self)
		self.__player = None

		self.__properties = dict()

	@property
	def title(self) -> str:
		return self.__title

	@title.setter
	def title(self, title: str) -> None:
		self.__title = title

	@property
	def author(self) -> str:
		return self.__author

	@author.setter
	def author(self, author: str) -> None:
		self.__author = author

	@property
	def properties(self) -> typing.Dict:
		"""Return the game properties.

		Returns:
			typing.Dict: A dictionary containing the properties.
		"""
		return self.__properties

	def getProperty(self, name: str) -> str:
		"""Return a property value.

		Args:
			name (str): Property key.

		Returns:
			str: the property value.
		"""
		return self.__properties[name]
	
	def setProperty(self, name: str, value: str) -> None:
		"""Set a property. Create if not exists.

		Args:
			name (str): Key of the property.
			value (str): Value of the property.
		"""
		self.__properties[name] = value

	@property
	def execWorker(self) -> ExecWorker:
		"""Return the exec worker thread.

		Returns:
			ExecWorker: The exec worker instance.
		"""
		return self.__execWorker

	@property
	def dictionary(self) -> "dragonfly.Dictionary":
		"""Return the dictionary of the game.

		Returns:
			Dictionary: The dictionary of the game.
		"""
		return self.__dictionary

	@property
	def parser(self) -> "dragonfly.syntax.Parser":
		"""Return the parser.

		Returns:
			syntax.parser.Parser: The parser.
		"""
		return self.__parser

	@property
	def player(self) -> "dragonfly.Noun":
		"""Return the game's player.

		Returns:
			entities.Noun: The player noun.
		"""
		return self.__player
	
	@player.setter
	def player(self, player: "dragonfly.Noun") -> None:
		"""Set the game player.

		Args:
			player (entities.Noun): The player noun.
		"""
		self.__player = player

	def execute(self, text: str):
		self.__parser.parse(text)

	@abstractmethod
	def init(self) -> None:
		"""Derived class implements this method to initialize game components.
		"""
		pass

	def run(self):
		"""Run the game.
		"""

		print("*** Dragonfly Library ***")
		print("Initializing ...")

		# Defaults
		self.setProperty("show-parsing-process", "false")
		self.setProperty("look-around", "never")
		self.setProperty("hide-title", "false")
		self.setProperty("player", "")

		self.init()

		# Sets player
		if self.getProperty("player"):
			self.player = self.dictionary.nouns(self.getProperty("player"))[0]

		if self.getProperty("show-parsing-process") == "true":
			print("[Parser] showing parsing process.")
			self.parser.showParsingProcess = True
		elif self.getProperty("show-parsing-process") == "false":
			print("[Parser] hiding parsing process.")
			self.parser.showParsingProcess = False
		else:
			raise dragonfly.DragonflyException("Game Property: show-parsing-process expect true/false value.")

		# Missing check
		print("Executing missing check ...")
		missing = dragonfly.checks.MissingCheck(self)
		missing.check()

		print(f'Player: "{self.player.name}" located in "{self.player.container.name}".')

		# Game Title
		if self.getProperty("hide-title") == "false":
			self.showTitle()
		elif self.getProperty("hide-title") == "true":
			print("Hidding game title ...")
		else:
			print("Warn: Expected true/false value on hide-title property. Assuming false.")
			self.showTitle()

		# Visibility behavior
		if self.getProperty("look-around") == "on-start" or self.getProperty("look-around") == "always":
			lookVerb = self.dictionary.verbByAction("LookAround")
			self.execute(lookVerb.name)
		elif self.getProperty("look-around") == "never":
			pass
		else:
			print("Warn: Expected never/on-start/always value on disable-prologue property. Assuming never.")
			self.setProperty("look-around", "never")

		print(f"Visibility behavior: look-around = {self.getProperty('look-around')}")

		print("Running ...")

		self.__console.show()

		self.execWorker.start()

		sys.exit(self.__app.exec_())

	def close(self):
		"""Close the game and console.
		"""
		self.__execWorker.console_quit.emit()

	def showTitle(self):
		dragonfly.output.Console.println(self.__title, "size: 20; bold: true")
		dragonfly.output.console.Console.println(self.author, "size: 12")
		dragonfly.output.console.Console.println(" ", "size: 80")

	def saveGame(self):
		filename = ""
		if not self.title: filename = "Untitled.sav"
		else: filename = self.title + ".sav"
		persist = Persistence(filename)
		persist.saveGame(self.dictionary)

	def loadGame(self):
		filename = ""
		if not self.title: filename = "Untitled.sav"
		else: filename = self.title + ".sav"
		persist = Persistence(filename)
		persist.loadGame(self.dictionary)
