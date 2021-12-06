import entities
import nautilus.app
import nautilus.view.widgets
import nautilus.view.game_prop_dialog
from nautilus.view.tree_view import TreeModel, TreeNode
from PyQt5 import uic
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import (QAction, QInputDialog, QListView, QMainWindow,
                             QPlainTextEdit, QScrollArea, QSplitter, QToolButton, QTreeView,
                             QWidget)


class MainWindow(QMainWindow):
	def __init__(self, nautilus: "nautilus.app.Nautilus") -> None:
		super().__init__()

		self.__nautilus = nautilus

		# Menus
		self.actionNewProject = QAction()
		self.actionOpenProject = QAction()
		self.actionSaveProject = QAction()
		self.actionCloseProject = QAction()
		self.actionProperties = QAction()
		self.actionNewNoun = QAction()
		self.actionNewVerb = QAction()
		self.actionNewExit = QAction()
		self.actionImport = QAction()

		# Buttons
		self.btnUpVerb = QToolButton()
		self.btnDownVerb = QToolButton()

		self.actionDebug = QAction()

		# Splitters
		self.vSplitter = QSplitter()
		self.hSplitter = QSplitter()

		# Nouns tree
		self.nounsTree = QTreeView()
		self.nounsTreeModel = TreeModel([])

		# Verb list
		self.verbList = QListView()
		self.verbListModel = QStringListModel()

		# Exit list
		self.exitList = QListView()
		self.exitListModel = QStringListModel()

		# Work widget
		self.workWidget = QWidget()
		self.workScroll = QScrollArea()

		# Log
		self.edtLog = QPlainTextEdit()

		uic.loadUi("base/nautilus/view/main-window.ui", self)

		# Signals
		self.actionNewProject.triggered.connect(self.__nautilus.project.new)
		self.actionOpenProject.triggered.connect(self.__nautilus.project.open)
		self.actionSaveProject.triggered.connect(self.__nautilus.project.save)

		self.actionProperties.triggered.connect(self.gameProperties)

		self.actionImport.triggered.connect(self.__nautilus.project.importDictionary)

		self.actionNewNoun.triggered.connect(self.newNoun)
		self.actionNewVerb.triggered.connect(self.newVerb)
		self.actionNewExit.triggered.connect(self.newExit)

		self.actionDebug.triggered.connect(self.debug)

		self.nounsTree.clicked.connect(self.nounsTreeClicked)
		self.verbList.clicked.connect(self.verbListClicked)
		self.exitList.clicked.connect(self.exitListClicked)

		self.btnUpVerb.clicked.connect(self.upVerb)
		self.btnDownVerb.clicked.connect(self.downVerb)

		# Sizes
		self.vSplitter.setSizes([200, 400])
		self.hSplitter.setSizes([600, 200])

		# Update UI

		self.update()
		self.displayNouns()
		self.displayVerbs()
		self.displayExits()

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
		self.actionSaveProject.setEnabled(False)
		self.actionNewNoun.setEnabled(False)
		self.actionNewVerb.setEnabled(False)
		self.actionNewExit.setEnabled(False)
		self.actionDebug.setEnabled(False)
		self.actionProperties.setEnabled(False)
		self.actionImport.setEnabled(False)

		if active:
			self.actionCloseProject.setEnabled(True)
			self.actionSaveProject.setEnabled(True)
			self.actionNewNoun.setEnabled(True)
			self.actionNewVerb.setEnabled(True)
			self.actionNewExit.setEnabled(True)
			self.actionDebug.setEnabled(True)
			self.actionProperties.setEnabled(True)
			self.actionImport.setEnabled(True)

		self.displayNouns()
		self.displayVerbs()
		self.displayExits()

	def nounsTreeClicked(self):
		selected = self.nounsTree.selectedIndexes()
		if selected:
			index = selected[0]
			noun = self.nounsTreeModel.getItem(index)
			
			self.workWidget.close()
			self.workWidget = nautilus.view.widgets.NounWidget(self.vSplitter, 
								self.__nautilus, noun)
			self.workScroll.setWidget(self.workWidget)
			self.workScroll.update()

	def verbListClicked(self):
		index = self.verbList.currentIndex()
		if index.row() == -1: return

		self.workWidget.close()
		self.workWidget = nautilus.view.widgets.VerbWidget(self.vSplitter, 
			self.__nautilus, self.nautilus.project.dictionary.verbs()[index.row()])
		self.workScroll.setWidget(self.workWidget)
		self.workScroll.update()

	def exitListClicked(self):
		index = self.exitList.currentIndex()
		if index.row() == -1: return

		self.workWidget.close()
		self.workWidget = nautilus.view.widgets.ExitWidget(self.vSplitter,
			self.__nautilus, self.nautilus.project.dictionary.exits()[index.row()])
		self.workScroll.setWidget(self.workWidget)
		self.workScroll.update()

	def upVerb(self) -> None:
		index = self.verbList.currentIndex()
		if index.row() < 1: return

		verbs = self.nautilus.project.dictionary.verbs()
		verbs[index.row()], verbs[index.row() - 1] = verbs[index.row() - 1], verbs[index.row()]

		sel = index.row() - 1

		self.displayVerbs()

		self.verbList.setCurrentIndex(self.verbListModel.index(sel, 0))

	def downVerb(self) -> None:
		index = self.verbList.currentIndex()
		if index.row() == -1 or index.row() == len(self.nautilus.project.dictionary.verbs()) - 1: return

		verbs = self.nautilus.project.dictionary.verbs()
		verbs[index.row()], verbs[index.row() + 1] = verbs[index.row() + 1], verbs[index.row()]

		sel = index.row() + 1

		self.displayVerbs()

		self.verbList.setCurrentIndex(self.verbListModel.index(sel, 0))
		
	def displayNouns(self):
		def addNoun(node: TreeNode, noun: entities.Noun) -> None:
			for n in noun.childs():
				child = TreeNode(n)
				node.addChild(child)
				addNoun(child, n)

		root = []
		for noun in self.nautilus.project.dictionary.nouns():
			if noun.container: continue
			node = TreeNode(noun)
			root.append(node)
			addNoun(node, noun)

		self.nounsTree.setModel(TreeModel(root))

	def displayVerbs(self):
		strVerbs = []
		for verb in self.nautilus.project.dictionary.verbs():
			strVerbs.append(str(verb))

		self.verbListModel = QStringListModel(strVerbs)
		self.verbList.setModel(self.verbListModel)

	def displayExits(self):
		strExits = []
		for exit in self.nautilus.project.dictionary.exits():
			strExits.append(str(exit))

		self.exitListModel = QStringListModel(strExits)
		self.exitList.setModel(self.exitListModel)


	def newNoun(self) -> None:
		text, ok = QInputDialog.getText(self, "New Noun", "Enter the noun's names:")
		if not ok: return

		names = text.split(',')
		nameList = []
		for n in names:
			if n.strip():
				nameList.append(n.strip())

		if not nameList: return

		noun = entities.Noun()
		noun.game = self.__nautilus.project.dictionary.game
		noun.names = nameList

		self.__nautilus.project.dictionary.addNoun(noun)
		self.displayNouns()

	def newVerb(self) -> None:
		text, ok = QInputDialog.getText(self, "New Verb", "Enter the verb's names:")
		if not ok: return

		names = text.split(',')
		nameList = []
		for n in names:
			if n.strip():
				nameList.append(n.strip())

		if not nameList: return

		verb = entities.Verb()
		verb.game = self.__nautilus.project.dictionary.game
		verb.names = nameList

		self.__nautilus.project.dictionary.addVerb(verb)
		self.displayVerbs()

	def newExit(self):
		text, ok = QInputDialog.getText(self, "New Exit", "Enter the exit's names:")
		if not ok: return

		names = text.split(',')
		nameList = []
		for n in names:
			if n.strip():
				nameList.append(n.strip())

		if not nameList: return

		exit = entities.Exit()

		exit.game = self.__nautilus.project.dictionary.game
		exit.names = nameList

		self.__nautilus.project.dictionary.addExit(exit)
		self.displayExits()

	def debug(self) -> None:
		self.__nautilus.project.run(debug=True)
		
	def gameProperties(self) -> None:
		dialog = nautilus.view.game_prop_dialog.GamePropDialog(self, self.nautilus)
		dialog.exec()

		if dialog.cancel: return None

		self.nautilus.project.title = dialog.edtTitle.text()
		self.nautilus.project.author = dialog.edtAuthor.text()

		# Properties
		prop = {}
		for p in dialog.properties:
			kv = p.split("=")
			if len(kv) != 2: continue
			prop[kv[0].strip()] = kv[1].strip()

		self.nautilus.project.properties = prop

		# Player
		self.nautilus.project.player = dialog.cbPlayer.currentText()

		# Articles
		d = self.nautilus.project.dictionary
		d.articles().clear()

		a = entities.Article()
		a.name = dialog.edtDefMaleSing.text().strip()
		a.female = False; a.plural = False; a.indefinited = False
		d.addArticle(a)

		a = entities.Article()
		a.name = dialog.edtDefFemaleSing.text().strip()
		a.female = True; a.plural = False; a.indefinited = False
		d.addArticle(a)

		a = entities.Article()
		a.name = dialog.edtDefMalePlural.text().strip()
		a.female = False; a.plural = True; a.indefinited = False
		d.addArticle(a)

		a = entities.Article()
		a.name = dialog.edtDefFemalePlural.text().strip()
		a.female = True; a.plural = True; a.indefinited = False
		d.addArticle(a)

		a = entities.Article()
		a.name = dialog.edtIndefMaleSing.text().strip()
		a.female = False; a.plural = False; a.indefinited = True
		d.addArticle(a)

		a = entities.Article()
		a.name = dialog.edtIndefFemaleSing.text().strip()
		a.female = True; a.plural = False; a.indefinited = True
		d.addArticle(a)

		a = entities.Article()
		a.name = dialog.edtIndefMalePlural.text().strip()
		a.female = False; a.plural = True; a.indefinited = True
		d.addArticle(a)

		a = entities.Article()
		a.name = dialog.edtIndefFemalePlural.text().strip()
		a.female = True; a.plural = True; a.indefinited = True
		d.addArticle(a)

