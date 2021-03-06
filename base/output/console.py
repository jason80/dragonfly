from PyQt5 import QtGui
import dfexcept
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (QFrame, QLineEdit, QMainWindow, QTextEdit,
                             QVBoxLayout, QWidget)
from output.history import History

from output.styles import ConsoleStyles

class ConsoleLineEdit(QLineEdit):

	def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
		if event.key() == Qt.Key_Up:
			self.setText(Console.instance.history.up())
		
		if event.key() == Qt.Key_Down:
			self.setText(Console.instance.history.down())
		
		return super().keyPressEvent(event)


class Console(QMainWindow):

	instance = None

	def __init__(self, game, consoleWidth: int, consoleHeight: int) -> None:
		super().__init__()

		Console.instance = self

		self.game = game

		self.__styles = ConsoleStyles()

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
		# Internal cloear output
		self.game.execWorker.console_clear.connect(self.textOutput.clear)

		# History
		self.history = History()

	def __consoleReturnPressed(self) -> None:
		self.inputMode = False

	def setStyle(self, style: str) -> None:
		self.__styles.parse(style)

		self.textOutput.setFontFamily(self.__styles.current["family"])
		self.textOutput.setFontPointSize(self.__styles.current["size"])
		self.textOutput.setFontWeight(QFont.Bold if self.__styles.current["bold"] else 0)
		self.textOutput.setFontItalic(self.__styles.current["italic"])
		self.textOutput.setTextColor(QColor(self.__styles.current["color"]))

	def resetStyle(self) -> None:
		self.__styles.reset()

	def __internalPrint(self, d: dict) -> None:
		self.setStyle(d["style"])

		msg = self.__replaceObjects(d["msg"])

		self.textOutput.insertPlainText(msg)

		# Move scroll to bottom
		sb = self.textOutput.verticalScrollBar()
		sb.setValue(sb.maximum())

		# Reset to default style
		self.instance.resetStyle()

	def __replaceObjects(self, text: str) -> str:
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

				if text[i] == "1":
					obj = self.game.parser.directObject
				elif text[i] == "2":
					obj = self.game.parser.indirectObject

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
							raise dfexcept.DragonflyException('Console: expected character "(" followed by @.')
				if capitalize:
					result += f"{objName[0].upper()}{objName[1:]}"
				else:
					result += objName
					
			else:
				result += ch

			i += 1
		return result

	def __replaceGenderNumber(self, obj, params: str, capitalize: bool) -> str:
		members = params.split(",")
		if len(members) != 4:
			raise dfexcept.DragonflyException("Console: expeted 4 parameters followed by @.")

		if not obj.isSet("female") and not obj.isSet("plural"): return members[0]
		if obj.isSet("female") and not obj.isSet("plural"): return members[1]
		if not obj.isSet("female") and obj.isSet("plural"): return members[2]
		if obj.isSet("female") and obj.isSet("plural"): return members[3]

		return ""

	# Static
	def print(string: str, style: str = "") -> None:
		Console.instance.game.execWorker.console_print.emit({"msg": string, "style": style})

	def println(string: str, style: str = "") -> None:
		Console.print(string + "\n", style)

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
