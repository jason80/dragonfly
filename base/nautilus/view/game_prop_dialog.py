import typing
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QComboBox, QDialog, QInputDialog, QLineEdit, QListView, QPushButton, QWidget
from PyQt5 import uic

import nautilus.app

class GamePropDialog(QDialog):
	def __init__(self, parent: typing.Optional[QWidget], nautilus: "nautilus.app.Nautilus") -> None:
		super().__init__(parent=parent)

		self.nautilus = nautilus
		self.__cancel = True

		self.edtTitle = QLineEdit()
		self.edtAuthor = QLineEdit()
		self.lstProperties = QListView()
		self.btnAddProp = QPushButton()
		self.btnEditProp = QPushButton()
		self.btnRemoveProp = QPushButton()

		self.edtDefMaleSing = QLineEdit()
		self.edtDefFemaleSing = QLineEdit()
		self.edtDefMalePlural = QLineEdit()
		self.edtDefFemalePlural = QLineEdit()

		self.edtIndefMaleSing = QLineEdit()
		self.edtIndefFemaleSing = QLineEdit()
		self.edtIndefMalePlural = QLineEdit()
		self.edtIndefFemalePlural = QLineEdit()

		self.cbPlayer = QComboBox()

		self.btnSave = QPushButton()

		uic.loadUi("base/nautilus/view/game-prop-dialog.ui", self)

		self.btnAddProp.clicked.connect(self.addProp)
		self.btnEditProp.clicked.connect(self.editProp)
		self.btnRemoveProp.clicked.connect(self.removeProp)

		self.btnSave.clicked.connect(self.savePressed)

		self.edtTitle.setText(self.nautilus.project.title)
		self.edtAuthor.setText(self.nautilus.project.author)

		self.properties = []
		self.propModel = QStringListModel()
		self.loadProperties()

		self.loadPlayerCombo()

		self.cbPlayer.setEditText(self.nautilus.project.player)

		self.loadArticles()

	@property
	def cancel(self) -> bool:
		return self.__cancel

	def loadProperties(self):
		project = self.nautilus.project

		self.properties.clear()

		keys = project.properties.keys()

		for k in keys:
			self.properties.append(f"{k}={project.properties[k]}")

		self.propModel = QStringListModel(self.properties)
		self.lstProperties.setModel(self.propModel)

	def addProp(self) -> None:
		text, ok = QInputDialog.getText(self, "Add Property", "key=value")
		if not ok: return None

		prop = text.split("=")
		if len(prop) != 2: return

		self.properties.append(f"{prop[0].strip()}={prop[1].strip()}")

		self.propModel = QStringListModel(self.properties)
		self.lstProperties.setModel(self.propModel)

	def editProp(self) -> None:
		index = self.lstProperties.currentIndex()
		if index.row() == -1: return

		text, ok = QInputDialog.getText(self, "Edit Property", "key=value", text=self.properties[index.row()])
		if not ok: return None

		prop = text.split("=")
		if len(prop) != 2: return

		self.properties[index.row()] = f"{prop[0].strip()}={prop[1].strip()}"

		self.propModel = QStringListModel(self.properties)
		self.lstProperties.setModel(self.propModel)

	def removeProp(self) -> None:
		index = self.lstProperties.currentIndex()
		if index.row() == -1: return

		self.properties.pop(index.row())

		self.propModel = QStringListModel(self.properties)
		self.lstProperties.setModel(self.propModel)

	def loadPlayerCombo(self) -> None:
		self.cbPlayer.clear()
		for n in self.nautilus.project.dictionary.nouns():
			self.cbPlayer.addItem(n.name)

	def loadArticles(self) -> None:
		d = self.nautilus.project.dictionary
		for a in d.articles():
			if a.indefinited:
				if not a.female and not a.plural:
					self.edtIndefMaleSing.setText(a.name)
				if a.female and not a.plural:
					self.edtIndefFemaleSing.setText(a.name)
				if not a.female and a.plural:
					self.edtIndefMalePlural.setText(a.name)
				if a.female and a.plural:
					self.edtIndefFemalePlural.setText(a.name)
			else:
				if not a.female and not a.plural:
					self.edtDefMaleSing.setText(a.name)
				if a.female and not a.plural:
					self.edtDefFemaleSing.setText(a.name)
				if not a.female and a.plural:
					self.edtDefMalePlural.setText(a.name)
				if a.female and a.plural:
					self.edtDefFemalePlural.setText(a.name)

	def savePressed(self) -> None:
		self.__cancel = False
		self.close()