from PyQt5.QtXml import QDomElement

import dragonfly
from dragonfly import DragonflyException

class IsSet(dragonfly.Condition):
	def __init__(self) -> None:
		super().__init__()

		self.instance = ""
		self.attr = ""

	def __str__(self) -> str:
		return f'Is set "{self.attr}" on "{self.instance}"'

	def check(self, action: "dragonfly.Action") -> bool:
		# Gets the noun
		noun = action.dictionary.nouns(self.instance)
		if not noun:
			raise DragonflyException(f'On IsSet condition: instance "{self.instance}" not found in dictionary.')
	
		return noun[0].isSet(self.attr)

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance")
		self.attr = element.attribute("attr")

class IsNotSet(dragonfly.Condition):
	def __init__(self) -> None:
		super().__init__()

		self.instance = ""
		self.attr = ""

	def __str__(self) -> str:
		return f'Is not set "{self.attr}" on "{self.instance}"'

	def check(self, action: "dragonfly.Action") -> bool:
		# Gets the noun
		noun = action.dictionary.nouns(self.instance)
		if not noun:
			raise DragonflyException(f'On IsNotSet condition: instance "{self.instance}" not found in dictionary.')
	
		return not noun[0].isSet(self.attr)

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance")
		self.attr = element.attribute("attr")

class DirectEqualsExit(dragonfly.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.exit = ""

	def __str__(self) -> str:
		return f'Direct equals exit: "{self.exit}"'

	def check(self, action: "dragonfly.Action") -> bool:
		e = action.dictionary.exit(self.exit)
		if not e:
			raise DragonflyException(f'On DirectEqualsExit condition: exit "{self.exit}" not found in dictionary.')

		return e.responds(action.parser.directObjectString)

	def load(self, element: QDomElement):
		self.exit = element.attribute("exit")
		
class Contains(dragonfly.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.container = ""
		self.instance = ""

	def __str__(self) -> str:
		return f'"{self.container}" contains "{self.instance}"'

	def check(self, action: "dragonfly.Action") -> bool:
		cont = action.dictionary.nouns(self.container)
		if not cont:
			raise DragonflyException(f'On Contains condition: container "{self.container}" not found in dictionary.')

		return cont[0].contains(self.instance)

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance", defaultValue="")
		self.container = element.attribute("container", defaultValue="")

class NotContains(dragonfly.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.container = ""
		self.instance = ""

	def __str__(self) -> str:
		return f'"{self.container}" not contains "{self.instance}"'

	def check(self, action: "dragonfly.Action") -> bool:
		cont = action.dictionary.nouns(self.container)
		if not cont:
			raise DragonflyException(f'On NotContains condition: container "{self.container}" not found in dictionary.')

		return not cont[0].contains(self.instance)

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance", defaultValue="")
		self.container = element.attribute("container", defaultValue="")

class DirectEquals(dragonfly.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.instance = ""

	def __str__(self) -> str:
		return f'Direct equals "{self.instance}"'

	def check(self, action: "dragonfly.Action") -> bool:
		obj = action.parser.directObject
		if not obj: return False

		return obj.responds(self.instance)

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance", defaultValue="")

class DirectNotEquals(dragonfly.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.instance = ""

	def __str__(self) -> str:
		return f'Direct not equals "{self.instance}"'

	def check(self, action: "dragonfly.Action") -> bool:
		obj = action.parser.directObject
		if not obj: return True

		return not obj.responds(self.instance)

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance", defaultValue="")

class IndirectEquals(dragonfly.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.instance = ""

	def __str__(self) -> str:
		return f'Indirect equals "{self.instance}"'

	def check(self, action: "dragonfly.Action") -> bool:
		obj = action.parser.indirectObject
		if not obj: return False

		return obj.responds(self.instance)

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance", defaultValue="")

class IndirectNotEquals(dragonfly.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.instance = ""

	def __str__(self) -> str:
		return f'Indirect equals "{self.instance}"'

	def check(self, action: "dragonfly.Action") -> bool:
		obj = action.parser.indirectObject
		if not obj: return True

		return not obj.responds(self.instance)

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance", defaultValue="")

class VariableEquals(dragonfly.Condition):
	def __init__(self) -> None:
		super().__init__()
		self.instance = ""
		self.variable = ""
		self.value = ""

	def __str__(self) -> str:
		return f'Variable "{self.variable}" equals to "{self.value}."'

	def check(self, action: "dragonfly.Action") -> bool:
		obj = action.dictionary.nouns(self.instance)

		if not obj:
			raise dragonfly.DragonflyException(
				f'On condition "VariableEquals" instance "{self.instance}" not found in dictionary.')
		
		obj = obj[0]

		return obj.getVariable(self.variable) == self.value

	def load(self, element: QDomElement):
		self.instance = element.attribute("instance", defaultValue="")
		self.variable = element.attribute("variable", defaultValue="")
		self.value = element.attribute("value", defaultValue="")
