from PyQt5.QtWidgets import QAction, QMainWindow
from PyQt5 import uic

import nautilus.app

class MainWindow(QMainWindow):
	def __init__(self, nautilus: "nautilus.app.Nautilus") -> None:
		super().__init__()

		# Menus
		self.actionNewProject = QAction()
		self.actionCloseProject = QAction()

		uic.loadUi("base/nautilus/view/main-window.ui", self)

		self.__nautilus = nautilus

		self.show()

	@property
	def nautilus(self) -> "nautilus.app.Nautilus":
		return self.__nautilus