import typing
from PyQt5.QtWidgets import QCheckBox, QDialog, QLineEdit, QListView, QPushButton, QWidget
from PyQt5 import uic

import action
import helper.forname

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

		self.exec()

	@property
	def cancel(self) -> bool:
		return self.__cancel

	@property
	def actionEvent(self) -> action.ActionEvent:
		return self.__actionEvent

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