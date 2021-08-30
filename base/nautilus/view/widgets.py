import typing
from PyQt5.QtWidgets import QComboBox, QLineEdit, QWidget
from PyQt5 import uic
import entities

class NounWidget(QWidget):
	def __init__(self, parent: typing.Optional['QWidget'], noun: "entities.Noun") -> None:
		super().__init__(parent=parent)

		self.noun = noun
		self.edtNames = QLineEdit()
		self.edtAttrs = QLineEdit()
		self.cbContainer = QComboBox()

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

		self.edtNames.setText(", ".join(self.noun.names))
		self.edtAttrs.setText(", ".join(self.noun.attributes))