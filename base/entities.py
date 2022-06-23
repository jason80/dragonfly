import typing
import copy

from PyQt5.QtXml import QDomDocument, QDomElement, QDomNode
from dfexcept import DragonflyException

import action
import dfbase
import helper.forname
import helper.text
import movement


class Entity():
	"""Base of the nouns, verbs and exits.
	Contains the multi-name property, and game and dictionary instances."""
	def __init__(self) -> None:
		self.__names = []
		self.__game = None
		self.__dictionary = None

	def __str__(self) -> str:
		return str(self.__names)

	@property
	def game(self) -> "dfbase.Game":
		"""Return the game instance.
		"""
		return self.__game

	@game.setter
	def game(self, g: "dfbase.Game") -> None:
		"""Set the game instance."""
		self.__game = g
		self.__dictionary = g.dictionary

	@property
	def dictionary(self) -> "dfbase.Dictionary":
		"""Return the dictionary instance.
		"""
		return self.__dictionary

	@property
	def names(self) -> typing.List[str]:
		"""Return the complete name list.
		"""
		return self.__names

	@names.setter
	def names(self, n: typing.List[str]) -> None:
		"""Set the complete name list.
		"""
		self.__names = n

	@property
	def name(self) -> str:
		"""Return the first name of the entity."""
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
		"""Load the entity from xml element.
		"""
		self.names.clear()
		for n in element.attribute("names").split(","):
			self.names.append(n.strip())

	def save(self, doc: QDomDocument, nodeName: str) -> QDomElement:
		"""Save entity to xml element.

		Args:
			doc (QDomDocument): xml document.
			nodeName (str): the tag name.

		Returns:
			QDomElement: element with entity data.
		"""
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
		"""Check if this noun contains a noun.

		Args:
			name (str): the name of the child.

		Returns:
			bool: True if and only if this contains the child.
		"""
		for n in self.dictionary.nouns():
			if n.container == self:
				if n.responds(name): return True

		return False

	def childs(self, name: str = "") -> typing.List["Noun"]:
		"""Return a list with chils wich responds to name.
		If the name = "", return all childs.
		"""
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
		"""Return a set with all attributes of the noun.
		"""
		return self.__attrs

	def set(self, values: typing.List[str]) -> None:
		"""Set a list of attributes."""
		self.__attrs.update(tuple(values))

	def isSet(self, value: str) -> bool:
		"""Check if an attribute is setted."""
		return value in self.__attrs

	def unset(self, values: typing.List[str]) -> None:
		"""Unset a list of attributes."""
		for v in values:
			self.__attrs.discard(v)

	@property
	def variables(self) -> typing.Dict:
		"""Return a dictionary with all variables of the noun.
		"""
		return self.__variables

	def getVariable(self, name: str) -> str:
		"""Return the value of the variable.
		Args:
			name (str): name of the variable.

		Returns:
			str: the value of the variable.
		"""
		return self.__variables[name]

	def setVariable(self, name: str, value: str) -> None:
		"""Set the value of the variable.

		Args:
			name (str): name of the variable.
			value (str): value of the variable.
		"""
		self.__variables[name] = value

	@property
	def beforeEvents(self) -> typing.List["action.ActionEvent"]:
		"""Return the list of the Before events.

		Returns:
			actions.ActionEvent: Before ActionEvent list.
		"""
		return self.__before
	
	@property
	def afterEvents(self) -> typing.List["action.ActionEvent"]:
		"""Return the list of the After events.

		Returns:
			actions.ActionEvent: After ActionEvent list.
		"""
		return self.__after

	def addBefore(self, actionEvent: "action.ActionEvent") -> None:
		"""Add a new Before action evento to the list.

		Args:
			actionEvent (action.ActionEvent): Before ActionEvent.
		"""
		self.__before.append(actionEvent)

	def addAfter(self, actionEvent: "action.ActionEvent") -> None:
		"""Add a new After action evento to the list.

		Args:
			actionEvent (action.ActionEvent): After ActionEvent.
		"""
		self.__after.append(actionEvent)

	def __doEvent(self, action: "action.Action", eventList: typing.List["action.ActionEvent"]) -> bool:
		"""Perform ActionEvent match with the Action, check if it meets the condition, and executes
		the event.

		eventList argument allows especify Before or After events.

		Args:
			action (action.Action): target Action.
			eventList (typing.List[action.ActionEvent]): list of the events.

		Returns:
			bool: True if and only if the event has not cacelled.
		"""
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
		"""Perform Before ActionEvent match with the Action, check if it meets the condition, and executes
		the event.

		Args:
			action (action.Action): target Action.

		Returns:
			bool: True if and only if the event has not cacelled.
		"""
		return self.__doEvent(action, self.__before)

	def doAfter(self, action: "action.Action") -> bool:
		"""Perform After ActionEvent match with the Action, check if it meets the condition, and executes
		the event.

		Args:
			action (action.Action): target Action.

		Returns:
			bool: True if and only if the event has not cacelled.
		"""
		return self.__doEvent(action, self.__after)

	@property
	def the(self) -> str:
		"""Construct the first name of the noun adding the definited article depending the
		genre and the number of self.

		Returns:
			str: The name with the article.
		"""
		result = ""
		for a in self.dictionary.articles():
			if a.female == self.isSet("female") and a.plural == self.isSet("plural") and not a.indefinited:
				result = a.name + " " + self.name

		return result

	@property
	def a(self) -> str:
		"""Construct the first name of the noun adding the indefinited article depending the
		genre and the number of self. If the noun is countless, return only the first name.

		Returns:
			str: The name with the article.
		"""

		if self.isSet("countless"): return self.name

		result = ""
		for a in self.dictionary.articles():
			if a.female == self.isSet("female") and a.plural == self.isSet("plural") and a.indefinited:
				result = a.name + " " + self.name

		return result

	@property
	def article(self) -> str:
		"""Return the definited article if the noun is definited, for otherwise return the
		indefinited article.

		Returns:
			str: the article depending the noun.
		"""
		return self.the if self.isSet("definited") else self.a

	@property
	def connections(self) -> typing.List[movement.Connection]:
		"""Return the list of all connections of the noun.

		Returns:
			typing.List[movement.Connection]: the list of the connections.
		"""
		return self.__connections

	def addConnection(self, conn: movement.Connection) -> None:
		"""Add a new connection to noun. If the exit exists, replace the destiny with the new instance.

		Args:
			conn (movement.Connection): a new connection.
		"""

		exit = self.dictionary.exit(conn.exit)

		for c in self.connections:
			if exit.responds(c.exit):
				c.destiny = conn.destiny
				return None

		self.__connections.append(conn)

	def connection(self, exit: "Exit") -> movement.Connection:
		"""Return a connection indicating the associated exit.

		Args:
			exit (Exit): The exit to match connection.

		Returns:
			movement.Connection: the connection associated to exit. If not exists any connection
							with the exit, return None.
		"""
		for c in self.__connections:
			if exit.responds(c.exit): return c
		return None

	def clone(self, container: "Noun") -> None:
		"""Clone the object on dictionary inner especified container.

		Utilice clone to add generic objects like floor, walls and roof.

		Args:
			container (Noun): Destiny for cloned instance.
		"""
		noun = copy.copy(self)
		noun.names = self.names
		noun.game = self.game
		noun.container = container

		self.dictionary.addNoun(noun)

		noun.set(self.attributes)

		for k in self.variables:
			noun.setVariable(self.getVariable(k))

		for n in self.childs():
			n.clone(noun)

	def load(self, element: QDomElement):
		"""Load the noun from xml element.

		Args:
			element (QDomElement): xml elememt.
		"""
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

				# Clones
				if child.nodeName() == "clone":
					lst = self.dictionary.nouns(child.attribute("instance"))
					if not lst:
						pass # TODO: error
					cl = lst[0]

					cl.clone(self)

	def save(self, doc: QDomDocument) -> QDomElement:
		"""Save the noun to xml element.

		Args:
			doc (QDomDocument): The xml document.

		Returns:
			QDomElement: The generated xml element.
		"""
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
	"""Represents the multi-name command wich is associated to Action.
	"""
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
		"""Return a dictionary with the responses of the verb.

		Returns:
			typing.Dict: responses of the verb.
		"""
		return self.__responses

	def getResponse(self, id: str) -> str:
		"""Return the response indicating the if of self. The responses are quieried by the
		action associated.

		Args:
			id (str): the response's id.

		Returns:
			str: the response.
		"""
		return self.__responses[id] if id in self.__responses else ""

	def setResponse(self, id: str, response: str) -> None:
		"""Set a response to the verb.

		Args:
			id (str): the id of the response.
			response (str): the response text.
		"""
		self.__responses[id] = response

	def hasResponse(self, id: str) -> bool:
		"""Check if response exists.

		Args:
			id (str): the id of the response.

		Returns:
			bool: True if and only if the verb contains the response.
		"""
		return id in self.__responses

	def load(self, element: QDomElement):
		"""Load verb from xml element.

		Args:
			element (QDomElement): the xml element.
		"""
		super().load(element)

		# Verb base
		actionString = element.attribute("action")
		self.action, error = helper.forname.getClass(actionString, defaultModule = "actions")
		if not self.action:
			raise DragonflyException(error)
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
		"""Save the verb to xml element.

		Args:
			doc (QDomDocument): the xml document.

		Returns:
			QDomElement: the xml element containing the verb.
		"""
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
	"""Female-Plural representation of the nouns. Can be definited of indefinited
	"""
	def __init__(self) -> None:
		self.__name = ""
		self.__female = False
		self.__plural = False
		self.__indefinited = False

	def __str__(self) -> str:
		return f"{self.name} ({'female' if self.female else 'male'}, {'plural' if self.plural else 'singular'}{', indefinited)' if self.indefinited else ')'}"

	@property
	def name(self) -> str:
		"""Name of the article.
		"""
		return self.__name

	@name.setter
	def name(self, name: str) -> None: self.__name = name

	@property
	def female(self) -> bool:
		"""Return True if the article is female.
		"""
		return self.__female

	@female.setter
	def female(self, female: bool) -> None: self.__female = female

	@property
	def plural(self) -> bool:
		"""Return True if the article is plural.
		"""
		return self.__plural

	@plural.setter
	def plural(self, plural: bool) -> None: self.__plural = plural

	@property
	def indefinited(self) -> bool:
		"""Return True if the article is indefinited.
		"""
		return self.__indefinited

	@indefinited.setter
	def indefinited(self, indefinited: bool) -> None: self.__indefinited = indefinited

	def load(self, element: QDomElement) -> None:
		"""Load the article from xml element.

		Args:
			element (QDomElement): the xml element
		"""
		self.__name = element.attribute("name")
		self.__female = element.attribute("genre") == "female"
		self.__plural = element.attribute("number") == "plural"
		self.__indefinited = element.attribute("indefinited") == "true"

	def save(self, doc: QDomDocument) -> QDomElement:
		"""Save the article to xml element.

		Args:
			doc (QDomDocument): the xml document.

		Returns:
			QDomElement: a new xml element with the article.
		"""
		element = doc.createElement("article")
		element.setAttribute("name", self.__name)
		element.setAttribute("genre", "female" if self.__female else "male")
		element.setAttribute("number", "plural" if self.__plural else "singular")
		element.setAttribute("indefinited", "true" if self.__indefinited else "false")

		return element
		
class Exit(Entity):
	"""Represents a possible point where the player can go.
	"""
	def __init__(self) -> None:
		super().__init__()

	def save(self, doc: QDomDocument) -> QDomElement:
		"""Save the exit to xml element.

		Args:
			doc (QDomDocument): xml document.

		Returns:
			QDomElement: xml element containing the exit.
		"""
		return super().save(doc, "exit")