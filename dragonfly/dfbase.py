import sys
import typing
from abc import ABC, abstractmethod

from PyQt5.QtCore import QFile, QIODevice, QTextStream, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtXml import QDomDocument, QDomNode

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

	def __init__(self, game: "Game") -> None:
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

		self.__dictionary = Dictionary(self)
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
	def dictionary(self) -> "Dictionary":
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
	def player(self) -> "dragonfly.syntax.Noun":
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

class Dictionary:
	"""Contains a list of nouns, verbs and exits."""
	def __init__(self, game: "Game") -> None:
		self.__game = game
		self.__nouns = []
		self.__verbs = []
		self.__articles = []
		self.__exits = []
		self.__conversations = []

		self.__gameOver = dragonfly.gameover.GameOver(self)

		self.__seeListDialog = dragonfly.dialogs.ListDialog("You can see: ", ", ", " and ")
		self.__propperListDialog = dragonfly.dialogs.PropperListDialog("is here", "are here", ", ", " and ")
		self.__objectChooserDialog = dragonfly.ObjectChooserDialog("Which one?", "Never mind.", "Please, enter the correct option.")
		self.__inventoryDialog = dragonfly.ListDialog("You have: ", ", ", " and ")
		self.__lookInsideDialog = dragonfly.ListDialog("Inside there is: ", ", ", " and ")

	def __str__(self) -> str:
		result = "Nouns:\n"
		for n in self.__nouns:
			result += f"{str(n)}\n"

		result += "\nVerbs:\n"
		for v in self.__verbs:
			result += f"{str(v)}\n"

		result += "\nArticle:\n"
		for a in self.__articles:
			result += f"{str(a)}\n"

		result += "\nExits:\n"
		for e in self.__exits:
			result += f"{str(e)}\n"

		return result

	@property
	def game(self) -> "Game":
		"""Return the game instance.

		Returns:
			Game: the game instance
		"""
		return self.__game

	@property
	def seeListDialog(self) -> "dragonfly.dialogs.ListDialog":
		"""Return the See List Dialog of the game.
		"""
		return self.__seeListDialog

	@seeListDialog.setter
	def seeListDialog(self, dialog: "dragonfly.dialogs.ListDialog"):
		"""Set the See List Dialog of the game.
		"""
		self.__seeListDialog = dialog

	@property
	def propperListDialog(self) -> "dragonfly.dialogs.PropperListDialog":
		"""Return the PropperListDialog used by LookAround action
		"""
		return self.__propperListDialog
	
	@propperListDialog.setter
	def propperListDialog(self, dialog: "dragonfly.dialogs.PropperListDialog") -> None:
		"""Set the PropperListDialog used by LookAround action
		"""
		self.__propperListDialog = dialog

	@property
	def objectChooserDialog(self) -> "dragonfly.dialogs.ObjectChooserDialog":
		"""Return the Object Chooser Dialog of the game.
		"""
		return self.__objectChooserDialog

	@objectChooserDialog.setter
	def objectChooserDialog(self, dialog: "dragonfly.dialogs.ObjectChooserDialog") -> None:
		"""Set the Object Chooser Dialog of the game.
		"""
		self.__objectChooserDialog = dialog

	@property
	def inventoryDialog(self) -> "dragonfly.dialogs.ListDialog":
		"""Return the Inventory Dialog of the game.
		"""
		return self.__inventoryDialog

	@inventoryDialog.setter
	def inventoryDialog(self, dialog: "dragonfly.dialogs.ListDialog") -> None:
		"""Set the Inventory Dialog of the game.
		"""
		self.__inventoryDialog = dialog

	@property
	def lookInsideDialog(self) -> "dragonfly.dialogs.ListDialog":
		"""Return the Look Inside Dialog of the game.
		"""
		return self.__lookInsideDialog

	@lookInsideDialog.setter
	def lookInsideDialog(self, dialog: "dragonfly.dialogs.ListDialog") -> None:
		"""Set the Look Inside Dialog of the game.
		"""
		self.__lookInsideDialog = dialog

	def nounByID(self, id: int) -> "dragonfly.Noun":
		for n in self.__nouns:
			if n.id == id: return n

		return None

	def nouns(self, name: str = "") -> typing.List["dragonfly.Noun"]:
		"""Return a list of the nouns wich responds to name."""
		if name == "": return self.__nouns
		result = []
		for n in self.__nouns:
			if n.responds(name): result.append(n)

		return result

	def verbs(self, name: str = "") -> typing.List["dragonfly.Verb"]:
		"""Return a list of the verbs wich responds to name.
		"""
		if name == "": return self.__verbs
		result = []
		for v in self.__verbs:
			if v.responds(name): result.append(v)

		return result

	def verbByAction(self, actionClassName: str) -> "dragonfly.Verb":
		"""Return a first ocurrence of the verb indicating the action class name.
		Action class name must be fully name (module.Class), for otherwise use 'actions'
		module by default.
		"""
		actionClass, error = dragonfly.helper.getClass(actionClassName, defaultModule="dragonfly.actions")
		if not actionClass:
			raise dragonfly.DragonflyException(error)
		for v in self.__verbs:
			if v.action == actionClass: return v

		return None

	def article(self, name: str) -> "dragonfly.Article":
		"""Return article instance y name.
		"""
		for a in self.__articles:
			if a.name.lower() == name.strip().lower():
				return a

		return None

	def exit(self, name: str) -> "dragonfly.Exit":
		"""Return exit instance by name.
		"""
		for e in self.__exits:
			if e.responds(name): return e

		return None

	def exits(self) -> typing.List["dragonfly.Exit"]:
		"""Return a list of exits.
		"""
		return self.__exits

	def articles(self) -> typing.List["dragonfly.Article"]:
		"""Return the complete article list.
		"""
		return self.__articles

	@property
	def conversations(self) -> typing.List["dragonfly.Conversation"]:
		return self.__conversations

	def conversation(self, owner: str) -> "dragonfly.Conversation":
		for c in self.conversations:
			if c.owner == owner: return c

		raise dragonfly.DragonflyException(
			f'Conversation: owner "{owner}" not found in dictionary.')

	
	@property
	def gameOver(self) -> "dragonfly.GameOver":
		return self.__gameOver

	def addNoun(self, noun: "dragonfly.Noun") -> None:
		"""Add a new noun to dictionary.
		Args:
			noun (dragonfly.Noun): A new noun instance.
		"""
		self.__nouns.append(noun)

	def addVerb(self, verb: "dragonfly.Verb") -> None:
		"""Add a new verb to dictionary.
		Args:
			verb (dragonfly.Verb): A new verb instance.
		"""
		self.__verbs.append(verb)

	def addArticle(self, article: "dragonfly.Article") -> None:
		"""Add a new article to dictionary,
		Args:
			article (dragonfly.Article): A new article instance.
		"""
		self.__articles.append(article)

	def addExit(self, exit: "dragonfly.Exit") -> None:
		"""Add a new exit to dictionary,
		Args:
			exit (dragonfly.Exit): A new exit instance.
		"""
		self.__exits.append(exit)

	def addConversation(self, conv: "dragonfly.Conversation"):
		self.__conversations.append(conv)

	def cascadeRemoveNoun(self, noun: "dragonfly.Noun") -> None:
		"""Remove the noun and recursively remove his childs.
		Args:
			noun (dragonfly.Noun): noun to remove.
		"""
		for c in noun.childs():
			self.cascadeRemoveNoun(c)

		self.__nouns.remove(noun)


	def load(self, path: str) -> None:
		"""Load the dictionary from xml document.

		Args:
			path (str): path to xml file.
		"""
		doc = QDomDocument()
		file = QFile(path)
		if not file.open(QIODevice.ReadOnly or QIODevice.Text):
			raise dragonfly.DragonflyException(f'Loading dictionary: Cannot load file: "{path}".')

		if not doc.setContent(file):
			file.close()
			raise dragonfly.DragonflyException(f'Loading dictionary: Cannot load content from xml file: "{path}".')

		file.close()

		root = doc.firstChildElement()

		if root.tagName() != "dragonfly": return None # Error

		for i in range(root.childNodes().count()):
			node = root.childNodes().at(i)
			if node.nodeType() == QDomNode.ElementNode:
				element = node.toElement()

				if element.nodeName() == "game":
					self.game.title = element.attribute("title")
					self.game.author = element.attribute("author")

				if element.nodeName() == "property":
					self.game.setProperty(element.attribute("name"), element.attribute("value"))

				if element.nodeName() == "include":
					print(f'Including "{element.attribute("path")}"...')
					self.load(element.attribute("path"))

				# Dialogs
				if element.nodeName() == "see-list-dialog":
					self.seeListDialog = dragonfly.dialogs.loadListDialog(element)
				if element.nodeName() == "propper-list-dialog":
					self.propperListDialog = dragonfly.dialogs.loadPropperListDialog(element)
				if element.nodeName() == "inventory-dialog":
					self.inventoryDialog = dragonfly.dialogs.loadListDialog(element)
				if element.nodeName() == "look-inside-dialog":
					self.lookInsideDialog = dragonfly.dialogs.loadListDialog(element)
				if element.nodeName() == "object-chooser-dialog":
					self.objectChooserDialog = dragonfly.dialogs.loadObjectChooserDialog(element)
					

				if element.nodeName() == "noun":
					noun = dragonfly.Noun()
					noun.game = self.__game
					self.addNoun(noun)
					noun.load(element)

				if element.nodeName() == "verb":
					verb = dragonfly.Verb()
					verb.game = self.__game
					self.addVerb(verb)
					verb.load(element)

				if element.nodeName() == "article":
					article = dragonfly.Article()
					article.load(element)
					self.addArticle(article)

				if element.nodeName() == "exit":
					e = dragonfly.Exit()
					e.load(element)
					self.addExit(e)

				if element.nodeName() == "conversation":
					c = dragonfly.Conversation()
					c.load(element)
					self.addConversation(c)
				
				if element.nodeName() == "game-over":
					self.__gameOver.load(element)

	def clear(self) -> None:
		"""Remove all data from dictionary.
		"""
		self.__nouns.clear()
		self.__verbs.clear()
		self.__exits.clear()
		self.__articles.clear()
