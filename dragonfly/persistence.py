from abc import ABC, abstractmethod
from xml.dom.minidom import Element
from PyQt5.QtXml import QDomDocument, QDomElement, QDomNode
from PyQt5.QtCore import QFile, QTextStream, QIODevice
import dragonfly
from dragonfly.movement import Connection

class PersistenceSystem(ABC):
	@abstractmethod
	def save(self, file: str, dict: "dragonfly.Dictionary") -> bool: pass

	@abstractmethod
	def load(self, file: str, dict: "dragonfly.Dictionary") -> bool: pass

class XMLPersistenceSystem(PersistenceSystem):
	def save(self, filename: str, dict: "dragonfly.Dictionary") -> bool:
		doc = QDomDocument()
		p_inst = doc.createProcessingInstruction("xml", 'version="1.0" encoding="UTF-8"')
		doc.appendChild(p_inst)

		root = doc.createElement("dragonfly-persistence")
		doc.appendChild(root)

		for n in dict.nouns():
			root.appendChild(self.saveNoun(doc, n))

		file = QFile(filename)

		if not file.open(QFile.WriteOnly or QFile.Truncate):
			print(f'Persistence: Cannot write file: "{filename}."')
			return False

		outstream = QTextStream(file)
		doc.save(outstream, 4)
		outstream.flush()
		file.close()

		return True

	def saveNoun(self, doc: QDomDocument, noun: "dragonfly.Noun") -> QDomElement:
		element = doc.createElement("noun")
		element.setAttribute("id", str(noun.id))
		element.setAttribute("names", ", ".join(noun.names))
		if noun.container:
			element.setAttribute("container", noun.container.id)
		else:
			element.setAttribute("container", "0")

		# Attributes
		setElement = doc.createElement("set")
		setElement.appendChild(doc.createTextNode(", ".join(noun.attributes)))
		element.appendChild(setElement)

		# Variables
		for k in noun.variables.keys():
			varElement = doc.createElement("variable")
			varElement.setAttribute("name", k)
			varElement.setAttribute("value", noun.variables[k])
			element.appendChild(varElement)

		# Connections
		for c in noun.connections:
			connElement = doc.createElement("connection")
			connElement.setAttribute("exit", c.exit)
			connElement.setAttribute("destiny", c.destiny)
			element.appendChild(connElement)

		return element

	def load(self, filename: str, dict: "dragonfly.Dictionary") -> bool:
		doc = QDomDocument()

		file = QFile(filename)
		if not file.open(QIODevice.ReadOnly or QIODevice.Text):
			print(f'Persistence: Cannot load file: "{filename}".')
			return False

		if not doc.setContent(file):
			print(f'Persistence: Cannot load file content: "{filename}".')
			file.close()
			return False

		file.close()

		root = doc.firstChildElement()

		for i in range(root.childNodes().count()):
			node = root.childNodes().at(i)
			if node.nodeType() == QDomNode.ElementNode:
				element = node.toElement()

				if element.nodeName() == "noun":
					if not self.loadNoun(dict, element):
						print(f'Persistence: Error loading "{filename}".')
						return False

		return True

	def loadNoun(self, dict: "dragonfly.Dictionary", element: QDomElement) -> bool:
		id = 0
		try:
			id = int(element.attribute("id"))
		except:
			return False

		noun = dict.nounByID(id)
		if not noun: return False

		# Clear all
		noun.attributes.clear()
		noun.variables.clear()
		noun.connections.clear()

		contID = 0
		try:
			contID = int(element.attribute("container"))
		except:
			return False

		if contID: noun.container = dict.nounByID(contID)

		noun.names = [n.strip() for n in element.attribute("names").split(",")]

		for i in range(element.childNodes().count()):
			node = element.childNodes().at(i)
			if node.nodeType() == QDomNode.ElementNode:
				child = node.toElement()

				if child.nodeName() == "set":
					for j in range(child.childNodes().count()):
						n = child.childNodes().at(j)
						if n.nodeType() == QDomNode.TextNode:
							sets = n.toText().data()
							noun.set([s.strip() for s in sets.split(",")])
							
				if child.nodeName() == "variable":
					noun.setVariable(child.attribute("name"),
							child.attribute("value"))

				if child.nodeName() == "connection":
					conn = Connection()
					conn.exit = child.attribute("exit")
					conn.destiny = child.attribute("destiny")
					noun.addConnection(conn)
		return True

class Persistence:
	def __init__(self, file: str, system: PersistenceSystem = XMLPersistenceSystem()) -> None:
		self.__file = file
		self.__system = system

	def saveGame(self, dict: "dragonfly.Dictionary") -> bool:
		return self.__system.save(self.__file, dict)

	def loadGame(self, dict: "dragonfly.Dictionary") -> bool:
		return self.__system.load(self.__file, dict)
