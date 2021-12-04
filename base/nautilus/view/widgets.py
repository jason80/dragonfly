import typing

import action
import entities
import movement
import nautilus.app
import helper.forname
from nautilus.view.event_dialog import EventDialog
from PyQt5 import uic
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import (QComboBox, QInputDialog, QLineEdit, QListView, QMessageBox,
                             QPushButton, QWidget)


class NounWidget(QWidget):
	def __init__(self, parent: typing.Optional['QWidget'], nautilus: "nautilus.app.Nautilus", noun: "entities.Noun") -> None:
		super().__init__(parent=parent)

		self.nautilus = nautilus
		self.noun = noun
		self.edtNames = QLineEdit()
		self.edtAttrs = QLineEdit()
		self.cbContainer = QComboBox()

		self.btnRemoveNoun = QPushButton()

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
		self.btnUpBefore = QPushButton()
		self.btnDownBefore = QPushButton()
		self.lstAfter = QListView()
		self.btnAddAfter = QPushButton()
		self.btnEditAfter = QPushButton()
		self.btnRemoveAfter = QPushButton()
		self.btnUpAfter = QPushButton()
		self.btnDownAfter = QPushButton()

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

		self.btnRemoveNoun.clicked.connect(self.removeNoun)

		self.btnAddVariable.clicked.connect(self.addVariable)
		self.btnEditVariable.clicked.connect(self.editVariable)
		self.btnRemoveVariable.clicked.connect(self.removeVariable)

		self.btnAddBefore.clicked.connect(self.addBefore)
		self.btnEditBefore.clicked.connect(self.editBefore)
		self.btnRemoveBefore.clicked.connect(self.removeBefore)
		self.btnUpBefore.clicked.connect(self.upBefore)
		self.btnDownBefore.clicked.connect(self.downBefore)

		self.btnAddAfter.clicked.connect(self.addAfter)
		self.btnEditAfter.clicked.connect(self.editAfter)
		self.btnRemoveAfter.clicked.connect(self.removeAfter)
		self.btnUpAfter.clicked.connect(self.upAfter)
		self.btnDownAfter.clicked.connect(self.downAfter)

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

		# Get index
		key = var[0].strip()
		i = 0
		for k in self.noun.variables.keys():
			if k == key: break
			i += 1

		self.loadVariables()

		index = self.variablesModel.index(i, 0)
		self.lstVariables.setCurrentIndex(index)

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

		# Get index
		key = var[0].strip()
		i = 0
		for k in self.noun.variables.keys():
			if k == key: break
			i += 1

		self.loadVariables()
		
		index = self.variablesModel.index(i, 0)
		self.lstVariables.setCurrentIndex(index)

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

		# Select the new item
		self.lstBefore.setCurrentIndex(self.beforeModel.index(len(self.noun.beforeEvents) - 1, 0))

	def editBefore(self) -> None:
		index = self.lstBefore.currentIndex()
		if index.row() == -1: return

		event = self.noun.beforeEvents[index.row()]

		dialog = EventDialog(self, event)
		
		if dialog.cancel: return

		i = index.row()

		self.loadBefore()

		# Select the edited item
		index = self.beforeModel.index(i, 0)
		self.lstBefore.setCurrentIndex(index)

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

		# Select the new item
		self.lstAfter.setCurrentIndex(self.afterModel.index(len(self.noun.afterEvents) - 1, 0))

	def editAfter(self) -> None:
		index = self.lstAfter.currentIndex()
		if index.row() == -1: return

		event = self.noun.afterEvents[index.row()]

		dialog = EventDialog(self, event)
		
		if dialog.cancel: return

		i = index.row()

		self.loadAfter()

		# Select the edited item
		index = self.afterModel.index(i, 0)
		self.lstAfter.setCurrentIndex(index)

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

		self.lstConnections.setCurrentIndex(self.connModel.index(len(self.noun.connections) - 1, 0))

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

		i = index.row()

		self.loadConnections()

		# Select the edited item
		index = self.connModel.index(i, 0)
		self.lstConnections.setCurrentIndex(index)

	def removeConnection(self):
		index = self.lstConnections.currentIndex()
		if index.row() == -1: return

		self.noun.connections.pop(index.row())

		self.loadConnections()

	def upBefore(self) -> None:
		index = self.lstBefore.currentIndex()
		if index.row() < 1: return

		sel = index.row() - 1

		self.noun.beforeEvents[index.row()], self.noun.beforeEvents[index.row() - 1] = self.noun.beforeEvents[index.row() - 1], self.noun.beforeEvents[index.row()]
		self.loadBefore()

		self.lstBefore.setCurrentIndex(self.beforeModel.index(sel, 0))

	def downBefore(self) -> None:
		index = self.lstBefore.currentIndex()
		if index.row() == -1 or index.row() == len(self.noun.beforeEvents) - 1: return

		sel = index.row() + 1

		self.noun.beforeEvents[index.row()], self.noun.beforeEvents[index.row() + 1] = self.noun.beforeEvents[index.row() + 1], self.noun.beforeEvents[index.row()]
		self.loadBefore()

		self.lstBefore.setCurrentIndex(self.beforeModel.index(sel, 0))

	def upAfter(self) -> None:
		index = self.lstAfter.currentIndex()
		if index.row() < 1: return

		sel = index.row() - 1

		self.noun.afterEvents[index.row()], self.noun.afterEvents[index.row() - 1] = self.noun.afterEvents[index.row() - 1], self.noun.afterEvents[index.row()]
		self.loadAfter()

		self.lstAfter.setCurrentIndex(self.afterModel.index(sel, 0))

	def downAfter(self) -> None:
		index = self.lstAfter.currentIndex()
		if index.row() == -1 or index.row() == len(self.noun.afterEvents) - 1: return

		sel = index.row() + 1

		self.noun.afterEvents[index.row()], self.noun.afterEvents[index.row() + 1] = self.noun.afterEvents[index.row() + 1], self.noun.afterEvents[index.row()]
		self.loadAfter()

		self.lstAfter.setCurrentIndex(self.afterModel.index(sel, 0))

	def removeNoun(self) -> None:

		qm = QMessageBox()
		ret = qm.question(self, 'Nautilus', 'Remove noun and his childs ?', qm.Yes | qm.No)

		if ret == qm.No: return

		dict = self.nautilus.project.dictionary
		dict.cascadeRemoveNoun(self.noun)

		self.nautilus.mainWindow.workWidget.close()
		self.nautilus.mainWindow.displayNouns()

class VerbWidget(QWidget):
	def __init__(self, parent: typing.Optional['QWidget'], nautilus: "nautilus.app.Nautilus", verb: "entities.Verb") -> None:
		super().__init__(parent=parent)

		self.nautilus = nautilus
		self.verb = verb

		self.edtNames = QLineEdit()
		self.edtAction = QLineEdit()
		self.edtSyntax = QLineEdit()

		self.lstResponses = QListView()
		#self.btnAddResponse = QPushButton()
		self.btnEditResponse = QPushButton()
		#self.btnRemoveResponse = QPushButton()

		self.btnRemoveVerb = QPushButton()

		uic.loadUi("base/nautilus/view/verb-widget.ui", self)

		self.edtNames.setText(", ".join(verb.names))
		self.edtSyntax.setText(", ".join(verb.syntax))
		if verb.action:
			self.edtAction.setText(verb.action.__name__)

		# Signals
		self.edtNames.editingFinished.connect(self.namesEdited)
		self.edtSyntax.editingFinished.connect(self.syntaxEdited)
		self.edtAction.editingFinished.connect(self.actionEdited)

		#self.btnAddResponse.clicked.connect(self.addResponse)
		self.btnEditResponse.clicked.connect(self.editResponse)
		#self.btnRemoveResponse.clicked.connect(self.removeResponse)

		self.btnRemoveVerb.clicked.connect(self.removeVerb)

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
		self.verb.action, error = helper.forname.getClass(strAction, "actions")
		if not self.verb.action:
			QMessageBox.about(self, "Error", error)

		self.loadResponses()

	def loadResponses(self) -> None:
		#keys = self.verb.responses.keys()

		responses = []

		if self.verb.action:
			actionInst = self.verb.action()
			keys = actionInst.responses()
			for k in keys:
				responses.append(f"{k}={self.verb.getResponse(k)}")

		self.responsesModel = QStringListModel(responses)
		self.lstResponses.setModel(self.responsesModel)

	"""
	def addResponse(self):
		text, ok = QInputDialog.getText(self, "Add Response", "response=text")
		if not ok: return

		res = text.split("=")
		if len(res) != 2: return

		self.verb.setResponse(res[0].strip(), res[1].strip())

		self.loadResponses()
	"""

	def editResponse(self):
		index = self.lstResponses.currentIndex()
		if index.row() == -1: return

		removeKey = index.data().split("=")[0]

		text, ok = QInputDialog.getText(self, "Edit Response", "response=text",
					text=index.data())
		if not ok: return

		res = text.split("=")
		if len(res) != 2: return

		if removeKey in self.verb.responses:
			self.verb.responses.pop(removeKey)

		self.verb.setResponse(res[0].strip(), res[1].strip())

		self.loadResponses()

	"""
	def removeResponse(self):
		index = self.lstResponses.currentIndex()
		if index.row() == -1: return

		removeKey = index.data().split("=")[0]
		self.verb.responses.pop(removeKey)
		self.loadResponses()
	"""

	def removeVerb(self) -> None:
		qm = QMessageBox()
		ret = qm.question(self, 'Nautilus', 'Remove verb ?', qm.Yes | qm.No)

		if ret == qm.No: return

		dict = self.nautilus.project.dictionary
		dict.verbs().remove(self.verb)

		self.nautilus.mainWindow.workWidget.close()
		self.nautilus.mainWindow.displayVerbs()

class ExitWidget(QWidget):
	def __init__(self, parent: typing.Optional['QWidget'], nautilus: "nautilus.app.Nautilus", exit: "entities.Exit") -> None:
		super().__init__(parent=parent)

		self.nautilus = nautilus
		self.exit = exit

		self.edtNames = QLineEdit()

		uic.loadUi("base/nautilus/view/exit-widget.ui", self)

		self.edtNames.setText(", ".join(exit.names))

		# Signals
		self.edtNames.editingFinished.connect(self.namesEdited)

	def namesEdited(self):
		strNames = self.edtNames.text().strip()
		if not strNames: return

		self.exit.names.clear()

		for n in strNames.split(","):
			self.exit.names.append(n.strip())
