import typing
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QWidget
from PyQt5 import uic

class NewProjectDialog(QDialog):
	def __init__(self, parent: typing.Optional[QWidget]) -> None:
		super().__init__(parent=parent)

		self.edtTitle = QLineEdit()
		self.edtAuthor = QLineEdit()
		self.edtPath = QLineEdit()
		self.btnCreate = QPushButton()
		self.btnSelectPath = QPushButton()

		uic.loadUi("base/nautilus/view/new-project.ui", self)

		# Signals
		self.btnSelectPath.clicked.connect(self.selectPath)

	def selectPath(self) -> None:
		print("Select path")


