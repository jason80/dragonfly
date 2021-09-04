import typing
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QCheckBox, QDialog, QLineEdit, QListView, QPushButton, QWidget
from PyQt5 import uic

import action
import helper.forname
import nautilus.view.event_element_dialog
import responses

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

		self.lstResponses = QListView()
		self.btnAddResponse = QPushButton()
		self.btnEditResponse = QPushButton()
		self.btnRemoveResponse = QPushButton()

		self.btnSave = QPushButton()

		self.__cancel = True

		uic.loadUi("base/nautilus/view/event-dialog.ui", self)

		# Signals
		self.btnAddResponse.clicked.connect(self.addResponse)
		self.btnEditResponse.clicked.connect(self.editResponse)
		self.btnRemoveResponse.clicked.connect(self.removeResponse)

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

	def editResponse(self) -> None:
		index = self.lstResponses.currentIndex()
		if index.row() == -1: return

		response = self.__actionEvent.responses[index.row()]
		dialog = nautilus.view.event_element_dialog.EventElementDialog(self, 
							"Edit Response", response, responses)
		if dialog.cancel: return None

		self.__actionEvent.responses[index.row()] = dialog.element

		self.loadResponses()

	def removeResponse(self) -> None:
		index = self.lstResponses.currentIndex()
		if index.row() == -1: return

		self.__actionEvent.responses.pop(index.row())

		self.loadResponses()

	def save(self):
		self.__cancel = False

		# Actions
		actions = self.edtActions.text().split(",")
		self.__actionEvent.actions.clear()
		for a in actions:
			aClass = helper.forname.getClass(a.strip(), "actions")
			self.__actionEvent.actions.append(aClass)

		self.__actionEvent.cancel = self.chkCancel.isChecked()

		self.close()