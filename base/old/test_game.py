from output.console import Console
import dialogs
import base

class TestGame(base.Game):
	def __init__(self) -> None:
		super().__init__(800, 600, testMode=False)

	def init(self) -> None:
		self.dictionary.load("test.xml")
		self.parser.showParsingProcess = True

		self.dictionary.seeListDialog = dialogs.ListDialog("Podés ver:", ", ", " y ")

		self.player = self.dictionary.nouns("player")[0]


if __name__ == "__main__":
	test = TestGame()
	test.run()
