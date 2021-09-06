import typing

import action
import entities
import movement
from nautilus.view.event_dialog import EventDialog
from PyQt5 import uic
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import (QComboBox, QInputDialog, QLineEdit, QListView,
                             QPushButton, QWidget)


class NounWidget(QWidget):
	def __init__(self, parent: typing.Optional['QWidget'], noun: "entities.Noun") -> None:
		super().__init__(parent=parent)

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
