import typing, sys, os
from PyQt5.QtWidgets import QApplication

import nautilus.base

import nautilus.view.main_window

class Nautilus(QApplication):
	def __init__(self, argv: typing.List[str]) -> None:
		super().__init__(argv)

		self.__project = nautilus.base.Project(self)

		self.__mainWindow = nautilus.view.main_window.MainWindow(self)

		# Initial path
		self.__initialPath = f'{os.getenv("HOME")}/nautilus-projects'
		if not os.path.exists(self.__initialPath):
			os.makedirs(self.__initialPath)

		self.log("--- Nautilus ---")


	@property
	def initialPath(self) -> str:
		return self.__initialPath

	@property
	def mainWindow(self) -> "nautilus.view.main_window.MainWindow":
		return self.__mainWindow

	@property
	def project(self) -> "nautilus.base.Project":
		return self.__project

	def log(self, msg: str) -> None:
		self.__mainWindow.edtLog.appendPlainText(msg)
		print(msg)

if __name__ == "__main__":
	app = Nautilus(sys.argv)
	sys.exit(app.exec_())
