import dfbase
import nautilus.app
import nautilus.view.new_project_dialog

class Project:
	def __init__(self, nautilus: nautilus.app.Nautilus) -> None:
		self.__nautilus = nautilus
		self.__dictionary = dfbase.Dictionary(None)
		self.__active = False

	@property
	def dictionary(self) -> "dfbase.Dictionary":
		return self.__dictionary

	@dictionary.setter
	def dictionary(self, dict: "dfbase.Dictionary") -> None:
		self.__dictionary = dict

	@property
	def nautilus(self) -> "nautilus.app.Nautilus":
		return self.__nautilus

	@property
	def active(self) -> bool:
		return self.__active
		
	def new(self) -> None:

		dialog = nautilus.view.new_project_dialog.NewProjectDialog(self.nautilus.mainWindow)
		dialog.exec()

		self.__dictionary.clear()
		self.__active = True

		print("New Project")