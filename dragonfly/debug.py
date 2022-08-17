import typing
import dragonfly
from dragonfly.output import Console

class Info(dragonfly.Action):

	def __init__(self) -> None:
		super().__init__()

		self.nounList = typing.List[dragonfly.Noun]

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

	def printNounInfo(self, noun: "dragonfly.Noun") -> None:
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

	def responses(self) -> typing.Tuple[str]:
		return ()

class Tree(dragonfly.Action):

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

	def printNode(self, noun: dragonfly.Noun, indent: str = "") -> None:
		Console.println(f"{indent}{noun.names}", "family: 'Courier'")
		for n in noun.childs():
			self.printNode(n, indent + "   ")

	def responses(self) -> typing.Tuple[str]:
		return ()

class TreeObject(Tree):
	def init(self) -> bool:
		for n in self.dictionary.nouns(self.parser.directObjectString):
			self.nounList.append(n)

		if not self.nounList:
			Console.println("Tree: No results.", "family: 'Courier'")
		return True

class Attr(dragonfly.Action):

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

	def responses(self) -> typing.Tuple[str]:
		return ()

class Move(dragonfly.Action):
	def __init__(self) -> None:
		super().__init__()
		
		self.__object = None
		self.__dest = None

	def init(self) -> bool:

		# Direct object
		name = self.parser.directObjectString
		lst = self.game.dictionary.nouns(name)
		if not lst:
			Console.println(f'Move: "{name}" not found in dictionary.', "family: 'Courier'")
			return False

		self.__object = self.dictionary.objectChooserDialog.execute(lst)
		if not self.__object: return False

		name = self.parser.indirectObjectString
		lst = self.game.dictionary.nouns(name)
		if not lst:
			Console.println(f'Move: "{name}" not found in dictionary.', "family: 'Courier'")
			return False

		self.__dest = self.dictionary.objectChooserDialog.execute(lst)
		if not self.__dest: return False

		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		self.__object.container = self.__dest
		Console.println(f'"{self.__object.name}" moved to "{self.__dest.name}".', "family: 'Courier'")

	def report(self) -> None:
		pass

	def responses(self) -> typing.Tuple[str]:
		return ()

class Root(dragonfly.Action):
	def __init__(self) -> None:
		super().__init__()
		self.__object = None

	def init(self) -> bool:

		name = self.parser.directObjectString
		lst = self.dictionary.nouns(name)

		if not lst:
			Console.println(f'Root: "{name}" not found in dictionary.', "family: 'Courier'")
			return False

		self.__object = self.dictionary.objectChooserDialog.execute(lst)
		if not self.__object: return False

		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		self.__object.container = None
		Console.println(f'"{self.__object.name}" moved to ROOT.', "family: 'Courier'")

	def report(self) -> None:
		pass

	def responses(self) -> typing.Tuple[str]:
		return ()

class VerbInfo(dragonfly.Action):
	def __init__(self) -> None:
		super().__init__()
		self.verbList = []

	def init(self) -> bool:
		name = self.parser.directObjectString

		if name == "all":
			self.verbList = self.dictionary.verbs()
		else:
			self.verbList = self.dictionary.verbs(name)

		if not self.verbList:
			Console.println(f'Verb: "{name}" not found in dictionary.', "family: 'Courier'")
			Console.println(f'Verb: use: "verb all" to list all verbs.', "family: 'Courier'")
			return False
		return True

	def check(self) -> bool:
		return True

	def carryOut(self) -> None:
		Console.println('---------------------------', "family: 'Courier'")
		for v in self.verbList:
			self.__verbInfo(v)
			Console.println('---------------------------', "family: 'Courier'")

	def report(self) -> None:
		pass

	def responses(self) -> typing.Tuple[str]:
		return ()

	def __verbInfo(self, verb: dragonfly.Verb) -> None:
		Console.println(f'Action: "{verb.action.__name__}" Syntax: "{verb.syntax}":', "family: 'Courier'")
		Console.println(f'{verb.names}', "family: 'Courier'")
