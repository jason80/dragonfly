
import dragonfly
import dragonfly.output

import tkinter
from tkinter import scrolledtext

class Console:
	"""The main console.
	"""
	instance = None
	tag_id = 0

	def __init__(self, game, consoleWidth: int, consoleHeight: int) -> None:
		super().__init__()

		Console.instance = self

		self.game = game

		self.__styles = dragonfly.output.ConsoleStyles()

		self.root = tkinter.Tk()
		self.root.title("Untitled")
		self.root.geometry(f"{consoleWidth}x{consoleHeight}")
		
		self.root.protocol("WM_DELETE_WINDOW", self.stop)

		self.output_text = scrolledtext.ScrolledText(self.root,
				wrap=tkinter.WORD, state=tkinter.DISABLED)
		self.output_text.pack(expand=True, fill='both')

		self.input_text = tkinter.Entry(self.root)
		self.input_text.pack(fill=tkinter.X)
		self.input_text.bind('<Return>', self.__console_return_pressed)

		self.input_text.focus()

		self.input_entered = False

		# History
		self.history = dragonfly.output.History()

	def __console_return_pressed(self, name) -> None:
		"""Occurs when the player hit enter.
		"""
		self.input_entered = True

	def setStyle(self, style: str) -> None:
		"""Set the style for console.

		Args:
			style (str): Style string.
		"""
		self.__styles.parse(style)

		Console.tag_id += 1
		tag = f"t{Console.tag_id}"

		f = (self.__styles.current["family"], self.__styles.current["size"], )
		if self.__styles.current["bold"]:
			f = f + ("bold",)
		if self.__styles.current["italic"]:
			f = f + ("italic",)

		self.output_text.tag_config(tag,
				font=f, foreground=self.__styles.current["color"])

	def resetStyle(self) -> None:
		"""Return style to default.
		"""
		self.__styles.reset()

	def __internal_print(self, d: dict) -> None:
		"""Insert text in the output.

		Args:
			d (dict): Message pack: style + message
		"""

		self.output_text.configure(state=tkinter.NORMAL)

		self.setStyle(d["style"])

		msg = self.__replace_objects(d["msg"])

		self.output_text.insert(tkinter.END, msg, f"t{Console.tag_id}")

		self.output_text.configure(state=tkinter.DISABLED)

		self.output_text.see(tkinter.END)

		# Reset to default style
		self.instance.resetStyle()

	def __replace_objects(self, text: str) -> str:
		"""Replace the special commands with the objects.

		Special commands 1:
		#: definited (the)
		#: indefinited (a)
		1: direct object
		2: indirect object
		3: parameters
		^: capitalize

		Examples:
		"#1" --> "the table"
		"%1" --> "a chair"
		"#^1" --> "The chair"

		Special commands 2:
		@: replace with the concrete text
		(a,b,c,d):
		a: singular male
		a: singular female
		a: plural male
		a: plural female

		1: direct object
		2: indirect object
		^: capitalize

		Examples:
		"#^1 @1(is,is,are,are) in the box" --> "The ball is in the box"
		(suppose that the ball is male plural)

		Args:
			text (str): text to be replace.

		Raises:
			dragonfly.DragonflyException: Occurs when not possible parse the special commands.

		Returns:
			str: Replaced text.
		"""
		result = ""
		
		i = 0

		while i < len(text):
			ch = text[i]
			if ch == "#" or ch == "%" or ch == "@":
				obj = None
				capitalize = False

				i += 1

				if text[i] == "^":
					capitalize = True
					i += 1

				# Direct Object
				if text[i] == "1":
					obj = self.game.parser.directObject
				# Indirect Object
				elif text[i] == "2":
					obj = self.game.parser.indirectObject
				# All parameters
				elif text[i] == "3":
					result += self.game.parser.parameters
					i += 1
					continue

				if not obj: result += "(NONE)"
				else:
					objName = None
					if ch == "%": objName = obj.a
					elif ch == "#": objName = obj.the
					elif ch == "@":
						i += 1
						if text[i] == "(":
							i += 1
							params = ""
							while i < len(text):
								if text[i] == ")":
									result += self.__replace_gender_number(obj, params, capitalize)
									break
								params += text[i]; i += 1

							i += 1
							continue
							
						else:
							raise dragonfly.DragonflyException('Console: expected character "(" followed by @.')
				if capitalize:
					result += f"{objName[0].upper()}{objName[1:]}"
				else:
					result += objName
					
			else:
				result += ch

			i += 1
		return result

	def __replace_gender_number(self, obj, params: str, capitalize: bool) -> str:
		"""Select the param depending the gender and the number of the noun.

		Args:
			obj (_type_): the noun.
			params (str): list of parameters (comma separated).
			capitalize (bool): force capitalization.

		Raises:
			dragonfly.DragonflyException: parameters error.

		Returns:
			str: Replaced text.
		"""
		members = params.split(",")
		if len(members) != 4:
			raise dragonfly.DragonflyException("Console: expeted 4 parameters followed by @.")

		if not obj.isSet("female") and not obj.isSet("plural"): return members[0]
		if obj.isSet("female") and not obj.isSet("plural"): return members[1]
		if not obj.isSet("female") and obj.isSet("plural"): return members[2]
		if obj.isSet("female") and obj.isSet("plural"): return members[3]

		return ""

	def start() -> None:
		Console.instance.root.mainloop()

	# Static
	def print(string: str, style: str = "") -> None:
		Console.instance.__internal_print({"msg": string + " ", "style": style})

	def println(string: str, style: str = "") -> None:
		Console.instance.__internal_print({"msg": string + "\n", "style": style})

	def clear() -> None:
		Console.instance.output_text.configure(state=tkinter.NORMAL)
		Console.instance.output_text.delete('1.0', tkinter.END)
		Console.instance.output_text.configure(state=tkinter.DISABLED)

	def pause():
		pass

	def stop(self) -> None:
		self.root.destroy()
		self.game.stop()
