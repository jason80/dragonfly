from typing import List
import dfbase
import entities
#import action
#import responses
import helper.forname

class MissingCheck:
	def __init__(self, game: "dfbase.Game") -> None:
		self.game = game
		self.dict = self.game.dictionary

	def check(self) -> None:
		self.__checkActions()

		# Find places
		if not self.dict.nouns():
			room = entities.Noun()
			room.game = self.game
			room.names = ["The First Room", "room"]

			""" # Description
			after = action.ActionEvent()
			after.actions.append(helper.forname.getClass("LookAround", "actions"))
			after.addResponse(responses.Message("A simple description."))
			room.addAfter(after) """
			self.dict.addNoun(room)

			self.__report(f"created a simple room: {room}")

		# Find player
		if not self.game.player:
			player = entities.Noun()
			player.game = self.game
			player.names = ["player"]
			player.container = self.dict.nouns()[0]
			self.dict.addNoun(player)
			self.game.player = player
			self.__report(f"created a player: {str(player)} in place {str(player.container)}")

	def __checkActions(self):

		# Check missing verbs
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
