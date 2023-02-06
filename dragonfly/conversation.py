import typing
import dragonfly
import dragonfly.helper

from PyQt5.QtXml import QDomElement, QDomNode

class Topics:
	def __init__(self) -> None:
		self.__match = []
		self.__conditions = []
		self.__responses = []

	@property
	def conditions(self) -> typing.List[dragonfly.Condition]:
		return self.__conditions

	@property
	def responses(self) -> typing.List[dragonfly.ActionResponse]:
		return self.__responses

	def addCondition(self, cond: dragonfly.Condition) -> None:
		self.__conditions.append(cond)

	def addResponse(self, response: dragonfly.ActionResponse) -> None:
		self.__responses.append(response)

	def match(self, params: str) -> bool:
		# TODO: improve match
		pList = params.lower().split(" ")

		for t in self.__match:
			if t.strip().lower() in pList:
				return True

		return False

	def load(self, element: QDomElement) -> None:
		self.__match = element.attribute("match").split(",")

		for i in range(element.childNodes().count()):
			node = element.childNodes().at(i)

			# simple text found: create a message response:
			if node.nodeType() == QDomNode.TextNode:
				text = node.toText().data().strip()
				if not text: continue

				messageClass, error = dragonfly.helper.getClass("Message", defaultModule="responses")
				if not messageClass:
					raise dragonfly.DragonflyException(error)
				
				message = messageClass()
				message.message = text
				self.__responses.append(message)

			if node.nodeType() == QDomNode.ElementNode:
				child = node.toElement()
				# Load condition
				if child.nodeName() == "if":
					condClass, error = dragonfly.helper.getClass(child.attribute("class"), defaultModule="conditions")
					if not condClass:
						raise dragonfly.DragonflyException(error)
					cond = condClass()
					cond.load(child)
					self.__conditions.append(cond)

				# Load responses
				if child.nodeName() == "response":
					responseClass, error = dragonfly.helper.getClass(child.attribute("class"), defaultModule="responses")
					if not responseClass:
						raise dragonfly.DragonflyException(error)
					response = responseClass()
					response.load(child)
					self.__responses.append(response)

class Conversation:
	def __init__(self) -> None:
		self.__owner = ""
		self.__topicsList = []
		self.__default = None

	@property
	def owner(self) -> str:
		return self.__owner

	@owner.setter
	def owner(self, owner: str) -> None:
		self.__owner = owner

	@property
	def topicsList(self) -> typing.List[Topics]:
		return self.__topicsList

	@property
	def default(self) -> Topics:
		return self.__default
		
	def start(self, action: dragonfly.Action) -> None:
		for t in self.topicsList:
			if t.match(action.parser.parameters):
				if self.topicsMatch(action, t): return

		# Run default
		if self.__default:
			for r in self.__default.responses:
				r.execute(action)

	def topicsMatch(self, action: dragonfly.Action, topics: Topics) -> bool:
		# Check conditions
		for c in topics.conditions:
			if not c.check(action): return False

		# Execute responses
		for r in topics.responses:
			r.execute(action)

		return True

	def load(self, element: QDomElement) -> None:
		self.owner = element.attribute("owner")

		for i in range(element.childNodes().count()):
			node = element.childNodes().at(i)
			if node.nodeType() == QDomNode.ElementNode:
				child = node.toElement()
				if child.nodeName() == "topics":
					topics = Topics()
					topics.load(child)
					self.__topicsList.append(topics)
				if child.nodeName() == "default":
					topics = Topics()
					topics.load(child)
					self.__default = topics
