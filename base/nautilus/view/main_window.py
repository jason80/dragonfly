from PyQt5.QtWidgets import QAction, QMainWindow, QSplitter
from PyQt5 import uic

import nautilus.app

class MainWindow(QMainWindow):
	def __init__(self, nautilus: "nautilus.app.Nautilus") -> None:
		super().__init__()

		self.__nautilus = nautilus

		# Menus
		self.actionNewProject = QAction()
		self.actionOpenProject = QAction()
		self.actionCloseProject = QAction()

		# Splitters
		self.vSplitter = QSplitter()
		self.hSplitter = QSplitter()

		uic.loadUi("base/nautilus/view/main-window.ui", self)

		# Signals
		self.actionNewProject.triggered.connect(self.__nautilus.project.new)
		self.actionOpenProject.triggered.connect(self.__nautilus.project.open)

		# Sizes
		self.vSplitter.setSizes([200, 400])
		self.hSplitter.setSizes([600, 200])

		# Update UI
		self.update()

		self.show()

	@property
	def nautilus(self) -> "nautilus.app.Nautilus":
		return self.__nautilus

	def update(self):

		active = self.nautilus.project.active

		# Window Title
		gameTitle = f" [{self.nautilus.project.title}]" if active else ""
		self.setWindowTitle(f"Nautilus{gameTitle}")

		self.actionCloseProject.setEnabled(False)

		if active:
			self.actionCloseProject.setEnabled(True)
		