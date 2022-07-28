from PyQt5.QtXml import QDomDocument, QDomElement, QDomNode

import dragonfly
from dragonfly.output import Console
from dragonfly import Help
from dragonfly import DragonflyException

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

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("style", self.style)
		element.setAttribute("new-line", "true" if self.newLine else "false")

		element.appendChild(doc.createTextNode(self.message))

		return element

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

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)

		element.setAttribute("instance", self.instance)
		if self.set: element.setAttribute("set", self.set)
		if self.unset: element.setAttribute("unset", self.unset)

		return element

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

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("instance", self.instance)
		element.setAttribute("name", self.name)

		return element

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

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("instance", self.instance)
		element.setAttribute("destiny", self.destiny)
		
		return element

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

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.appendChild(doc.createTextNode(self.message))
		
		return element

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

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("instance", self.instance)
		element.appendChild(doc.createTextNode(self.message))
		
		return element

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

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.appendChild(doc.createTextNode(self.sentence))

		return element

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

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("instance", self.instance)
		element.setAttribute("exit", self.exit)
		element.setAttribute("destiny", self.destiny)
		
		return element

class ShowTitle(dragonfly.ActionResponse):
	def __str__(self) -> str:
		return "Show game title"

	def execute(self, action: "dragonfly.Action") -> None:
		action.game.showTitle()

	def load(self, element: QDomElement) -> None:
		pass

	def save(self, doc: QDomDocument) -> QDomElement:
		return super().save()
		
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

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("owner")
		return element
