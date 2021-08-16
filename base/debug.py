from output.console import Console
import entities
from typing import List
import action

class Info(action.Action):

	def __init__(self) -> None:
		super().__init__()

		self.nounList = List[entities.Noun]

	def init(self) -> bool:

		self.nounList = self.dictionary.nouns(self.parser.directObjectString)
		if not self.nounList:
			Console.println("Nouns not found in dictionary.", "family: 'Courier'")
			return False

		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		for n in self.nounList:
			self.printNounInfo(n)

		Console.println("-" * 20, "family: 'Courier'")

	def report(self) -> None:
		pass

	def printNounInfo(self, noun: "entities.Noun") -> None:
		Console.println("-" * 20, "family: 'Courier'")
		Console.println(f"Names: {noun.names}", "family: 'Courier'")
		Console.println(f"Container: {noun.container.name if noun.container else 'None'}", "family: 'Courier'")
		if noun.attributes:
			Console.println(f"Attributes: {noun.attributes}", "family: 'Courier'")
		if noun.variables:
			Console.println(f"Variables: {noun.variables}", "family: 'Courier'")
		if noun.connections:
			Console.println("Connections:", "family: 'Courier'")
			for c in noun.connections:
				Console.println(f"\t{c.exit} --> {c.destiny}", "family: 'Courier'")

class Tree(action.Action):

	def __init__(self) -> None:
		super().__init__()
		self.nounList = []

	def init(self) -> bool:
		for n in self.dictionary.nouns(""):
			if not n.container:
				self.nounList.append(n)
		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		Console.println("Nouns:", "family: 'Courier'")
		for n in self.nounList:
			self.printNode(n)

	def report(self) -> None:
		pass

	def printNode(self, noun: entities.Noun, indent: str = "") -> None:
		Console.println(f"{indent}{noun.names}", "family: 'Courier'")
		for n in noun.childs():
			self.printNode(n, indent + "   ")

class Attr(action.Action):

	def __init__(self) -> None:
		super().__init__()
		self.obj = None
		self.attrs = ""
		self.command = ""

	def init(self) -> bool:
		lst = self.dictionary.nouns(self.parser.directObjectString)
		if not lst:
			Console.println("Attr: noun not found in dictionary.", "family: 'Courier'")
			return False

		self.command = self.parser.keyword.lower()

		self.obj = lst[0]
		return True

	def check(self) -> bool:

		Console.println(self.command)

		if self.command != "set" and self.command != "unset":
			Console.println("Attr: usage: 'attr <obj> set/unset <attr list>'.", "family: 'Courier'")
			return False
		return True

	def carryOut(self) -> None:
		lst = []
		for a in self.parser.indirectObjectString.split(" "):
			if a.strip():
				lst.append(a)

		if self.command == "set":
			self.obj.set(lst)
			Console.println(f'setted {lst} to {self.obj.name}.', "family: 'Courier'")
		if self.command == "unset":
			self.obj.unset(lst)
			Console.println(f'unsetted {lst} to {self.obj.name}.', "family: 'Courier'")

	def report(self) -> None:
		pass
