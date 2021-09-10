import typing

import action
import entities
import movement
import nautilus.app
import helper.forname
from nautilus.view.event_dialog import EventDialog
from PyQt5 import uic
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import (QComboBox, QInputDialog, QLineEdit, QListView,
                             QPushButton, QWidget)


class NounWidget(QWidget):
	def __init__(self, parent: typing.Optional['QWidget'], nautilus: "nautilus.app.Nautilus", noun: "entities.Noun") -> None:
		super().__init__(parent=parent)

		self.nautilus = nautilus
		self.noun = noun
		self.edtNames = QLineEdit()
		self.edtAttrs = QLineEdit()
		self.cbContainer = QComboBox()

		# Variables
		self.lstVariables = QListView()
		self.btnAddVariable = QPushButton()
		self.btnEditVariable = QPushButton()
		self.btnRemoveVariable = QPushButton()

		# Events
		self.lstBefore = QListView()
		self.btnAddBefore = QPushButton()
		self.btnEditBefore = QPushButton()
		self.btnRemoveBefore = QPushButton()
		self.lstAfter = QListView()
		self.btnAddAfter = QPushButton()
		self.btnEditAfter = QPushButton()
		self.btnRemoveAfter = QPushButton()

		# Connections
		self.lstConnections = QListView()
		self.btnAddConnection = QPushButton()
		self.btnEditConnection = QPushButton()
		self.btnRemoveConnection = QPushButton()

		# List of containers
		self.containerList = [None]
		for n in noun.dictionary.nouns():
			if n == noun: continue
			self.containerList.append(n)

		uic.loadUi("base/nautilus/view/noun-widget.ui", self)

		# Load combo with containers
		self.cbContainer.addItem("[None]")
		for n in self.containerList:
			if n: self.cbContainer.addItem(n.name)

		# Select the container
		for i in range(len(self.containerList)):
			if self.containerList[i] == noun.container:
				self.cbContainer.setCurrentIndex(i)
				break

		# List of variables
		self.variablesModel = QStringListModel()
		self.loadVariables()

		# List of events
		self.beforeModel = QStringListModel()
		self.loadBefore()

		self.afterModel = QStringListModel()
		self.loadAfter()

		# List of connections
		self.connModel = QStringListModel()
		self.loadConnections()

		self.edtNames.setText(", ".join(self.noun.names))
		self.edtAttrs.setText(", ".join(self.noun.attributes))

		# Signals

		self.edtNames.editingFinished.connect(self.namesEdited)
		self.edtAttrs.editingFinished.connect(self.attrsEdited)

		self.btnAddVariable.clicked.connect(self.addVariable)
		self.btnEditVariable.clicked.connect(self.editVariable)
		self.btnRemoveVariable.clicked.connect(self.removeVariable)

		self.btnAddBefore.clicked.connect(self.addBefore)
		self.btnEditBefore.clicked.connect(self.editBefore)
		self.btnRemoveBefore.clicked.connect(self.removeBefore)

		self.btnAddAfter.clicked.connect(self.addAfter)
		self.btnEditAfter.clicked.connect(self.editAfter)
		self.btnRemoveAfter.clicked.connect(self.removeAfter)

		self.btnAddConnection.clicked.connect(self.addConnection)
		self.btnEditConnection.clicked.connect(self.editConnection)
		self.btnRemoveConnection.clicked.connect(self.removeConnection)

		self.cbContainer.currentIndexChanged.connect(self.containerChanged)

	def namesEdited(self) -> None:
		strNames = self.edtNames.text().strip()
		if not strNames: return

		self.noun.names.clear()

		for n in strNames.split(","):
			self.noun.names.append(n.strip())

	def attrsEdited(self) -> None:
		strAttrs = self.edtAttrs.text().strip()
		if not strAttrs: return

		self.noun.attributes.clear()

		for a in strAttrs.split(","):
			self.noun.set([a.strip()])

	def containerChanged(self):
		self.noun.container = self.containerList[self.cbContainer.currentIndex()]
		self.nautilus.mainWindow.displayNouns()

	def loadVariables(self) -> None:

		keys = self.noun.variables.keys()
		variables = []
		for k in keys:
			variables.append(f"{k}={self.noun.getVariable(k)}")

		self.variablesModel = QStringListModel(variables)
		self.lstVariables.setModel(self.variablesModel)

	def addVariable(self) -> None:
		text, ok = QInputDialog.getText(self, "Add Variable", "variable=value")
		if not ok: return

		var = text.split("=")
		if len(var) != 2: return

		self.noun.setVariable(var[0].strip(), var[1].strip())

		self.loadVariables()

	def editVariable(self) -> None:
		index = self.lstVariables.currentIndex()
		if index.row() == -1: return

		removeKey = index.data().split("=")[0]

		text, ok = QInputDialog.getText(self, "Edit Variable", "variable=value",
					text=index.data())
		if not ok: return

		var = text.split("=")
		if len(var) != 2: return

		self.noun.variables.pop(removeKey)

		self.noun.setVariable(var[0].strip(), var[1].strip())

		self.loadVariables()

	def removeVariable(self):
		index = self.lstVariables.currentIndex()
		if index.row() == -1: return

		removeKey = index.data().split("=")[0]
		self.noun.variables.pop(removeKey)
		self.loadVariables()

	def loadBefore(self):
		beforeList = []
		for b in self.noun.beforeEvents:
			beforeList.append(str(b))
		self.beforeModel = QStringListModel(beforeList)
		self.lstBefore.setModel(self.beforeModel)

	def addBefore(self) -> None:
		event = action.ActionEvent()
		dialog = EventDialog(self, event)

		if dialog.cancel: return

		event = dialog.actionEvent
		self.noun.addBefore(event)

		self.loadBefore()

	def editBefore(self) -> None:
		index = self.lstBefore.currentIndex()
		if index.row() == -1: return

		event = self.noun.beforeEvents[index.row()]

		dialog = EventDialog(self, event)
		
		if dialog.cancel: return

		self.loadBefore()

	def removeBefore(self) -> None:
		index = self.lstBefore.currentIndex()
		if index.row() == -1: return

		event = self.noun.beforeEvents.pop(index.row())

		self.loadBefore()

	def loadAfter(self) -> None:
		afterList = []
		for a in self.noun.afterEvents:
			afterList.append(str(a))
		self.afterModel = QStringListModel(afterList)
		self.lstAfter.setModel(self.afterModel)

	def addAfter(self) -> None:
		event = action.ActionEvent()
		dialog = EventDialog(self, event)

		if dialog.cancel: return

		event = dialog.actionEvent
		self.noun.addAfter(event)

		self.loadAfter()

	def editAfter(self) -> None:
		index = self.lstAfter.currentIndex()
		if index.row() == -1: return

		event = self.noun.afterEvents[index.row()]

		dialog = EventDialog(self, event)
		
		if dialog.cancel: return

		self.loadAfter()

	def removeAfter(self) -> None:
		index = self.lstAfter.currentIndex()
		if index.row() == -1: return

		event = self.noun.afterEvents.pop(index.row())

		self.loadAfter()

	def loadConnections(self) -> None:
		connList = []
		for c in self.noun.connections:
			connList.append(str(c))

		self.connModel = QStringListModel(connList)
		self.lstConnections.setModel(self.connModel)

	def addConnection(self) -> None:
		text, ok = QInputDialog.getText(self, "Add Connection", "exit=destiny")
		if not ok: return

		conn = text.split("=")
		if len(conn) != 2: return

		connection = movement.Connection()
		connection.exit = conn[0].strip()
		connection.destiny = conn[1].strip()

		self.noun.addConnection(connection)

		self.loadConnections()

	def editConnection(self) -> None:
		index = self.lstConnections.currentIndex()
		if index.row() == -1: return

		connection = self.noun.connections[index.row()]

		text, ok = QInputDialog.getText(self, "Edit Connection", "exit=destiny",
					text=f"{connection.exit}={connection.destiny}")
		if not ok: return

		conn = text.split("=")
		if len(conn) != 2: return

		connection.exit = conn[0].strip()
		connection.destiny = conn[1].strip()

		self.loadConnections()

	def removeConnection(self):
		index = self.lstConnections.currentIndex()
		if index.row() == -1: return

		self.noun.connections.pop(index.row())

		self.loadConnections()

class VerbWidget(QWidget):
	def __init__(self, parent: typing.Optional['QWidget'], nautilus: "nautilus.app.Nautilus", verb: "entities.Verb") -> None:
		super().__init__(parent=parent)

		self.nautilus = nautilus
		self.verb = verb

		self.edtNames = QLineEdit()
		self.edtAction = QLineEdit()
		self.edtSyntax = QLineEdit()

		self.lstResponses = QListView()
		self.btnAddResponse = QPushButton()
		self.btnEditResponse = QPushButton()
		self.btnRemoveResponse = QPushButton()

		uic.loadUi("base/nautilus/view/verb-widget.ui", self)

		self.edtNames.setText(", ".join(verb.names))
		self.edtSyntax.setText(", ".join(verb.syntax))
		if verb.action:
			self.edtAction.setText(verb.action.__name__)

		# Signals
		self.edtNames.editingFinished.connect(self.namesEdited)
		self.edtSyntax.editingFinished.connect(self.syntaxEdited)
		self.edtAction.editingFinished.connect(self.actionEdited)

		self.btnAddResponse.clicked.connect(self.addResponse)
		self.btnEditResponse.clicked.connect(self.editResponse)
		self.btnRemoveResponse.clicked.connect(self.removeResponse)

		self.responsesModel = QStringListModel()
		self.loadResponses()

	def namesEdited(self):
		strNames = self.edtNames.text().strip()
		if not strNames: return

		self.verb.names.clear()

		for n in strNames.split(","):
			self.verb.names.append(n.strip())
	
	def syntaxEdited(self):
		strSyntax = self.edtSyntax.text().strip()
		if not strSyntax: return

		self.verb.syntax.clear()

		for n in strSyntax.split(","):
			self.verb.syntax.append(n.strip())

	def actionEdited(self):
		strAction = self.edtAction.text().strip()
		self.verb.action = helper.forname.getClass(strAction, "actions")

	def loadResponses(self) -> None:
		keys = self.verb.responses.keys()
		responses = []
		for k in keys:
			responses.append(f"{k}={self.verb.getResponse(k)}")

		self.responsesModel = QStringListModel(responses)
		self.lstResponses.setModel(self.responsesModel)

	def addResponse(self):
		text, ok = QInputDialog.getText(self, "Add Response", "response=text")
		if not ok: return

		res = text.split("=")
		if len(res) != 2: return

		self.verb.setResponse(res[0].strip(), res[1].strip())

		self.loadResponses()

	def editResponse(self):
		index = self.lstResponses.currentIndex()
		if index.row() == -1: return

		removeKey = index.data().split("=")[0]

		text, ok = QInputDialog.getText(self, "Edit Response", "response=text",
					text=index.data())
		if not ok: return

		res = text.split("=")
		if len(res) != 2: return

		self.verb.responses.pop(removeKey)

		self.verb.setResponse(res[0].strip(), res[1].strip())

		self.loadResponses()

	def removeResponse(self):
		index = self.lstResponses.currentIndex()
		if index.row() == -1: return

		removeKey = index.data().split("=")[0]
		self.verb.responses.pop(removeKey)
		self.loadResponses()