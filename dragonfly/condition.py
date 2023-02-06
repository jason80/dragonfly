from abc import ABC, abstractmethod

import dragonfly

from PyQt5.QtXml import QDomElement

class Condition(ABC):
	def __init__(self) -> None:
		pass

	@abstractmethod
	def check(self, action: "dragonfly.Action") -> bool:
		pass

	@abstractmethod
	def load(self, element: QDomElement):
		pass
