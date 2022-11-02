import dragonfly

class GameLauncher(dragonfly.Game):
	def __init__(self) -> None:
		super().__init__(800, 600)

	def init(self) -> None:
		try:
			self.dictionary.load("dragonfly.xml")
		except:
			print('Error: "dragonfly.xml" not found.')
			exit(0)

if __name__ == "__main__":
	game = GameLauncher()
	game.run()
