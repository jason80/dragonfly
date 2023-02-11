import typing

import dragonfly

from PyQt5.QtXml import QDomDocument, QDomNode
from PyQt5.QtCore import QFile, QIODevice

class Dictionary:
	"""Contains a list of nouns, verbs and exits."""
	def __init__(self, game: "dragonfly.Game") -> None:
		self.__game = game
		self.__nouns = []
		self.__verbs = []
		self.__articles = []
		self.__exits = []
		self.__conversations = []

		self.__gameOver = dragonfly.GameOver(self)

		self.__seeListDialog = dragonfly.ListDialog("You can see: ", ", ", " and ")
		self.__propperListDialog = dragonfly.PropperListDialog("is here", "are here", ", ", " and ")
		self.__objectChooserDialog = dragonfly.ObjectChooserDialog(self, "Which one?", "Never mind.", "Please, enter the correct option.")
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
	def game(self) -> "dragonfly.Game":
		"""Return the game instance.

		Returns:
			Game: the game instance
		"""
		return self.__game

	@property
	def seeListDialog(self) -> "dragonfly.ListDialog":
		"""Return the See List Dialog of the game.
		"""
		return self.__seeListDialog

	@seeListDialog.setter
	def seeListDialog(self, dialog: "dragonfly.ListDialog"):
		"""Set the See List Dialog of the game.
		"""
		self.__seeListDialog = dialog

	@property
	def propperListDialog(self) -> "dragonfly.PropperListDialog":
		"""Return the PropperListDialog used by LookAround action
		"""
		return self.__propperListDialog
	
	@propperListDialog.setter
	def propperListDialog(self, dialog: "dragonfly.PropperListDialog") -> None:
		"""Set the PropperListDialog used by LookAround action
		"""
		self.__propperListDialog = dialog

	@property
	def objectChooserDialog(self) -> "dragonfly.ObjectChooserDialog":
		"""Return the Object Chooser Dialog of the game.
		"""
		return self.__objectChooserDialog

	@objectChooserDialog.setter
	def objectChooserDialog(self, dialog: "dragonfly.ObjectChooserDialog") -> None:
		"""Set the Object Chooser Dialog of the game.
		"""
		self.__objectChooserDialog = dialog

	@property
	def inventoryDialog(self) -> "dragonfly.ListDialog":
		"""Return the Inventory Dialog of the game.
		"""
		return self.__inventoryDialog

	@inventoryDialog.setter
	def inventoryDialog(self, dialog: "dragonfly.ListDialog") -> None:
		"""Set the Inventory Dialog of the game.
		"""
		self.__inventoryDialog = dialog

	@property
	def lookInsideDialog(self) -> "dragonfly.ListDialog":
		"""Return the Look Inside Dialog of the game.
		"""
		return self.__lookInsideDialog

	@lookInsideDialog.setter
	def lookInsideDialog(self, dialog: "dragonfly.ListDialog") -> None:
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
					self.seeListDialog = dragonfly.loadListDialog(element)
				if element.nodeName() == "propper-list-dialog":
					self.propperListDialog = dragonfly.loadPropperListDialog(element)
				if element.nodeName() == "inventory-dialog":
					self.inventoryDialog = dragonfly.loadListDialog(element)
				if element.nodeName() == "look-inside-dialog":
					self.lookInsideDialog = dragonfly.loadListDialog(element)
				if element.nodeName() == "object-chooser-dialog":
					self.objectChooserDialog = dragonfly.loadObjectChooserDialog(self.game, element)
					

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
