from PyQt5.QtXml import QDomDocument, QDomElement, QDomNode

import dragonfly
from dragonfly.output import Console
from dragonfly import Help
from dragonfly import DragonflyException
from gameover import ResultType

class Message(dragonfly.ActionResponse):

	def __init__(self) -> None:
		self.message = ""
		self.style = ""
		self.newLine = True

	def __str__(self) -> str:
		result = "println" if self.newLine else "print"
		return f'{result} "{self.message}"'

	def execute(self, action: "dragonfly.Action") -> None:
		if self.newLine: Console.println(self.message, self.style)
		else: Console.print(self.message, self.style)

	def load(self, element: QDomElement) -> None:

		self.style = element.attribute("style")
		nl = element.attribute("new-line", defaultValue = "true")
		if nl == "true": self.newLine = True
		elif nl == "false": self.newLine = False
		else:
			# Error
			pass

		for i in range(element.childNodes().count()):
			node = element.childNodes().at(i)
			if node.nodeType() == QDomNode.TextNode:
				self.message = node.toText().data().strip()

class Attr(dragonfly.ActionResponse):
	def __init__(self) -> None:
		self.instance = ""
		self.set = ""
		self.unset = ""

	def __str__(self) -> str:
		lst = []
		if self.set:
			lst.append(f'set "{self.set}"')
		if self.unset:
			lst.append(f'unset "{self.set}"')

		return " & ".join(lst) + " to " + self.instance

	def execute(self, action: "dragonfly.Action") -> None:
		objList = action.dictionary.nouns(self.instance)
		if not objList:
			raise DragonflyException(f'On Set response: noun "{self.instance}" not found in dictionary.')

		obj = objList[0]

		sets = []
		for s in self.set.split(","):
			sets.append(s.strip())

		unsets = []
		for u in self.unset.split(","):
			unsets.append(u.strip())

		obj.set(sets)
		obj.unset(unsets)

	def load(self, element: QDomElement) -> None:
		self.instance = element.attribute("instance")
		self.set = element.attribute("set", defaultValue="")
		self.unset = element.attribute("unset", defaultValue="")

class Variable(dragonfly.ActionResponse):
	def __init__(self) -> None:
		self.instance = ""
		self.variable = ""
		self.set = ""

	def __str__(self) -> str:
		return f'Set "{self.set}" to variable "{self.variable}", instance: "{self.instance}".'

	def execute(self, action: "dragonfly.Action") -> None:
		obj = action.dictionary.nouns(self.instance)
		if not obj:
			raise DragonflyException(f'On Variable response: noun "{self.instance}" not found in dictionary.')

		obj = obj[0]

		obj.setVariable(self.variable, self.set)

	def load(self, element: QDomElement) -> None:
		self.instance = element.attribute("instance")
		self.variable = element.attribute("variable")
		self.set = element.attribute("set")

class AppendName(dragonfly.ActionResponse):
	def __init__(self) -> None:
		self.instance = ""
		self.name = ""

	def __str__(self) -> str:
		return f'Append name "{self.name}" to "{self.instance}"'

	def execute(self, action: "dragonfly.Action") -> None:
		objList = action.dictionary.nouns(self.instance)
		if not objList:
			raise DragonflyException(f'On AppendName response: noun "{self.instance}" not found in dictionary.')
		
		obj = objList[0]
		obj.appendName(self.name)

	def load(self, element: QDomElement) -> None:
		self.instance = element.attribute("instance", defaultValue="")
		self.name = element.attribute("name", defaultValue="")

class Move(dragonfly.ActionResponse):
	def __init__(self) -> None:
		self.instance = ""
		self.destiny = ""

	def __str__(self) -> str:
		return f'Move "{self.instance}" to "{self.destiny}"'

	def getObj(self, action: "dragonfly.Action", name: str) -> "dragonfly.Noun":
		objList = action.dictionary.nouns(name)
		if not objList: return None
		return objList[0]

	def execute(self, action: "dragonfly.Action") -> None:
		obj = self.getObj(action, self.instance)
		if not obj: raise DragonflyException(f'On Move response: noun "{self.instance}" not found in dictionary.')

		dest = self.getObj(action, self.destiny)
		if not dest: raise DragonflyException(f'On Move response: destiny "{self.destiny}" not found in dictionary.')

		obj.container = dest

	def load(self, element: QDomElement) -> None:
		self.instance = element.attribute("instance", defaultValue="")
		self.destiny = element.attribute("destiny", defaultValue="")

class Tip(dragonfly.ActionResponse):
	def __init__(self) -> None:
		self.message = ""

	def __str__(self) -> str:
		return f'Show tip "{self.message}"'

	def execute(self, action: "dragonfly.Action") -> None:
		Help.tip(self.message)
		pass

	def load(self, element: QDomElement) -> None:
		for i in range(element.childNodes().count()):
			node = element.childNodes().at(i)
			if node.nodeType() == QDomNode.TextNode:
				self.message = node.toText().data().strip()

class TipOnce(dragonfly.ActionResponse):
	def __init__(self) -> None:
		self.message = ""
		self.instance = ""

	def __str__(self) -> str:
		return f'Show tip "{self.message} once"'

	def execute(self, action: "dragonfly.Action") -> None:
		objList = action.dictionary.nouns(self.instance)
		if not objList: return None
		Help.tipOnce(objList[0], self.message)

	def load(self, element: QDomElement) -> None:
		self.instance = element.attribute("instance", defaultValue="")
		for i in range(element.childNodes().count()):
			node = element.childNodes().at(i)
			if node.nodeType() == QDomNode.TextNode:
				self.message = node.toText().data().strip()

class Execute(dragonfly.ActionResponse):
	def __init__(self) -> None:
		self.sentence = ""

	def __str__(self) -> str:
		return f'Execute "{self.sentence}" sentence'

	def execute(self, action: "dragonfly.Action") -> None:
		action.game.execute(self.sentence)

	def load(self, element: QDomElement) -> None:
		for i in range(element.childNodes().count()):
			node = element.childNodes().at(i)
			if node.nodeType() == QDomNode.TextNode:
				self.sentence = node.toText().data().strip()

class AddConnection(dragonfly.ActionResponse):
	def __init__(self) -> None:
		self.instance = ""
		self.exit = ""
		self.destiny = ""

	def __str__(self) -> str:
		return f'Add connection to {self.instance}: {self.exit} -> {self.destiny}'

	def execute(self, action: "dragonfly.Action") -> None:
		objList = action.dictionary.nouns(self.instance)
		if not objList: raise DragonflyException(f'On AddConnection response: noun "{self.instance}" not found in dictionary.')

		conn = dragonfly.Connection()
		conn.exit = self.exit
		conn.destiny = self.destiny
		objList[0].addConnection(conn)

	def load(self, element: QDomElement) -> None:
		self.instance = element.attribute("instance", defaultValue="")
		self.exit = element.attribute("exit", defaultValue="")
		self.destiny = element.attribute("destiny", defaultValue="")

class ShowTitle(dragonfly.ActionResponse):
	def __str__(self) -> str:
		return "Show game title"

	def execute(self, action: "dragonfly.Action") -> None:
		action.game.showTitle()

	def load(self, element: QDomElement) -> None:
		pass
		
class RunConversation(dragonfly.ActionResponse):
	def __init__(self) -> None:
		self.owner = ""
		
	def __str__(self) -> str:
		return f"Run Conversation with '{self.owner}'"

	def execute(self, action: dragonfly.Action) -> None:
		c = action.dictionary.conversation(self.owner)
		c.start(action)

	def load(self, element: QDomElement) -> None:
		self.owner = element.attribute("owner")

class Pause(dragonfly.ActionResponse):

	def __str__(self) -> str:
		return "Pause"

	def execute(self, action: dragonfly.Action) -> None:
		action.game.pause()

	def load(self, element: QDomElement) -> None:
		pass

class Clear(dragonfly.ActionResponse):
	def __str__(self) -> str:
		return "Clear"

	def execute(self, action: dragonfly.Action) -> None:
		Console.clear()

	def load(self, element: QDomElement) -> None:
		pass

class EndGame(dragonfly.ActionResponse):
	def __init__(self) -> None:
		self.result = ""
		self.message = ""

	def __str__(self) -> str:
		return "End game"

	def execute(self, action: dragonfly.Action) -> None:
		victory = True
		if (self.result == "victory"): victory = True
		elif (self.result == "defeat"): victory = False
		else: raise DragonflyException(f'On EndGame: expected "victory" or "defeat" value on result attr.')

		action.dictionary.gameOver.run(ResultType.VICTORY if victory else ResultType.DEFEAT, self.message)

	def load(self, element: QDomElement) -> None:
		self.result = element.attribute("result")

		for i in range(element.childNodes().count()):
			node = element.childNodes().at(i)
			if node.nodeType() == QDomNode.TextNode:
				self.message = node.toText().data().strip()
