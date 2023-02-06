from abc import ABC, abstractmethod

import dragonfly

from PyQt5.QtXml import QDomElement

class ActionResponse(ABC):
	def __init__(self) -> None:
		pass

	@abstractmethod
	def execute(self, action: "dragonfly.Action") -> None:
		pass

	@abstractmethod
	def load(self, element: QDomElement) -> None:
		pass
