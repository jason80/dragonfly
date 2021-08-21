from typing import List
import dfbase
import entities
import helper.forname

class MissingCheck:
	def __init__(self, game: "dfbase.Game") -> None:
		self.game = game
		self.dict = self.game.dictionary

	def check(self) -> None:
		self.__checkActions()

	def __checkActions(self):
		self.__createIfNotExists("Quit", ["quit", "q"])
		self.__createIfNotExists("LookAround", ["look"])

	def __createIfNotExists(self, cls: str, names: List[str]):
		verb = self.dict.verbByAction(cls)
		if not verb:
			verb = entities.Verb()
			verb.names = names
			verb.action = helper.forname.getClass(cls, defaultModule = "actions")
			self.dict.addVerb(verb)
			self.__report(f"created verb {str(verb)}")

	def __report(self, msg: str) -> None:
		print(f"[Missing check] {msg}.")
