from dfexcept import DragonflyException
from PyQt5.QtXml import QDomDocument, QDomElement
import action

class IsSet(action.Condition):
	def __init__(self) -> None:
		super().__init__()

		self.instance = ""
		self.attr = ""

	def __str__(self) -> str:
		return f'Is set "{self.attr}" on "{self.instance}"'

	def check(self, action: "action.Action") -> bool:
		# Gets the noun
		noun = action.dictionary.nouns(self.instance)
		if not noun:
			raise DragonflyException(f'On IsSet condition: instance "{self.instance}" not found in dictionary.')
	
		return noun[0].isSet(self.attr)

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance")
		self.attr = element.attribute("attr")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("instance", self.instance)
		element.setAttribute("attr", self.attr)
		return element

class DirectEqualsExit(action.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.exit = ""

	def __str__(self) -> str:
		return f'Direct equals exit: "{self.exit}"'

	def check(self, action: "action.Action") -> bool:
		e = action.dictionary.exit(self.exit)
		if not e:
			raise DragonflyException(f'On DirectEqualsExit condition: exit "{self.exit}" not found in dictionary.')

		return e.responds(action.parser.directObjectString)

	def load(self, element: QDomElement):
		self.exit = element.attribute("exit")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("exit", self.exit)
		return element
		
class Contains(action.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.container = ""
		self.instance = ""

	def __str__(self) -> str:
		return f'"{self.container}" contains "{self.instance}"'

	def check(self, action: "action.Action") -> bool:
		cont = action.dictionary.nouns(self.container)
		if not cont:
			raise DragonflyException(f'On Contains condition: container "{self.container}" not found in dictionary.')

		return cont[0].contains(self.instance)

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance", defaultValue="")
		self.container = element.attribute("container", defaultValue="")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)

		element.setAttribute("instance", self.instance)
		element.setAttribute("container", self.container)

		return element

class DirectEquals(action.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.instance = ""

	def __str__(self) -> str:
		return f'Direct equals "{self.instance}"'

	def check(self, action: "action.Action") -> bool:
		obj = action.parser.directObject
		if not obj: return False

		return obj.responds(self.instance)

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance", defaultValue="")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("instance", self.instance)
		return element

class DirectNotEquals(action.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.instance = ""

	def __str__(self) -> str:
		return f'Direct not equals "{self.instance}"'

	def check(self, action: "action.Action") -> bool:
		obj = action.parser.directObject
		if not obj: return True

		return not obj.responds(self.instance)

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance", defaultValue="")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("instance", self.instance)
		return element

class IndirectEquals(action.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.instance = ""

	def __str__(self) -> str:
		return f'Indirect equals "{self.instance}"'

	def check(self, action: "action.Action") -> bool:
		obj = action.parser.indirectObject
		if not obj: return False

		return obj.responds(self.instance)

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance", defaultValue="")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("instance", self.instance)
		return element

class IndirectNotEquals(action.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.instance = ""

	def __str__(self) -> str:
		return f'Indirect equals "{self.instance}"'

	def check(self, action: "action.Action") -> bool:
		obj = action.parser.indirectObject
		if not obj: return True

		return not obj.responds(self.instance)

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance", defaultValue="")

	def save(self, doc: QDomDocument) -> QDomElement:
		element = super().save(doc)
		element.setAttribute("instance", self.instance)
		return element