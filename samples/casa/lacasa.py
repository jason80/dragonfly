import dialogs
import dfbase

class LaCasa(dfbase.Game):

	def __init__(self) -> None:
		super().__init__(800, 600)

	def init(self) -> None:
		self.dictionary.load("templates/dict-debug.xml")
		self.dictionary.load("templates/dict-es.xml")
		self.dictionary.load("samples/casa/auxiliar.xml")
		self.dictionary.load("samples/casa/living.xml")
		self.dictionary.load("samples/casa/pasillo.xml")

		self.dictionary.seeListDialog = dialogs.ListDialog("Puedes ver:", ", ", " y ")
		self.dictionary.inventoryDialog = dialogs.ListDialog("Tienes en tu poder:", ", ", " y ")
		self.dictionary.lookInsideDialog = dialogs.ListDialog("Dentro hay:", ", ", " y ")
		self.dictionary.objectChooserDialog = dialogs.ObjectChooserDialog("¿Cuál?", "No importa.", "Opción incorrecta.")

		self.player = self.dictionary.nouns("player")[0]

		self.setProperty("look-around", "always")
		self.setProperty("show-parsing-process", "false")

if __name__ == "__main__":
	game = LaCasa()
	game.run()