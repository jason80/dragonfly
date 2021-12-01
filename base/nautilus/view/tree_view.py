import typing
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt

class TreeNode(object):
	def __init__(self, data) -> None:
		self.__data = data

		self.__children = []
		self.__parent = None
		self.__row = 0

	def data(self):
		return self.__data

	def childCount(self) -> int:
		return len(self.__children)

	def child(self, row: int) -> "TreeNode":
		if row >= 0 and row < self.childCount():
			return self.__children[row]

	def parent(self) -> "TreeNode":
		return self.__parent

	def row(self) -> int:
		return self.__row

	def addChild(self, child: "TreeNode") -> None:
		child.__parent = self
		child.__row = len(self.__children)
		self.__children.append(child)
		
class TreeModel(QAbstractItemModel):
	def __init__(self, nodes: typing.List[TreeNode]) -> None:
		super().__init__()

		self.__root = TreeNode(None)
		for node in nodes:
			self.__root.addChild(node)

	def rowCount(self, index: QModelIndex) -> int:
		if index.isValid():
			return index.internalPointer().childCount()
		return self.__root.childCount()

	def addChild(self, node: TreeNode, _parent: QModelIndex) -> None:
		if not _parent or not _parent.isValid():
			parent = self.__root
		else:
			parent = _parent.internalPointer()

		parent.addChild(node)

	def index(self, row: int, column: int, _parent: QModelIndex = None) -> QModelIndex:
		if not _parent or not _parent.isValid():
			parent = self.__root
		else:
			parent = _parent.internalPointer()

		if not QAbstractItemModel.hasIndex(self, row, column, _parent):
			return QModelIndex()

		child = parent.child(row)
		if child:
			return QAbstractItemModel.createIndex(self, row, column, child)
		else:
			return QModelIndex()

	def parent(self, index: QModelIndex) -> QModelIndex:
		if index.isValid():
			p = index.internalPointer().parent()
			if p:
				return QAbstractItemModel.createIndex(self, p.row(), 0, p)
		return QModelIndex()

	def columnCount(self, index: QModelIndex) -> int:
		if index.isValid():
			return 1
		return 1

	def data(self, index: QModelIndex, role: int) -> typing.Any:
		if not index.isValid():
			return None
		node = index.internalPointer()
		if role == Qt.DisplayRole:
			return str(node.data())
		return None

	def getItem(self, index: QModelIndex):
		if index.isValid():
			node = index.internalPointer()
			if node:
				return node.data()

		return self.__root.data()