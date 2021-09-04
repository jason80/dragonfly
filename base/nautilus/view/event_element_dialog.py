import typing
from PyQt5.QtWidgets import QCheckBox, QComboBox, QDialog, QFormLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5 import uic

import helper.reflect
import helper.forname

class EventElementDialog(QDialog):
	def __init__(self, parent: typing.Optional[QWidget], element: typing.Any, module) -> None:
		super().__init__(parent=parent)
		self.__element = element
		self.__module = module

		self.__cancel = True

		self.cbElementType = QComboBox()
		self.formLayout = QFormLayout()
		self.btnSave = QPushButton()

		self.attrsComponents = []

		uic.loadUi("base/nautilus/view/event-element-dialog.ui", self)

		# Signals
		self.cbElementType.currentIndexChanged.connect(self.typeChanged)
		self.btnSave.clicked.connect(self.save)

		# Load classes
		for c in helper.reflect.getClasses(module):
			self.cbElementType.addItem(c.__name__)

		self.loadAttributes()
		
		self.exec()

	@property
	def cancel(self) -> bool:
		return self.__cancel

	@property
	def element(self) -> typing.Any:
		return self.__element

	def typeChanged(self):
		self.__element = None
		self.loadAttributes()

	def loadAttributes(self):

		# Clean form layout
		while self.formLayout.rowCount():
			self.formLayout.removeRow(0)

		# Clean component list
		self.attrsComponents.clear()

		if not self.__element:
			self.__element = helper.forname.getClass(self.cbElementType.currentText(), self.__module.__name__)()
		
		index = 0
		for k in self.__element.__dict__.keys():
			value = self.__element.__dict__[k]
			label = QLabel(self)
			label.setText(k)
			self.formLayout.setWidget(index, QFormLayout.LabelRole, label)

			if type(value) == str:
				line = QLineEdit(self)
				line.setText(value)
				self.formLayout.setWidget(index, QFormLayout.FieldRole, line)
				self.attrsComponents.append(line)
			if type(value) == bool:
				chk = QCheckBox(self)
				chk.setChecked(value)
				self.formLayout.setWidget(index, QFormLayout.FieldRole, chk)
				self.attrsComponents.append(chk)

			index += 1

	def save(self):

		keys = list(self.__element.__dict__.keys())

		for i in range(len(keys)):
			key = keys[i]

			component = self.attrsComponents[i]
			if type(component) == QLineEdit:
				self.__element.__dict__[key] = component.text().strip()
			if type(component) == QCheckBox:
				self.__element.__dict__[key] = component.isChecked()

		self.__cancel = False

		self.close()