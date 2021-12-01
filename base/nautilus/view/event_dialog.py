import typing
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QCheckBox, QDialog, QLineEdit, QListView, QMessageBox, QPushButton, QWidget
from PyQt5 import uic

import action, responses, conditions
import helper.forname
import nautilus.view.event_element_dialog

class EventDialog(QDialog):
	def __init__(self, parent: typing.Optional[QWidget], event: action.ActionEvent) -> None:
		super().__init__(parent=parent)

		self.__actionEvent = event

		self.edtActions = QLineEdit()
		self.chkCancel = QCheckBox()

		self.lstConditions = QListView()
		self.btnAddCondition = QPushButton()
		self.btnEditCondition = QPushButton()
		self.btnRemoveCondition = QPushButton()
		self.btnUpCondition = QPushButton()
		self.btnDownCondition = QPushButton()

		self.lstResponses = QListView()
		self.btnAddResponse = QPushButton()
		self.btnEditResponse = QPushButton()
		self.btnRemoveResponse = QPushButton()
		self.btnUpResponse = QPushButton()
		self.btnDownResponse = QPushButton()

		self.btnSave = QPushButton()

		self.__cancel = True

		uic.loadUi("base/nautilus/view/event-dialog.ui", self)

		# Signals
		self.btnAddResponse.clicked.connect(self.addResponse)
		self.btnEditResponse.clicked.connect(self.editResponse)
		self.btnRemoveResponse.clicked.connect(self.removeResponse)
		self.btnUpResponse.clicked.connect(self.upResponse)
		self.btnDownResponse.clicked.connect(self.downResponse)

		self.btnAddCondition.clicked.connect(self.addCondition)
		self.btnEditCondition.clicked.connect(self.editCondition)
		self.btnRemoveCondition.clicked.connect(self.removeCondition)
		self.btnUpCondition.clicked.connect(self.upCondition)
		self.btnDownCondition.clicked.connect(self.downCondition)

		self.btnSave.clicked.connect(self.save)

		# Load event
		# Actions
		actions = []
		for a in self.__actionEvent.actions:
			if a.__module__ != "actions":
				actions.append(f"{a.__module__}.{a.__name__}")
			else: actions.append(f"{a.__name__}")

		self.edtActions.setText(", ".join(actions))

		# Cancel
		self.chkCancel.setChecked(self.__actionEvent.cancel)

		# Responses
		self.responsesModel = QStringListModel()
		self.loadResponses()

		# Conditions
		self.conditionsModel = QStringListModel()
		self.loadConditions()

		self.exec()

	@property
	def cancel(self) -> bool:
		return self.__cancel

	@property
	def actionEvent(self) -> action.ActionEvent:
		return self.__actionEvent

	def loadResponses(self) -> None:

		if not self.__actionEvent: return None

		responseList = []
		for r in self.__actionEvent.responses:
			responseList.append(str(r))

		self.responsesModel = QStringListModel(responseList)
		self.lstResponses.setModel(self.responsesModel)

	def addResponse(self) -> None:
		dialog = nautilus.view.event_element_dialog.EventElementDialog(self, 
								"New Response", None, responses)
		if dialog.cancel: return None

		self.__actionEvent.addResponse(dialog.element)

		self.loadResponses()

		self.lstResponses.setCurrentIndex(self.responsesModel.index(len(self.__actionEvent.responses) - 1, 0))

	def editResponse(self) -> None:
		index = self.lstResponses.currentIndex()
		if index.row() == -1: return

		response = self.__actionEvent.responses[index.row()]
		dialog = nautilus.view.event_element_dialog.EventElementDialog(self, 
							"Edit Response", response, responses)
		if dialog.cancel: return None

		self.__actionEvent.responses[index.row()] = dialog.element

		sel = index.row()

		self.loadResponses()

		self.lstResponses.setCurrentIndex(self.responsesModel.index(sel, 0))

	def removeResponse(self) -> None:
		index = self.lstResponses.currentIndex()
		if index.row() == -1: return

		self.__actionEvent.responses.pop(index.row())

		self.loadResponses()

	def addCondition(self) -> None:
		dialog = nautilus.view.event_element_dialog.EventElementDialog(self, 
								"New Condition", None, conditions)
		if dialog.cancel: return None

		self.__actionEvent.addCondition(dialog.element)

		self.loadConditions()

		self.lstConditions.setCurrentIndex(self.conditionsModel.index(len(self.__actionEvent.conditions) - 1, 0))

	def loadConditions(self) -> None:
		if not self.__actionEvent: return None

		conditionList = []
		for r in self.__actionEvent.conditions:
			conditionList.append(str(r))

		self.conditionsModel = QStringListModel(conditionList)
		self.lstConditions.setModel(self.conditionsModel)

	def editCondition(self) -> None:
		index = self.lstConditions.currentIndex()
		if index.row() == -1: return

		condition = self.__actionEvent.conditions[index.row()]
		dialog = nautilus.view.event_element_dialog.EventElementDialog(self, 
							"Edit Condition", condition, conditions)
		if dialog.cancel: return None

		self.__actionEvent.conditions[index.row()] = dialog.element

		sel = index.row()

		self.loadConditions()

		self.lstConditions.setCurrentIndex(self.conditionsModel.index(sel, 0))

	def removeCondition(self) -> None:
		index = self.lstConditions.currentIndex()
		if index.row() == -1: return

		self.__actionEvent.conditions.pop(index.row())

		self.loadConditions()

	def upCondition(self):
		index = self.lstConditions.currentIndex()
		if index.row() < 1: return

		self.__actionEvent.conditions[index.row()], self.__actionEvent.conditions[index.row() - 1] = self.__actionEvent.conditions[index.row() - 1], self.__actionEvent.conditions[index.row()] 

		sel = index.row() - 1

		self.loadConditions()

		self.lstConditions.setCurrentIndex(self.conditionsModel.index(sel, 0))

	def downCondition(self):
		index = self.lstConditions.currentIndex()
		if index.row() == -1 or index.row() == len(self.__actionEvent.conditions) - 1: return

		self.__actionEvent.conditions[index.row()], self.__actionEvent.conditions[index.row() + 1] = self.__actionEvent.conditions[index.row() + 1], self.__actionEvent.conditions[index.row()] 

		sel = index.row() + 1

		self.loadConditions()

		self.lstConditions.setCurrentIndex(self.conditionsModel.index(sel, 0))

	def upResponse(self):
		index = self.lstResponses.currentIndex()
		if index.row() < 1: return

		self.__actionEvent.responses[index.row()], self.__actionEvent.responses[index.row() - 1] = self.__actionEvent.responses[index.row() - 1], self.__actionEvent.responses[index.row()] 

		sel = index.row() - 1

		self.loadResponses()

		self.lstResponses.setCurrentIndex(self.responsesModel.index(sel, 0))

	def downResponse(self):
		index = self.lstResponses.currentIndex()
		if index.row() == -1 or index.row() == len(self.__actionEvent.responses) - 1: return

		self.__actionEvent.responses[index.row()], self.__actionEvent.responses[index.row() + 1] = self.__actionEvent.responses[index.row() + 1], self.__actionEvent.responses[index.row()] 

		sel = index.row() + 1

		self.loadResponses()

		self.lstResponses.setCurrentIndex(self.responsesModel.index(sel, 0))

	def save(self) -> None:
		self.__cancel = False

		# Actions
		actions = self.edtActions.text().split(",")
		self.__actionEvent.actions.clear()
		for a in actions:
			aClass, error = helper.forname.getClass(a.strip(), "actions")
			if not aClass:
				QMessageBox.about(self, "Error", error)
				return None
			self.__actionEvent.actions.append(aClass)

		self.__actionEvent.cancel = self.chkCancel.isChecked()

		self.close()