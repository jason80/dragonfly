import dragonfly
from dragonfly.output import Console

class Help:

	def __init__(self) -> None:
		pass

	# Static
	def tip(msg: str) -> None:
		"""Show tip message for helping

		Args:
			msg (str): String message
		"""
		Console.println(f'<{msg}>', 'family: "Sans"; italic: True')

	def tipOnce(noun: dragonfly.Noun, msg: str) -> None:
		"""Show tip message for helping once, while is not set 'tip' on noun instance.

		Args:
			noun (entities.Noun): noun instance
			msg (str): String message
		"""
		if not noun.isSet("tip"):
			Help.tip(msg)
			noun.set(["tip"])
