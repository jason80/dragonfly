import typing, sys
from PyQt5.QtWidgets import QApplication

import nautilus.view.main_window

class Nautilus(QApplication):
	def __init__(self, argv: typing.List[str]) -> None:
		super().__init__(argv)

		self.__mainWindow = nautilus.view.main_window.MainWindow(self)

	@property
	def mainWindow(self) -> "nautilus.view.main_window.MainWindow":
		return self.__mainWindow

if __name__ == "__main__":
	app = Nautilus(sys.argv)
	sys.exit(app.exec_())
