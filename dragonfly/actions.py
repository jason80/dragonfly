import typing
import dragonfly
from dragonfly import DragonflyException
from dragonfly.output import Console

class SingleAction(dragonfly.Action):
	"""Single action takes no arguments. Usually represents verb like "jump", "scream".
		By default, SingleAction fires response: "nothing-happens"

		Responses:
		nothing-happens
	"""

	def init(self) -> bool:
		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		pass

	def report(self) -> None:
		self.fireResponse("nothing-happens")

	def responses(self) -> typing.Tuple[str]:
		return ("nothing-happens",)

class DefaultAction(dragonfly.Action):
	"""DefaultAction takes one argument (direct object).
	By default, fires response "nothing-happens"

	Responses:
	direct-not-found
	direct-is-the-player
	nothing-happens
	"""

	def init(self) -> bool:
		lst = self.game.player.childs(self.parser.directObjectString)
		lst.extend(self.game.player.container.childs(self.parser.directObjectString))

		if not lst: return self.fireResponse("direct-not-found")

		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.directObject: return False

		self.sendEventLater(self.parser.directObject)

		return True

	def check(self) -> bool:
		if self.parser.directObject == self.game.player:
			return self.fireResponse("direct-is-the-player")
		return True

	def carryOut(self) -> None:
		pass

	def report(self) -> None:
		self.fireResponse("nothing-happens")

	def responses(self) -> typing.Tuple[str]:
		return ("nothing-happens", "direct-not-found", "direct-is-the-player", )

class UnknownVerb(dragonfly.Action):
	def init(self) -> bool:
		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		self.fireResponse("unknown-verb")

	def report(self) -> None:
		pass

	def responses(self) -> typing.Tuple[str]:
		return ("unknown-verb", )

class Quit(dragonfly.Action):
	def init(self) -> bool:
		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		self.game.close()

	def report(self) -> None:
		pass

	def responses(self) -> typing.Tuple[str]:
		return ()

class Clear(dragonfly.Action):
	def init(self) -> bool:
		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		Console.clear()

	def report(self) -> None:
		pass

	def responses(self) -> typing.Tuple[str]:
		return ()

class SaveGame(dragonfly.Action):
	def init(self) -> bool:
		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		self.game.saveGame()

	def report(self) -> None:
		self.fireResponse("game-saved")

	def responses(self) -> typing.Tuple[str]:
		return ("game-saved", )

class LoadGame(dragonfly.Action):
	def init(self) -> bool:
		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		self.game.loadGame()

	def report(self) -> None:
		self.fireResponse("game-loaded")

	def responses(self) -> typing.Tuple[str]:
		return ("game-loaded", )

class Inventory(dragonfly.Action):
	def init(self) -> bool:
		self.sendEventLater(self.game.player)
		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		lst = self.game.player.childs()
		if not lst: self.fireResponse("inventory-is-empty")
		else:
			self.dictionary.inventoryDialog.execute(lst)

		self.sendEventLater(self.game.player)

	def report(self) -> None:
		pass

	def responses(self) -> typing.Tuple[str]:
		return ("inventory-is-empty", )

class ExamineObject(dragonfly.Action):
	def init(self) -> bool:

		lst = self.game.player.childs(self.parser.directObjectString)
		lst.extend(self.game.player.container.childs(self.parser.directObjectString))

		if not lst: return self.fireResponse("direct-not-found")

		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.directObject: return False

		self.sendEventLater(self.parser.directObject)

		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		self.sendEventLater(self.parser.directObject)

	def report(self) -> None:
		pass

	def responses(self) -> typing.Tuple[str]:
		return ("direct-not-found", )

class LookAround(dragonfly.Action):
	def init(self) -> bool:
		self.place = self.game.player.container
		self.sendEventLater(self.place)

		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		# Print the description of the place
		Console.println(self.place.name, "bold: true")
		self.sendEventLater(self.place)

	def report(self) -> None:
		nouns = []
		proppers = []
		for n in self.place.childs():
			if n == self.game.player: continue
			if n.isSet("scene"): continue
			if n.isSet("propper"): proppers.append(n)
			else: nouns.append(n)

		if nouns:
			Console.println("")
			self.dictionary.seeListDialog.execute(nouns)
		if proppers:
			Console.println("")
			self.dictionary.propperListDialog.execute(proppers)
	
	def responses(self) -> typing.Tuple[str]:
		return ()

class LookInside(dragonfly.Action):
	def init(self) -> bool:

		lst = self.game.player.childs(self.parser.directObjectString)
		lst.extend(self.game.player.container.childs(self.parser.directObjectString))

		if not lst: return self.fireResponse("direct-not-found")

		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.directObject: return False

		self.sendEventLater(self.parser.directObject)

		return True

	def check(self) -> bool:
		if self.parser.directObject == self.game.player:
			return self.fireResponse("direct-is-the-player")
		if not self.parser.directObject.isSet("container"):
			return self.fireResponse("direct-is-not-container")
		if self.parser.directObject.isSet("closed"):
			return self.fireResponse("direct-is-closed")

		return True

	def carryOut(self) -> None:
		childs = self.parser.directObject.childs()
		if not childs:
			self.fireResponse("container-is-empty")
		else:
			self.dictionary.lookInsideDialog.execute(childs)

		self.sendEventLater(self.parser.directObject)

	def report(self) -> None:
		pass

	def responses(self) -> typing.Tuple[str]:
		return ("direct-not-found", "direct-is-the-player", "direct-is-not-container",
					"direct-is-closed", "container-is-empty", )

class TakeObject(dragonfly.Action):
	def init(self) -> bool:
		# Get the object from the current place
		lst = self.game.player.container.childs(self.parser.directObjectString)
		if not lst: return self.fireResponse("direct-not-found")

		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.directObject: return False

		self.sendEventLater(self.parser.directObject)

		return True

	def check(self) -> bool:
		if self.parser.directObject == self.game.player:
			return self.fireResponse("direct-is-the-player")
		if self.parser.directObject.isSet("fixed"):
			return self.fireResponse("direct-is-fixed")
		if self.parser.directObject.isSet("heavy"):
			return self.fireResponse("direct-is-heavy")

		return True

	def carryOut(self) -> None:
		# Move the DO to player's inventory
		self.parser.directObject.container = self.game.player
		self.parser.directObject.set(["taken"])
		self.sendEventLater(self.parser.directObject)

	def report(self) -> None:
		self.fireResponse("direct-taken")

	def responses(self) -> typing.Tuple[str]:
		return ("direct-not-found", "direct-is-the-player", "direct-is-fixed",
					"direct-is-heavy", "direct-taken", )

class LeaveObject(dragonfly.Action):
	def init(self) -> bool:
		lst = self.game.player.childs(self.parser.directObjectString)
		if not lst: return self.fireResponse("direct-not-found")

		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.directObject: return False

		self.sendEventLater(self.parser.directObject)

		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		noun = self.parser.directObject
		noun.container = self.game.player.container
		noun.set(["leaved"])

		self.sendEventLater(noun)

	def report(self) -> None:
		self.fireResponse("direct-left")

	def responses(self) -> typing.Tuple[str]:
		return ("direct-not-found", "direct-left", )

class TakeFrom(dragonfly.Action):
	def init(self) -> bool:

		lst = self.game.player.childs(self.parser.indirectObjectString)
		lst.extend(self.game.player.container.childs(self.parser.indirectObjectString))

		if not lst: return self.fireResponse("indirect-not-found")

		self.parser.indirectObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.indirectObject: return False

		self.sendEventLater(self.parser.indirectObject)

		return True

	def check(self) -> bool:

		container = self.parser.indirectObject

		if not container.isSet("container"):
			return self.fireResponse("indirect-is-not-container")
		if container.isSet("closed"):
			return self.fireResponse("indirect-is-closed")

		lst = container.childs(self.parser.directObjectString)
		if not lst: return self.fireResponse("direct-not-found")

		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.directObject: return False

		# Send the before event now
		return self.parser.directObject.doBefore(self)

	def carryOut(self) -> None:
		# Move the noun to the player's inventory
		self.parser.directObject.container = self.game.player
		self.parser.directObject.set(["taken"])
		self.sendEventLater(self.parser.indirectObject)
		self.sendEventLater(self.parser.directObject)

	def report(self) -> None:
		self.fireResponse("direct-taken")

	def responses(self) -> typing.Tuple[str]:
		return ("indirect-not-found", "indirect-is-not-container", "indirect-is-closed",
					"direct-not-found", "direct-taken", )

class LeaveIn(dragonfly.Action):
	def init(self) -> bool:
		# The direct object in inventory (object)
		lst = self.game.player.childs(self.parser.directObjectString)
		if not lst: return self.fireResponse("direct-not-found")

		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.directObject: return False

		# The indirect object in the inventory or the current place (container)
		lst = self.game.player.childs(self.parser.indirectObjectString)
		lst.extend(self.game.player.container.childs(self.parser.indirectObjectString))
		if not lst: return self.fireResponse("indirect-not-found")

		self.parser.indirectObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.indirectObject: return False

		self.sendEventLater(self.parser.directObject)
		self.sendEventLater(self.parser.indirectObject)

		return True

	def check(self) -> bool:

		if self.parser.indirectObject == self.game.player:
			return self.fireResponse("indirect-is-the-player")
		if not self.parser.indirectObject.isSet("container"):
			return self.fireResponse("indirect-is-not-container")
		if self.parser.indirectObject.isSet("closed"):
			return self.fireResponse("indirect-is-closed")

		return True

	def carryOut(self) -> None:
		# Move the object to the container
		self.parser.directObject.container = self.parser.indirectObject
		self.parser.directObject.set(["leaved"])
		self.sendEventLater(self.parser.directObject)
		self.sendEventLater(self.parser.indirectObject)

	def report(self) -> None:
		self.fireResponse("direct-leaved")

	def responses(self) -> typing.Tuple[str]:
		return ("direct-not-found", "indirect-not-found", "indirect-is-the-player",
					"indirect-is-not-container", "indirect-is-closed", "direct-leaved", )

class PullObject(dragonfly.Action):
	def init(self) -> bool:

		lst = self.game.player.container.childs(self.parser.directObjectString)
		if not list: return self.fireResponse("direct-not-found")

		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.directObject: return False

		self.sendEventLater(self.parser.directObject)

		return True

	def check(self) -> bool:
		if self.parser.directObject == self.game.player:
			return self.fireResponse("direct-is-the-player")
		if self.parser.directObject.isSet("fixed"):
			return self.fireResponse("direct-is-fixed")
		return True

	def carryOut(self) -> None:
		self.sendEventLater(self.parser.directObject)

	def report(self) -> None:
		self.fireResponse("nothing-happens")

	def responses(self) -> typing.Tuple[str]:
		return ("direct-not-found", "direct-is-the-player", "direct-is-fixed", "nothing-happens", )

class PushObject(dragonfly.Action):
	def init(self) -> bool:

		lst = self.game.player.container.childs(self.parser.directObjectString)
		if not list: return self.fireResponse("direct-not-found")

		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.directObject: return False

		self.sendEventLater(self.parser.directObject)

		return True

	def check(self) -> bool:
		if self.parser.directObject == self.game.player:
			return self.fireResponse("direct-is-the-player")
		if self.parser.directObject.isSet("fixed"):
			return self.fireResponse("direct-is-fixed")
		return True

	def carryOut(self) -> None:
		self.sendEventLater(self.parser.directObject)

	def report(self) -> None:
		self.fireResponse("nothing-happens")

	def responses(self) -> typing.Tuple[str]:
		return ("direct-not-found", "direct-is-the-player", "direct-is-fixed",
						"nothing-happens", )

class OpenObject(dragonfly.Action):
	def init(self) -> bool:
		lst = self.game.player.childs(self.parser.directObjectString)
		lst.extend(self.game.player.container.childs(self.parser.directObjectString))

		if not lst: return self.fireResponse("direct-not-found")

		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)

		if not self.parser.directObject: return False

		self.sendEventLater(self.parser.directObject)

		return True

	def check(self) -> bool:

		if self.parser.directObject == self.game.player:
			return self.fireResponse("direct-is-the-player")
		if not self.parser.directObject.isSet("closable"):
			return self.fireResponse("direct-is-not-closable")
		if not self.parser.directObject.isSet("closed"):
			return self.fireResponse("direct-is-open")

		return True

	def carryOut(self) -> None:
		self.parser.directObject.unset(["closed"])
		self.sendEventLater(self.parser.directObject)

	def report(self) -> None:
		self.fireResponse("direct-was-opened")

	def responses(self) -> typing.Tuple[str]:
		return ("direct-not-found", "direct-is-the-player", "direct-is-not-closable",
					"direct-is-open", "direct-was-opened", )

class CloseObject(dragonfly.Action):
	def init(self) -> bool:
		lst = self.game.player.childs(self.parser.directObjectString)
		lst.extend(self.game.player.container.childs(self.parser.directObjectString))

		if not lst: return self.fireResponse("direct-not-found")

		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)

		if not self.parser.directObject: return False

		self.sendEventLater(self.parser.directObject)

		return True

	def check(self) -> bool:

		if self.parser.directObject == self.game.player:
			return self.fireResponse("direct-is-the-player")
		if not self.parser.directObject.isSet("closable"):
			return self.fireResponse("direct-is-not-closable")
		if self.parser.directObject.isSet("closed"):
			return self.fireResponse("direct-is-closed")

		return True

	def carryOut(self) -> None:
		self.parser.directObject.set(["closed"])
		self.sendEventLater(self.parser.directObject)

	def report(self) -> None:
		self.fireResponse("direct-was-closed")

	def responses(self) -> typing.Tuple[str]:
		return ("direct-not-found", "direct-is-the-player", "direct-is-not-closable",
						"direct-is-closed", "direct-was-closed", )

class OpenWith(dragonfly.Action):
	def init(self) -> bool:

		# Direct object in inventory or current place
		lst = self.game.player.childs(self.parser.directObjectString)
		lst.extend(self.game.player.container.childs(self.parser.directObjectString))

		if not lst: return self.fireResponse("direct-not-found")

		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.directObject: return False

		# Indirect object in inventory
		lst = self.game.player.childs(self.parser.indirectObjectString)

		if not lst: return self.fireResponse("indirect-not-found")

		self.parser.indirectObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.indirectObject: return False

		self.sendEventLater(self.parser.directObject)
		self.sendEventLater(self.parser.indirectObject)

		return True

	def check(self) -> bool:

		if self.parser.directObject == self.game.player:
			return self.fireResponse("direct-is-the-player")
		if self.parser.indirectObject == self.game.player:
			return self.fireResponse("indirect-is-the-player")

		if not self.parser.directObject.isSet("closable"):
			return self.fireResponse("direct-is-not-closable")

		if not self.parser.directObject.isSet("closed"):
			return self.fireResponse("direct-is-open")

		return True

	def carryOut(self) -> None:
		self.sendEventLater(self.parser.directObject)
		self.sendEventLater(self.parser.indirectObject)

	def report(self) -> None:
		self.fireResponse("nothing-happens")

	def responses(self) -> typing.Tuple[str]:
		return ("direct-not-found", "direct-is-the-player", "indirect-is-the-player",
					"direct-is-not-closable", "direct-is-open", "nothing-happens", )

class CloseWith(dragonfly.Action):
	def init(self) -> bool:

		# Direct object in inventory or current place
		lst = self.game.player.childs(self.parser.directObjectString)
		lst.extend(self.game.player.container.childs(self.parser.directObjectString))

		if not lst: return self.fireResponse("direct-not-found")

		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.directObject: return False

		# Indirect object in inventory
		lst = self.game.player.childs(self.parser.indirectObjectString)

		if not lst: return self.fireResponse("indirect-not-found")

		self.parser.indirectObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.indirectObject: return False

		self.sendEventLater(self.parser.directObject)
		self.sendEventLater(self.parser.indirectObject)

		return True

	def check(self) -> bool:

		if self.parser.directObject == self.game.player:
			return self.fireResponse("direct-is-the-player")
		if self.parser.indirectObject == self.game.player:
			return self.fireResponse("indirect-is-the-player")

		if not self.parser.directObject.isSet("closable"):
			return self.fireResponse("direct-is-not-closable")

		if self.parser.directObject.isSet("closed"):
			return self.fireResponse("direct-is-closed")

		return True

	def carryOut(self) -> None:
		self.sendEventLater(self.parser.directObject)
		self.sendEventLater(self.parser.indirectObject)

	def report(self) -> None:
		self.fireResponse("nothing-happens")

	def responses(self) -> typing.Tuple[str]:
		return ("direct-not-found", "indirect-not-found", "direct-is-the-player",
					"indirect-is-the-player", "direct-is-not-closable",
							"direct-is-closed", "nothing-happens", )

class GoTo(dragonfly.Action):

	def __init__(self) -> None:
		super().__init__()
		self.conn = None

	def init(self) -> bool:

		# Get exit from dictionary
		exit = self.dictionary.exit(self.parser.directObjectString)
		if not exit: return self.fireResponse("exit-not-exists")

		# Get connection from dictionary
		self.conn = self.game.player.container.connection(exit)
		if not self.conn: return self.fireResponse("exit-not-found")

		self.sendEventLater(self.game.player.container)

		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		# Get the destiny
		nouns = self.dictionary.nouns(self.conn.destiny)
		if not nouns:
			raise DragonflyException(f'Called GoTo action from "{self.game.player.container.name}": Destiny "{self.conn.destiny}" not found on exit "{self.conn.exit}"')

		# Move the player
		self.game.player.container = nouns[0]

		# Visibility behavior
		if self.game.getProperty("look-around") == "always":
			# Look around verb
			v = self.dictionary.verbByAction("LookAround")
			self.game.execute(v.name)
		
		self.sendEventLater(self.game.player.container)

	def report(self) -> None:
		pass
	
	def responses(self) -> typing.Tuple[str]:
		return ("exit-not-exists", "exit-not-found", )

class Talk(dragonfly.Action):
	def init(self) -> bool:
		self.place = self.game.player.container
		self.sendEventLater(self.place)

		return True
		
	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		self.fireResponse("player-says")

		self.sendEventLater(self.place)

	def report(self) -> None:
		pass

	def responses(self) -> typing.Tuple[str]:
		return ("player-says")

class TalkTo(dragonfly.Action):
	def init(self) -> bool:
		# Direct object in inventory or current place
		lst = self.game.player.childs(self.parser.directObjectString)
		lst.extend(self.game.player.container.childs(self.parser.directObjectString))

		if not lst: return self.fireResponse("direct-not-found")

		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.directObject: return False

		self.sendEventLater(self.parser.directObject)

		return True
	
	def check(self) -> bool:
		if self.parser.directObject == self.game.player:
			return self.fireResponse("direct-is-the-player")
		if not self.parser.directObject.isSet("speaker"):
			return self.fireResponse("direct-is-not-speaker")
		return True

	def carryOut(self) -> None:
		self.sendEventLater(self.parser.directObject)

	def report(self) -> None:
		self.fireResponse("nothing-happens")

	def responses(self) -> typing.Tuple[str]:
		return ("direct-not-found", "direct-is-the-player", "direct-is-not-speaker",
					"nothing-happens", )

class GiveTo(dragonfly.Action):
	def init(self) -> bool:

		# Direct Object in inventory
		lst = self.game.player.childs(self.parser.directObjectString)
		if not lst: return self.fireResponse("direct-not-found")
		self.parser.directObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.directObject: return False

		# Indirect Object in the place
		lst = self.game.player.container.childs(self.parser.indirectObjectString)
		if not lst: return self.fireResponse("indirect-not-found")
		self.parser.indirectObject = self.dictionary.objectChooserDialog.execute(lst)
		if not self.parser.indirectObject: return False

		self.sendEventLater(self.parser.directObject)
		self.sendEventLater(self.parser.indirectObject)

		return True

	def check(self) -> bool:
		if self.game.player == self.parser.indirectObject:
			return self.fireResponse("indirect-is-the-player")
		if not self.parser.indirectObject.isSet("interactive"):
			return self.fireResponse("indirect-is-not-interactive")
		return True

	def carryOut(self) -> None:
		# Move direct inner indirect
		self.parser.directObject.container = self.parser.indirectObject

		self.sendEventLater(self.parser.directObject)
		self.sendEventLater(self.parser.indirectObject)

	def report(self) -> None:
		self.fireResponse("given-to-indirect")

	def responses(self) -> typing.Tuple[str]:
		return ("direct-not-found", "indirect-not-found", "indirect-is-the-player",
				"indirect-is-not-interactive", "given-to-indirect")

class ReadObject(DefaultAction):
	pass

class SmokeObject(DefaultAction):
	pass

class TurnOnObject(DefaultAction):
	pass

class TurnOffObject(DefaultAction):
	pass

class HitObject(DefaultAction):
	pass

class TouchObject(DefaultAction):
	pass
