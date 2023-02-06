import typing
import copy

import dragonfly

from PyQt5.QtXml import QDomElement, QDomNode

class Noun(dragonfly.Entity):
	"""Nouns represents the objects of the game. Can be contained by other nouns.
		and has attributes and variables.
	"""

	id_max = 0

	def __init__(self, container: "Noun" = None) -> None:
		super().__init__()
		self.__container = container
		self.__attrs = set()
		self.__variables = dict()

		self.__before = []
		self.__after = []

		self.__connections = []

		# Generate an id
		Noun.id_max += 1
		self.__id = Noun.id_max

	def __str__(self) -> str:
		result = super().__str__()
		if self.__container != None:
			result += f" ({self.__container.name})"

		if self.__attrs:
			result += f" attrs: {', '.join(self.__attrs)}"
		
		return result

	@property
	def id(self) -> int:
		return self.__id

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
		if name in self.__variables.keys():
			return self.__variables[name]

		return ""

	def setVariable(self, name: str, value: str) -> None:
		"""Set the value of the variable.

		Args:
			name (str): name of the variable.
			value (str): value of the variable.
		"""
		self.__variables[name] = value

	@property
	def beforeEvents(self) -> typing.List["dragonfly.ActionEvent"]:
		"""Return the list of the Before events.

		Returns:
			dragonfly.ActionEvent: Before ActionEvent list.
		"""
		return self.__before
	
	@property
	def afterEvents(self) -> typing.List["dragonfly.ActionEvent"]:
		"""Return the list of the After events.

		Returns:
			dragonfly.ActionEvent: After ActionEvent list.
		"""
		return self.__after

	def addBefore(self, actionEvent: "dragonfly.ActionEvent") -> None:
		"""Add a new Before action evento to the list.

		Args:
			actionEvent (dragonfly.ActionEvent): Before ActionEvent.
		"""
		self.__before.append(actionEvent)

	def addAfter(self, actionEvent: "dragonfly.ActionEvent") -> None:
		"""Add a new After action evento to the list.

		Args:
			actionEvent (dragonfly.ActionEvent): After ActionEvent.
		"""
		self.__after.append(actionEvent)

	def __doEvent(self, action: "dragonfly.Action", eventList: typing.List["dragonfly.ActionEvent"]) -> bool:
		"""Perform ActionEvent match with the Action, check if it meets the condition, and executes
		the event.

		eventList argument allows especify Before or After events.

		Args:
			action (dragonfly.Action): target Action.
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

	def doBefore(self, action: "dragonfly.Action") -> bool:
		"""Perform Before ActionEvent match with the Action, check if it meets the condition, and executes
		the event.

		Args:
			action (action.Action): target Action.

		Returns:
			bool: True if and only if the event has not cacelled.
		"""
		return self.__doEvent(action, self.__before)

	def doAfter(self, action: "dragonfly.Action") -> bool:
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

		# If is a propper noun:
		if self.isSet("propper"):
			result = self.name
		else:
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
	def connections(self) -> typing.List["dragonfly.Connection"]:
		"""Return the list of all connections of the noun.

		Returns:
			typing.List[dragonfly.Connection]: the list of the connections.
		"""
		return self.__connections

	def addConnection(self, conn: "dragonfly.Connection") -> None:
		"""Add a new connection to noun. If the exit exists, replace the destiny with the new instance.

		Args:
			conn (dragonfly.Connection): a new connection.
		"""

		exit = self.dictionary.exit(conn.exit)

		if not exit:
			raise dragonfly.DragonflyException(
				f'Adding connection: Exit "{conn.exit}" not found in dictionary.')

		for c in self.connections:
			if exit.responds(c.exit):
				c.destiny = conn.destiny
				return None

		self.__connections.append(conn)

	def connection(self, exit: "dragonfly.Exit") -> "dragonfly.Connection":
		"""Return a connection indicating the associated exit.

		Args:
			exit (Exit): The exit to match connection.

		Returns:
			dragonfly.Connection: the connection associated to exit. If not exists any connection
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
					event = dragonfly.ActionEvent()
					event.load(child)
					self.addBefore(event)

				if child.nodeName() == "after":
					event = dragonfly.ActionEvent()
					event.load(child)
					self.addAfter(event)

				# Connections
				if child.nodeName() == "connection":
					conn = dragonfly.Connection()
					conn.load(child)
					self.addConnection(conn)

				# Clones
				if child.nodeName() == "clone":
					instance = child.attribute("instance")
					lst = self.dictionary.nouns(instance)
					if not lst:
						raise dragonfly.DragonflyException(
							f'Noun target "{instance}" not found in dictionary.')
					cl = lst[0]

					cl.clone(self)
