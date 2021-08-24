from dfexcept import DragonflyException
import sys
import typing
from abc import ABC, abstractmethod

from PyQt5.QtCore import QFile, QIODevice, QTextStream, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtXml import QDomDocument, QDomNode

import dialogs
import entities
import syntax.parser
import helper.forname
import output.console
import checks

class ExecWorker(QThread):

	console_print = pyqtSignal(dict)
	console_clear = pyqtSignal()

	def __init__(self, game: "Game") -> None:
		super().__init__()
		self.game = game

	def run(self) -> None:
		while True:
			line = output.console.Console.input()
			output.console.Console.println("")
			output.console.Console.println(line, "family: 'Courier'") # Console echo
			self.game.execute(line)

class Game(ABC):
	"""Dragonfly Game base entity"""
	def __init__(self, consoleWidth: int = 1000, consoleHeight: int = 600, testMode: bool = False) -> None:

		if not testMode:
			self.__app = QApplication(sys.argv)
			self.__execWorker = ExecWorker(self)
			self.__console = output.console.Console(self, consoleWidth, consoleHeight)

		self.__dictionary = Dictionary(self)
		self.__parser = syntax.parser.Parser(self)
		self.__player = None

		self.__properties = dict()

	@property
	def properties(self) -> typing.Dict:
		return self.__properties

	def getProperty(self, name: str) -> str:
		return self.__properties[name]
	
	def setProperty(self, name: str, value: str) -> None:
		self.__properties[name] = value

	@property
	def execWorker(self) -> ExecWorker:
		return self.__execWorker

	@property
	def dictionary(self) -> "Dictionary":
		return self.__dictionary

	@property
	def parser(self) -> "syntax.parser.Parser":
		return self.__parser

	@property
	def player(self) -> "entities.Noun":
		return self.__player
	
	@player.setter
	def player(self, player: "entities.Noun") -> None:
		self.__player = player

	def execute(self, text: str):
		self.__parser.parse(text)

	@abstractmethod
	def init(self) -> None:
		pass

	def run(self):

		print("*** Dragonfly Library ***")
		print("Initializing ...")

		# Defaults
		self.setProperty("show-parsing-process", "false")
		self.setProperty("look-around", "never")

		self.init()

		if self.getProperty("show-parsing-process") == "true":
			print("[Parser] showing parsing process.")
			self.parser.showParsingProcess = True
		elif self.getProperty("show-parsing-process") == "false":
			print("[Parser] hiding parsing process.")
			self.parser.showParsingProcess = False
		else:
			raise DragonflyException("Game Property: show-parsing-process expect true/false value.")

		# Missing check
		print("Executing missing check ...")
		missing = checks.MissingCheck(self)
		missing.check()

		print(f'Player: "{self.player.name}" located in "{self.player.container.name}".')

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
		self.__console.close()

class Dictionary:
	"""Contains a list of nouns, verbs and exits."""
	def __init__(self, game: "Game") -> None:
		self.__game = game
		self.__nouns = []
		self.__verbs = []
		self.__articles = []
		self.__exits = []

		self.__seeListDialog = dialogs.ListDialog("You can see: ", ", ", " and ")
		self.__objectChooserDialog = dialogs.ObjectChooserDialog("Which one?", "Never mind.", "Please, enter the correct option.")
		self.__inventoryDialog = dialogs.ListDialog("You have: ", ", ", " and ")
		self.__lookInsideDialog = dialogs.ListDialog("Inside there is: ", ", ", " and ")

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
		return self.__game

	@property
	def seeListDialog(self) -> "dialogs.ListDialog":
		return self.__seeListDialog

	@seeListDialog.setter
	def seeListDialog(self, dialog: "dialogs.ListDialog"):
		self.__seeListDialog = dialog

	@property
	def objectChooserDialog(self) -> "dialogs.ObjectChooserDialog":
		return self.__objectChooserDialog

	@objectChooserDialog.setter
	def objectChooserDialog(self, dialog: "dialogs.ObjectChooserDialog") -> None:
		self.__objectChooserDialog = dialog

	@property
	def inventoryDialog(self) -> "dialogs.ListDialog":
		return self.__inventoryDialog

	@inventoryDialog.setter
	def inventoryDialog(self, dialog: "dialogs.ListDialog") -> None:
		self.__inventoryDialog = dialog

	@property
	def lookInsideDialog(self) -> "dialogs.ListDialog":
		return self.__lookInsideDialog

	@lookInsideDialog.setter
	def lookInsideDialog(self, dialog: "dialogs.ListDialog") -> None:
		self.__lookInsideDialog = dialog

	def nouns(self, name: str = "") -> typing.List["entities.Noun"]:
		"""Returns a list of the nouns wich responds to name."""
		if name == "": return self.__nouns
		result = []
		for n in self.__nouns:
			if n.responds(name): result.append(n)

		return result

	def verbs(self, name: str = "") -> typing.List["entities.Verb"]:
		if name == "": return self.__verbs
		result = []
		for v in self.__verbs:
			if v.responds(name): result.append(v)

		return result

	def verbByAction(self, actionClassName: str) -> "entities.Verb":
		actionClass = helper.forname.getClass(actionClassName, defaultModule="actions")
		for v in self.__verbs:
			if v.action == actionClass: return v

		return None

	def article(self, name: str) -> "entities.Article":
		for a in self.__articles:
			if a.name.lower() == name.strip().lower():
				return a

		return None

	def exit(self, name: str) -> "entities.Exit":
		for e in self.__exits:
			if e.responds(name): return e

		return None

	def articles(self) -> typing.List["entities.Article"]:
		return self.__articles

	def addNoun(self, noun: "entities.Noun") -> None:
		self.__nouns.append(noun)

	def addVerb(self, verb: "entities.Verb") -> None:
		self.__verbs.append(verb)

	def addArticle(self, article: "entities.Article") -> None:
		self.__articles.append(article)

	def addExit(self, exit: "entities.Exit") -> None:
		self.__exits.append(exit)

	def load(self, path: str) -> None:
		doc = QDomDocument()
		file = QFile(path)
		if not file.open(QIODevice.ReadOnly or QIODevice.Text):
			raise DragonflyException(f'Loading dictionary: Cannot load file: "{path}".')

		if not doc.setContent(file):
			file.close()
			raise DragonflyException(f'Loading dictionary: Cannot load content from xml file: "{path}".')

		file.close()

		root = doc.firstChildElement()

		if root.tagName() != "dictionary": return None # Error

		for i in range(root.childNodes().count()):
			node = root.childNodes().at(i)
			if node.nodeType() == QDomNode.ElementNode:
				element = node.toElement()

				if element.nodeName() == "noun":
					noun = entities.Noun()
					noun.game = self.__game
					self.addNoun(noun)
					noun.load(element)

				if element.nodeName() == "verb":
					verb = entities.Verb()
					verb.game = self.__game
					self.addVerb(verb)
					verb.load(element)

				if element.nodeName() == "article":
					article = entities.Article()
					article.load(element)
					self.addArticle(article)

				if element.nodeName() == "exit":
					e = entities.Exit()
					e.load(element)
					self.addExit(e)

	def save(self, path: str) -> None:
		doc = QDomDocument()

		p_inst = doc.createProcessingInstruction("xml", 'version="1.0" encoding="UTF-8"')
		doc.appendChild(p_inst)

		root = doc.createElement("dictionary")
		doc.appendChild(root)

		# Save nouns
		for n in self.__nouns:
			if not n.container:
				root.appendChild(n.save(doc))

		# Save verbs
		for v in self.__verbs:
			root.appendChild(v.save(doc))
	
		# Save articles
		for a in self.__articles:
			root.appendChild(a.save(doc))

		# Save exits
		for e in self.__exits:
			root.appendChild(e.save(doc))

		# Write file
		file = QFile(path)
		if not file.open(QFile.WriteOnly or QFile.Truncate):
			raise DragonflyException(f'Cannot write file: "{path}"')

		outstream = QTextStream(file)
		doc.save(outstream, 4)
		outstream.flush()
		file.close()

	def clear(self) -> None:
		self.__nouns.clear()
		self.__verbs.clear()
		self.__exits.clear()
		self.__articles.clear()