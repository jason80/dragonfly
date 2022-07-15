
class DragonflyException(Exception):
	"""Dragonfly general exception.
	"""
	def __init__(self, msg: str) -> None:
		super().__init__(msg)
		