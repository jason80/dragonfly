import typing

from PyQt5.QtXml import QDomDocument, QDomElement, QDomNode

import action
import dfbase
import helper.forname
import helper.text
import movement


class Entity():
	"""Base of the nouns, verbs and exits."""
	def __init__(self) -> None:
		self.__names = []
		self.__game = None
		self.__dictionary = None

	def __str__(self) -> str:
		return str(self.__names)

	@property
	def game(self) -> "dfbase.Game":
		return self.__game

	@game.setter
	def game(self, g: "dfbase.Game") -> None:
		self.__game = g
		self.__dictionary = g.dictionary

	@property
	def dictionary(self) -> "dfbase.Dictionary":
		return self.__dictionary

	@property
	def names(self) -> typing.List[str]:
		return self.__names

	@names.setter
	def names(self, n: typing.List[str]) -> None:
		self.__names = n

	@property
	def name(self) -> str:
		"""Gets the first name of the entity."""
		return self.__names[0] if self.__names else ""

	def responds(self, name: str) -> bool:
		"""Returns True if the entity responds to the name."""
		for n in self.__names:
			if helper.text.isEquals(n, name): return True
			#if n.lower() == name.lower(): return True

		return False

	def appendName(self, name: str) -> None:
		"""Add a new name at top of the list of names if it not responds to the name."""
		if not self.responds(name):
			self.__names.insert(0, name)

	def load(self, element: QDomElement) -> None:
		self.names.clear()
		for n in element.attribute("names").split(","):
			self.names.append(n.strip())

	def save(self, doc: QDomDocument, nodeName: str) -> QDomElement:
		element = doc.createElement(nodeName)
		element.setAttribute("names", ", ".join(self.__names))
		return element

class Noun(Entity):
	"""Nouns represents the objects of the game. Can be contained by other nouns.
		and has attributes and variables.
	"""
	def __init__(self, container: "Noun" = None) -> None:
		super().__init__()
		self.__container = container
		self.__attrs = set()
		self.__variables = dict()

		self.__before = []
		self.__after = []

		self.__connections = []

	def __str__(self) -> str:
		result = super().__str__()
		if self.__container != None:
			result += f" ({self.__container.name})"

		if self.__attrs:
			result += f" attrs: {', '.join(self.__attrs)}"
		
		return result

	@property
	def container(self) -> "Noun":
		"""Get the container Noun"""
		return self.__container

	@container.setter
	def container(self, cont: "Noun") -> None:
		"""Set the container noun. If the container is self, raise an exception."""
		if self == cont:
			raise Exception(f"Noun {self.name} cannot contain itself.")
		self.__container = cont

	def contains(self, name: str) -> bool:
		for n in self.dictionary.nouns():
			if n.container == self:
				if n.responds(name): return True

		return False

	def childs(self, name: str = "") -> typing.List["Noun"]:
		result = []
		for n in self.dictionary.nouns():
			if n.container == self:
				if not name:
					result.append(n)
				else:
					if n.responds(name):
						result.append(n)
		
		return result

	@property
	def attributes(self) -> typing.Set:
		return self.__attrs

	def set(self, values: typing.List[str]) -> None:
		"""Set a list of attributes"""
		self.__attrs.update(tuple(values))

	def isSet(self, value: str) -> bool:
		"""Check is setted an attribute."""
		return value in self.__attrs

	def unset(self, values: typing.List[str]) -> None:
		for v in values:
			self.__attrs.discard(v)

	@property
	def variables(self) -> typing.Dict:
		return self.__variables

	@property
	def beforeEvents(self) -> typing.List["action.ActionEvent"]:
		return self.__before
	
	@property
	def afterEvents(self) -> typing.List["action.ActionEvent"]:
		return self.__after

	def getVariable(self, name: str) -> str:
		return self.__variables[name]

	def setVariable(self, name: str, value: str) -> None:
		self.__variables[name] = value

	def addBefore(self, actionEvent: "action.ActionEvent") -> None:
		self.__before.append(actionEvent)

	def addAfter(self, actionEvent: "action.ActionEvent") -> None:
		self.__after.append(actionEvent)

	def __doEvent(self, action: "action.Action", eventList: typing.List["action.ActionEvent"]) -> bool:
		result = True
		for actionEvent in eventList:
			# If match action with list
			if actionEvent.match(action):
				# Check if actionevent's conditions return true
				if not actionEvent.checkConditions(action): continue
				
				# Execute responses
				actionEvent.execute(action)
				result = not actionEvent.cancel

		return result

	def doBefore(self, action: "action.Action") -> bool:
		return self.__doEvent(action, self.__before)

	def doAfter(self, action: "action.Action") -> bool:
		return self.__doEvent(action, self.__after)

	@property
	def the(self) -> str:

		result = ""
		for a in self.dictionary.articles():
			if a.female == self.isSet("female") and a.plural == self.isSet("plural") and not a.indefinited:
				result = a.name + " " + self.name

		return result

	@property
	def a(self) -> str:
		if self.isSet("countless"): return self.name

		result = ""
		for a in self.dictionary.articles():
			if a.female == self.isSet("female") and a.plural == self.isSet("plural") and a.indefinited:
				result = a.name + " " + self.name

		return result

	@property
	def article(self) -> str:
		return self.the if self.isSet("definited") else self.a

	@property
	def connections(self) -> typing.List[movement.Connection]:
		return self.__connections

	def addConnection(self, conn: movement.Connection) -> None:
		self.__connections.append(conn)

	def connection(self, exit: "Exit") -> movement.Connection:
		for c in self.__connections:
			if exit.responds(c.exit): return c
		return None

	def load(self, element: QDomElement):
		super().load(element)

		for i in range(element.childNodes().count()):
			node = element.childNodes().at(i)
			if node.nodeType() == QDomNode.ElementNode:
				child = node.toElement()

				# Sets
				if child.nodeName() == "set":
					for j in range(child.childNodes().count()):
						n = child.childNodes().at(j)
						if n.nodeType() == QDomNode.TextNode:
							sets = n.toText().data()
							for s in sets.split(","):
								self.set([s.strip()])

				# Variables
				if child.nodeName() == "variable":
					name = child.attribute("name")
					value = child.attribute("value")
					self.setVariable(name, value)

				# Childs
				if child.nodeName() == "noun":
					childNoun = Noun(container=self)
					childNoun.game = self.game
					childNoun.load(child)
					self.dictionary.addNoun(childNoun)

				# Events
				if child.nodeName() == "before":
					event = action.ActionEvent()
					event.load(child)
					self.addBefore(event)

				if child.nodeName() == "after":
					event = action.ActionEvent()
					event.load(child)
					self.addAfter(event)

				# Connections
				if child.nodeName() == "connection":
					conn = movement.Connection()
					conn.load(child)
					self.addConnection(conn)

	def save(self, doc: QDomDocument) -> QDomElement:
		# Save the entity base
		element = super().save(doc, "noun")

		# Attrs
		if self.__attrs:
			attrs =  ", ".join(self.__attrs)
			attrElement = doc.createElement("set")
			attrElement.appendChild(doc.createTextNode(attrs))
			element.appendChild(attrElement)

		# Variables
		for v in self.__variables:
			vElement = doc.createElement("variable")
			vElement.setAttribute("name", v)
			vElement.setAttribute("value", self.__variables[v])
			element.appendChild(vElement)

		# Childs
		for n in self.childs():
			element.appendChild(n.save(doc))

		# Events before
		for e in self.__before:
			element.appendChild(e.save(doc, "before"))

		# Events after
		for e in self.__after:
			element.appendChild(e.save(doc, "after"))

		# Connections
		for c in self.__connections:
			element.appendChild(c.save(doc))

		return element


class Verb(Entity):
	def __init__(self) -> None:
		super().__init__()

		self.__action = None
		self.__syntax = []

		self.__responses = {}

	def __str__(self) -> str:
		return f"{super().__str__()} ({self.__action})"

	@property
	def action(self) -> typing.Type["action.Action"]:
		"""Return the action associated with this verb."""
		return self.__action

	@action.setter
	def action(self, action: typing.Type["action.Action"]) -> None:
		"""Set the associated action"""
		self.__action = action

	@property
	def syntax(self) -> typing.List[str]:
		"""Return the verb's syntax."""
		return self.__syntax

	@syntax.setter
	def syntax(self, syntax: typing.List[str]) -> None:
		"""Set the verb's syntax."""
		self.__syntax = syntax

	@property
	def responses(self) -> typing.Dict:
		return self.__responses

	def getResponse(self, id: str) -> str:
		return self.__responses[id] if id in self.__responses else ""

	def setResponse(self, id: str, response: str) -> None:
		self.__responses[id] = response

	def hasResponse(self, id: str) -> bool:
		return id in self.__responses

	def load(self, element: QDomElement):
		super().load(element)

		# Verb base
		actionString = element.attribute("action")
		self.action = helper.forname.getClass(actionString, defaultModule = "actions")
		if element.attribute("syntax"):
			for member in element.attribute("syntax").split(","):
				self.syntax.append(member.strip())

		# Responses
		for i in range(element.childNodes().count()):
			node = element.childNodes().at(i)
			if node.nodeType() == QDomNode.ElementNode:
				child = node.toElement()
				if child.nodeName() == "response":
					self.setResponse(child.attribute("id"), child.attribute("string"))

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc, "verb")

		# Verb base
		element.setAttribute("action", self.__action.__name__)
		element.setAttribute("syntax", ", ".join(self.__syntax))

		# Responses
		for r in self.__responses:
			rElement = doc.createElement("response")
			rElement.setAttribute("id", r)
			rElement.setAttribute("string", self.__responses[r])
			element.appendChild(rElement)

		return element

class Article:
	def __init__(self) -> None:
		self.__name = ""
		self.__female = False
		self.__plural = False
		self.__indefinited = False

	def __str__(self) -> str:
		return f"{self.name} ({'female' if self.female else 'male'}, {'plural' if self.plural else 'singular'}{', indefinited)' if self.indefinited else ')'}"

	@property
	def name(self) -> str: return self.__name

	@property
	def female(self) -> bool: return self.__female

	@property
	def plural(self) -> bool: return self.__plural

	@property
	def indefinited(self) -> bool: return self.__indefinited

	def load(self, element: QDomElement) -> None:
		self.__name = element.attribute("name")
		self.__female = element.attribute("genre") == "female"
		self.__plural = element.attribute("number") == "plural"
		self.__indefinited = element.attribute("indefinited") == "true"

	def save(self, doc: QDomDocument) -> QDomElement:
		element = doc.createElement("article")
		element.setAttribute("name", self.__name)
		element.setAttribute("genre", "female" if self.__female else "male")
		element.setAttribute("number", "plural" if self.__plural else "singular")
		element.setAttribute("indefinited", "true" if self.__indefinited else "false")

		return element
		
class Exit(Entity):
	def __init__(self) -> None:
		super().__init__()

	def save(self, doc: QDomDocument) -> QDomElement:
		return super().save(doc, "exit")