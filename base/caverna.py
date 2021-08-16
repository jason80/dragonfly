from dialogs import ListDialog, ObjectChooserDialog
import dfbase

class CavernaGame(dfbase.Game):
	def __init__(self) -> None:
		super().__init__(800, 600, testMode=False)

	def init(self) -> None:

		self.dictionary.load("dict-debug.xml")

		self.dictionary.load("dict-es.xml")
		self.dictionary.load("caverna.xml")

		#self.parser.showParsingProcess = True

		self.dictionary.seeListDialog = ListDialog("Podes ver:", ", ", " y ")
		self.dictionary.objectChooserDialog = ObjectChooserDialog("¿Cuál?", "No importa.", "Opción incorrecta.")
		self.dictionary.inventoryDialog = ListDialog("Tienes en tu poder: ", ", ", " y ")

		self.player = self.dictionary.nouns("player")[0]

		#self.dictionary.save("test.sav.xml")


if __name__ == "__main__":
	game = CavernaGame()
	game.run()
