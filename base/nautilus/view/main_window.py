import typing
from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtWidgets import QAction, QInputDialog, QListView, QMainWindow, QPlainTextEdit, QScrollArea, QSplitter, QTreeView, QWidget
from PyQt5 import uic
import entities
import nautilus.app
from nautilus.view.tree_view import TreeModel, TreeNode
import nautilus.view.widgets

class MainWindow(QMainWindow):
	def __init__(self, nautilus: "nautilus.app.Nautilus") -> None:
		super().__init__()

		self.__nautilus = nautilus

		# Menus
		self.actionNewProject = QAction()
		self.actionOpenProject = QAction()
		self.actionSaveProject = QAction()
		self.actionCloseProject = QAction()
		self.actionNewNoun = QAction()
		self.actionNewVerb = QAction()

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

		self.actionNewNoun.triggered.connect(self.newNoun)
		self.actionNewVerb.triggered.connect(self.newVerb)

		self.actionDebug.triggered.connect(self.debug)

		self.nounsTree.clicked.connect(self.nounsTreeClicked)
		self.verbList.clicked.connect(self.verbListClicked)

		# Sizes
		self.vSplitter.setSizes([200, 400])
		self.hSplitter.setSizes([600, 200])

		# Update UI

		self.update()
		self.displayNouns()
		self.displayVerbs()

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
		self.actionDebug.setEnabled(False)

		if active:
			self.actionCloseProject.setEnabled(True)
			self.actionSaveProject.setEnabled(True)
			self.actionNewNoun.setEnabled(True)
			self.actionNewVerb.setEnabled(True)
			self.actionDebug.setEnabled(True)

		self.displayNouns()
		self.displayVerbs()

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

	def debug(self) -> None:
		self.__nautilus.project.run(debug=True)
		