from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (QFrame, QLineEdit, QMainWindow, QTextEdit,
                             QVBoxLayout, QWidget)

import dragonfly
import dragonfly.output

class ConsoleLineEdit(QLineEdit):
	"""Line text box in the main console.
	"""
	def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
		"""Occurs when the player hits a key in line edit on main console.
		"""
		if event.key() == Qt.Key_Up:
			self.setText(Console.instance.history.up())
		
		if event.key() == Qt.Key_Down:
			self.setText(Console.instance.history.down())
		
		return super().keyPressEvent(event)


class Console(QMainWindow):
	"""The main console.
	"""
	instance = None

	def __init__(self, game, consoleWidth: int, consoleHeight: int) -> None:
		super().__init__()

		Console.instance = self

		self.game = game

		self.__styles = dragonfly.output.ConsoleStyles()

		self.centralWidget = QWidget(self)
		self.setCentralWidget(self.centralWidget)
		self.verticalLayout = QVBoxLayout(self.centralWidget)

		self.resize(consoleWidth, consoleHeight)

		# Output
		self.textOutput = QTextEdit(self.centralWidget)
		self.verticalLayout.addWidget(self.textOutput)
		self.textOutput.setReadOnly(True)
		self.textOutput.setFocusPolicy(Qt.NoFocus)
		self.textOutput.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.textOutput.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.textOutput.setFrameShape(QFrame.NoFrame)
		self.textOutput.setTextInteractionFlags(Qt.NoTextInteraction)

		# Input
		self.textInput = ConsoleLineEdit(self.centralWidget)
		self.verticalLayout.addWidget(self.textInput)
		self.textInput.setFrame(False)

		self.inputMode = True

		# Connect input action
		self.textInput.returnPressed.connect(self.__consoleReturnPressed)

		# Internal print
		self.game.execWorker.console_print.connect(self.__internalPrint)
		# Internal clear output
		self.game.execWorker.console_clear.connect(self.textOutput.clear)
		# Internal console quit
		self.game.execWorker.console_quit.connect(self.close)

		# History
		self.history = dragonfly.output.History()

	def __consoleReturnPressed(self) -> None:
		"""Occurs when the player hit enter.
		"""
		self.inputMode = False

	def setStyle(self, style: str) -> None:
		"""Set the style for console.

		Args:
			style (str): Style string.
		"""
		self.__styles.parse(style)

		self.textOutput.setFontFamily(self.__styles.current["family"])
		self.textOutput.setFontPointSize(self.__styles.current["size"])
		self.textOutput.setFontWeight(QFont.Bold if self.__styles.current["bold"] else 0)
		self.textOutput.setFontItalic(self.__styles.current["italic"])
		self.textOutput.setTextColor(QColor(self.__styles.current["color"]))

	def resetStyle(self) -> None:
		"""Return style to default.
		"""
		self.__styles.reset()

	def __internalPrint(self, d: dict) -> None:
		"""Insert text in the output.

		Args:
			d (dict): Message pack: style + message
		"""
		self.setStyle(d["style"])

		msg = self.__replaceObjects(d["msg"])

		self.textOutput.insertPlainText(msg)

		# Move scroll to bottom
		sb = self.textOutput.verticalScrollBar()
		sb.setValue(sb.maximum())

		# Reset to default style
		self.instance.resetStyle()

	def __replaceObjects(self, text: str) -> str:
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
									result += self.__replaceGenderNumber(obj, params, capitalize)
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

	def __replaceGenderNumber(self, obj, params: str, capitalize: bool) -> str:
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

	# Static
	def print(string: str, style: str = "") -> None:
		Console.instance.game.execWorker.console_print.emit({"msg": string + " ", "style": style})

	def println(string: str, style: str = "") -> None:
		Console.instance.game.execWorker.console_print.emit({"msg": string + "\n", "style": style})

	def clear() -> None:
		Console.instance.game.execWorker.console_clear.emit()

	def input() -> str:
		Console.instance.inputMode = True

		while Console.instance.inputMode:
			pass

		line = Console.instance.textInput.text()

		# Add to history
		Console.instance.history.store(line)

		Console.instance.textInput.clear()
		return line

	def pause():
		pass
