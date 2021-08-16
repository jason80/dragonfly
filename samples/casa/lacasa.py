import dfbase

class LaCasa(dfbase.Game):

	def __init__(self) -> None:
		super().__init__(800, 600)

	def init(self) -> None:
		self.dictionary.load("templates/dict-debug.xml")
		self.dictionary.load("templates/dict-es.xml")
		self.dictionary.load("samples/casa/lacasa.xml")

		self.player = self.dictionary.nouns("player")[0]

		self.setProperty("look-around", "always")
		self.setProperty("show-parsing-process", "true")

if __name__ == "__main__":
	game = LaCasa()
	game.run()