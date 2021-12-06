import typing
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QDialog, QListView, QPushButton, QWidget
from PyQt5 import uic

class ImportDialog(QDialog):
	def __init__(self, parent: typing.Optional[QWidget]) -> None:
		super().__init__(parent=parent)

		self.__cancel = True

		self.lstTemplates = QListView()
		self.dictModel = QStringListModel()
		self.btnImport = QPushButton()

		uic.loadUi("base/nautilus/view/import.ui", self)

		self.templateList = ["dict-es.xml"]
		self.lstTemplates.setModel(QStringListModel(self.templateList))

		self.selected = ""

		self.btnImport.clicked.connect(self.importClicked)
		self.lstTemplates.clicked.connect(self.templateSelected)

		self.exec()

	@property
	def cancel(self) -> bool:	
		return self.__cancel

	def importClicked(self) -> None:
		self.__cancel = False
		self.close()
		
	def templateSelected(self):
		index = self.lstTemplates.currentIndex()
		if index.row() != -1:
			self.selected = self.templateList[index.row()]
			self.btnImport.setEnabled(True)
		else:
			self.selected = ""
			self.btnImport.setEnabled(False)
