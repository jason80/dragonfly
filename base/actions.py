import action
from dfexcept import DragonflyException
from output.console import Console

class SingleAction(action.Action):
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

class DefaultAction(action.Action):
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

class UnknownVerb(action.Action):
	def init(self) -> bool:
		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		self.fireResponse("unknown-verb")

	def report(self) -> None:
		pass

class Quit(action.Action):
	def init(self) -> bool:
		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		self.game.close()

	def report(self) -> None:
		pass

class Inventory(action.Action):
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

class ExamineObject(action.Action):
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

class LookAround(action.Action):
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
		for n in self.place.childs():
			if n == self.game.player: continue
			if n.isSet("scene"): continue
			nouns.append(n)

		if nouns: self.dictionary.seeListDialog.execute(nouns)

class LookInside(action.Action):
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

class TakeObject(action.Action):
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

class TakeFrom(action.Action):
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
		self.parser.directObject.doBefore(self)

		return True

	def carryOut(self) -> None:
		# Move the noun to the player's inventory
		self.parser.directObject.container = self.game.player
		self.parser.directObject.set(["taken"])
		self.sendEventLater(self.parser.indirectObject)
		self.sendEventLater(self.parser.directObject)

	def report(self) -> None:
		self.fireResponse("direct-taken")

class LeaveIn(action.Action):
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

class PullObject(action.Action):
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

class PushObject(action.Action):
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

class OpenObject(action.Action):
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

class OpenObject(action.Action):

	def __init__(self) -> None:
		super().__init__()

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

	def carryOut(self):
		self.parser.directObject.unset(["closed"])
		self.sendEventLater(self.parser.directObject)

	def report(self):
		self.fireResponse("direct-was-openned")


class CloseObject(action.Action):
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

class OpenWith(action.Action):
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

class CloseWith(action.Action):
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

class GoTo(action.Action):

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

class LeaveObject(action.Action):
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
