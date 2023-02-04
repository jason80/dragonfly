import dfbase
import output.console
from enum import Enum

from PyQt5.QtXml import QDomElement, QDomNode

class ResultType(Enum):
	VICTORY = 0
	DEFEAT = 1

class GameOver:
	def __init__(self, dict: "dfbase.Dictionary") -> None:
		self.__dictionary = dict
		self.__gameOverMessage = "Game over"
		self.__gameOverStyle = ""
		self.__victoryMessage = "with VICTORY !"
		self.__victoryStyle = ""
		self.__defeatMessage = "with defeat"
		self.__defeatStyle = ""

	def run(self, result: ResultType, message: str) -> None:
		output.console.Console.println(self.__gameOverMessage, self.__gameOverStyle)
		if result == ResultType.VICTORY:
			output.console.Console.println(self.__victoryMessage, self.__victoryStyle)
		else:
			output.console.Console.println(self.__defeatMessage, self.__defeatStyle)
		output.console.Console.println(message)

	def load(self, element: QDomElement) -> None:
		for i in range(element.childNodes().count()):
			child = element.childNodes().at(i)
			if (child.nodeType() == QDomNode.ElementNode):
				if (child.nodeName() == "game-over-message"):
					self.__gameOverMessage, self.__gameOverStyle = \
					self.loadMessage(child)
				if (child.nodeName() == "victory-message"):
					self.__victoryMessage, self.__victoryStyle = \
					self.loadMessage(child)
				if (child.nodeName() == "defeat-message"):
					self.__defeatMessage, self.__defeatStyle = \
					self.loadMessage(child)

	def loadMessage(self, element: QDomElement):
		style = element.attribute("style")
		for i in range(element.childNodes().count()):
			child = element.childNodes().at(i)
			if (child.nodeType == QDomNode.TextNode):
				return child.toText().data().strip(), style
		return style, ""
