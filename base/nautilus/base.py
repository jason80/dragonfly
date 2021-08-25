from PyQt5.QtCore import QFile, QIODevice, QTextStream
from PyQt5.QtXml import QDomDocument
import dfbase
import nautilus.app
import nautilus.view.new_project_dialog

class Project:
	def __init__(self, nautilus: nautilus.app.Nautilus) -> None:
		self.__nautilus = nautilus
		self.__dictionary = dfbase.Dictionary(None)
		self.__active = False

		self.__title = ""
		self.__author = ""
		self.__path = ""

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
	def path(self) -> str:
		return self.__path

	@path.setter
	def path(self, path: str) -> None:
		self.__path = path
		
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

		print(f"Project created '{self.__title}'.")
		print(f"Location: '{self.__path}'.")

	def load(self):
		doc = QDomDocument()
		file = QFile(f"{self.__path}/nautilus.xml")
		if not file.open(QIODevice.ReadOnly or QIODevice.Text):
			# TODO: Error
			pass

		if not doc.setContent(file):
			file.close()
			# TODO: Error

		file.close()

		root = doc.firstChildElement()

		if root.tagName() != "nautilus": return None # TODO: Error

		self.__title = root.attribute("title")
		self.__author = root.attribute("author")
		
	def save(self):
		doc = QDomDocument()

		p_inst = doc.createProcessingInstruction("xml", 'version="1.0" encoding="UTF-8"')
		doc.appendChild(p_inst)

		root = doc.createElement("nautilus")
		doc.appendChild(root)

		# Save info
		root.setAttribute("title", self.__title)
		root.setAttribute("author", self.__author)

		# Write file
		file = QFile(self.__path + "/" + "nautilus.xml")
		if not file.open(QFile.WriteOnly or QFile.Truncate):
			# TODO: Error
			pass

		outstream = QTextStream(file)
		doc.save(outstream, 4)
		outstream.flush()
		file.close()