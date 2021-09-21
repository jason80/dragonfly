import os
import nautilus.app

def generateMainClass(nautilus: nautilus.app.Nautilus) -> None:
	"""Generate game.py with MainClass derived from dfbase.Game if the file not exists."""

	if os.path.exists(f"{nautilus.project.path}/game.py"): return

	nautilus.log(f'Generating "{nautilus.project.mainClass}" on "{nautilus.project.path}/game.py".')

	project = nautilus.project
	content = f"""import dfbase, initials

class {project.mainClass}(dfbase.Game):
	def __init__(self):
		super().__init__(800, 600)

	def init(self):
		initials.runInitials(self)

if __name__ == "__main__":
	game = {project.mainClass}()
	game.run()
	"""

	with open(f"{nautilus.project.path}/game.py", "w") as f:
		f.write(content)

	f.close()

def generateInitials(nautilus: nautilus.app.Nautilus, debug: bool) -> None:

	nautilus.log(f'Generating "{nautilus.project.path}/initials.py".')

	dbgLine = f"game.dictionary.load('{os.getenv('DFPATH')}/templates/dict-debug.xml')" if debug else ""

	content = f"""import dfbase

def runInitials(game: dfbase.Game) -> None:
	{dbgLine}
	game.dictionary.load('dictionary.xml')

	"""
	with open(f"{nautilus.project.path}/initials.py", "w") as f:
		f.write(content)

	f.close()
	