import typing, platform, os
from PyQt5.QtCore import QFile, QIODevice, QTextStream
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtXml import QDomDocument, QDomNode
import dfbase
import nautilus.app
import nautilus.view.new_project_dialog
import nautilus.view.import_dialog
import nautilus.codegen

class NautilusGame(dfbase.Game):

	def __init__(self) -> None:
		super().__init__(testMode=True)

	def init(self) -> None:
		pass

class Project:
	def __init__(self, nautilus: nautilus.app.Nautilus) -> None:
		self.__nautilus = nautilus
		self.__game = NautilusGame()
		self.__dictionary = self.__game.dictionary
		self.__active = False

		self.__title = ""
		self.__author = ""
		self.__mainClass = "NautilusGame"
		self.__path = ""

		self.__properties = {}

		self.__player = ""

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

	@property
	def title(self) -> str:
		return self.__title

	@title.setter
	def title(self, title: str) -> None:
		self.__title = title

	@property
	def author(self) -> str:
		return self.__author

	@author.setter
	def author(self, author: str) -> None:
		self.__author = author

	@property
	def mainClass(self) -> str:
		return self.__mainClass

	@mainClass.setter
	def mainClass(self, mainClass: str) -> None:
		self.__mainClass = mainClass

	@property
	def path(self) -> str:
		return self.__path

	@path.setter
	def path(self, path: str) -> None:
		self.__path = path

	@property
	def properties(self) -> typing.Dict:
		return self.__properties

	@properties.setter
	def properties(self, prop: typing.Dict) -> None:
		self.__properties = prop

	@property
	def player(self) -> str:
		return self.__player

	@player.setter
	def player(self, player: str) -> None:
		self.__player = player
		
	def new(self) -> None:

		dialog = nautilus.view.new_project_dialog.NewProjectDialog(self.nautilus.mainWindow)
		dialog.exec()

		if dialog.cancel: return None

		self.__title = dialog.edtTitle.text().strip()
		self.__author = dialog.edtAuthor.text().strip()
		self.__path = dialog.edtPath.text().strip()

		self.__dictionary.clear()
		self.__active = True

		self.save()

		self.nautilus.log(f"Project created '{self.__title}'.")
		self.nautilus.log(f"Location: '{self.__path}'.")

		#print(f"Project created '{self.__title}'.")
		#print(f"Location: '{self.__path}'.")

		self.nautilus.mainWindow.update()

	def open(self):
		self.__path = QFileDialog.getExistingDirectory(self.nautilus.mainWindow, "Select Directory", self.__nautilus.initialPath, QFileDialog.DontUseNativeDialog)

		if not self.__path: return

		self.load()

		self.__active = True

		self.nautilus.log(f"Project loaded '{self.__title}'.")
		self.nautilus.log(f"Location: '{self.__path}'.")

		#print(f"Project loaded '{self.__title}'.")
		#print(f"Location: '{self.__path}'.")

		self.nautilus.mainWindow.update()

	def load(self):
		doc = QDomDocument()
		file = QFile(f"{self.__path}/nautilus.xml")
		if not file.open(QIODevice.ReadOnly or QIODevice.Text):
			# TODO: Error
			print(f'Cannot open file "{self.__path}/nautilus.xml".')

		if not doc.setContent(file):
			file.close()
			# TODO: Error
			print(f'Cannot parse file "{self.__path}/nautilus.xml".')

		file.close()

		root = doc.firstChildElement()

		if root.tagName() != "nautilus": return None # TODO: Error

		self.__title = root.attribute("title")
		self.__author = root.attribute("author")
		self.__mainClass = root.attribute("main-class")
		self.__player = root.attribute("player")

		self.__properties.clear()

		for i in range(root.childNodes().count()):
			node = root.childNodes().at(i)
			if node.nodeType() == QDomNode.ElementNode:
				child = node.toElement()
				if child.nodeName() == "property":
					self.__properties[child.attribute("key").strip()] = child.attribute("value").strip()

		# Load dictionary
		self.__dictionary.clear()
		self.__dictionary.load(f"{self.__path}/dictionary.xml")
		
	def save(self):

		# Write project file

		doc = QDomDocument()

		p_inst = doc.createProcessingInstruction("xml", 'version="1.0" encoding="UTF-8"')
		doc.appendChild(p_inst)

		root = doc.createElement("nautilus")
		doc.appendChild(root)

		# Save info
		root.setAttribute("title", self.__title)
		root.setAttribute("author", self.__author)
		root.setAttribute("main-class", self.__mainClass)
		root.setAttribute("player", self.__player)

		# Save properties
		for k in self.__properties:
			propElement = doc.createElement("property")
			propElement.setAttribute("key", k)
			propElement.setAttribute("value", self.__properties[k])
			root.appendChild(propElement)

		# Write file
		file = QFile(f"{self.__path}/nautilus.xml")
		if not file.open(QFile.WriteOnly or QFile.Truncate):
			# TODO: Error
			pass

		outstream = QTextStream(file)
		doc.save(outstream, 4)
		outstream.flush()
		file.close()

		# Write dictionary file
		self.__dictionary.save(f"{self.__path}/dictionary.xml")

		self.nautilus.log(f"Project saved '{self.__title}'.")
		self.nautilus.log(f"Location: '{self.__path}'.")		

		#print(f"Project saved '{self.__title}'.")
		#print(f"Location: '{self.__path}'.")

		self.nautilus.mainWindow.update()

	def run(self, debug: bool) -> None:

		# Save the project first
		self.save()

		nautilus.codegen.generateMainClass(self.__nautilus)
		nautilus.codegen.generateInitials(self.__nautilus, debug)

		#os.system(f'cd {self.__path};python3 {self.__path}/game.py')
		cdir = os.getcwd()

		self.__nautilus.log(f'Changing dir to "{self.__path}".')
		os.chdir(self.__path)

		self.__nautilus.log(f'Executing game.py')
		python = ""
		if platform.system() == "Linux": python = "python3"
		if platform.system() == "Windows": python = "python"
		if platform.system() == "Darwin": python = "python"

		os.system(f'{python} game.py')

		self.__nautilus.log(f'Returning to project dir.')
		os.chdir(cdir)
		
	def importDictionary(self) -> None:
		dialog = nautilus.view.import_dialog.ImportDialog(self.__nautilus.mainWindow)
		
		if dialog.cancel: return

		path = os.getenv("DFPATH") + "/templates/" + dialog.selected
		self.dictionary.load(path)

		self.nautilus.log(f'Imported from "{path}".')


		self.nautilus.mainWindow.update()
		