from dfexcept import DragonflyException
import typing

import action
import dfbase
import entities
from output.console import Console


class Parser:
	def __init__(self, game: "dfbase.Game") -> None:
		self.__game = game
		self.__showParsingProcess = False

		self.__dObjStr = ""
		self.__iObjStr = ""
		self.__dObj = None
		self.__iObj = None
		self.__keyword = ""

	@property
	def game(self) -> "dfbase.Game":
		return self.__game

	@property
	def showParsingProcess(self) -> bool:
		return self.__showParsingProcess

	@showParsingProcess.setter
	def showParsingProcess(self, val: bool) -> None:
		self.__showParsingProcess = val

	@property
	def dictionary(self) -> "dfbase.Dictionary":
		return self.__game.dictionary

	@property
	def directObjectString(self) -> str:
		return self.__dObjStr

	@property
	def indirectObjectString(self) -> str:
		return self.__iObjStr

	@property
	def directObject(self) -> "entities.Noun":
		return self.__dObj

	@directObject.setter
	def directObject(self, noun: "entities.Noun") -> None:
		self.__dObj = noun

	@property
	def indirectObject(self) -> "entities.Noun":
		return self.__iObj

	@indirectObject.setter
	def indirectObject(self, noun: "entities.Noun") -> None:
		self.__iObj = noun

	@property
	def keyword(self) -> str:
		return self.__keyword

	def parse(self, line: str) -> None:

		# Gets tokens
		separated = line.strip().split(" ")
		tokens = []
		for t in separated:
			t = t.strip()
			if t: tokens.append(t)
		
		# Empty line
		if not tokens:
			self.debug("token list is empty.")
			return None

		# Filter the verbs
		verbs = self.dictionary.verbs(tokens[0])

		# Verb not found
		if not verbs:
			self.debug("verbs not found.")
			
			# Check if the token is an exit
			exit = self.dictionary.exit(line.strip())
			if exit:
				self.debug(f'exit: "{exit.name}" found.')
				# Get the verb associated to GoTo action
				gotoVerb = self.dictionary.verbByAction("GoTo")
				self.__dObjStr = line.strip()
				self.__iObjStr = ""

				# Instantiate the GoTo action
				action = gotoVerb.action()
				action.verb = gotoVerb
				action.game = self.game

				# Execute
				self.debug(f'calling GoTo action on exit: "{self.__dObjStr}".')
				action.execute()
				
			else:
				self.debug("exit not found.")
				self.parse("?")
			return None

		self.debug(f"for {tokens[0]}, {len(verbs)} verb(s) found, checking syntax ...")

		action = None

		# Checks the verbs syntaxs
		for v in verbs:
			# Clear objects string
			self.__dObjStr = ""
			self.__iObjStr = ""
			self.__keyword = ""

			action = self.checkSyntax(v, tokens)
			if action: break # Syntax not match

		if not action:
			self.debug(f'syntax check fails: "{tokens[0]}".')

			# Print syntax fail response on first verb (print response)
			response = verbs[0].getResponse("syntax-fail").strip()
			if response:
				Console.println(response)
			else:
				self.game.execute("?")


			return None

		# Clean articles from object strings
		self.__dObjStr = self.cleanArticles(self.__dObjStr)
		self.__iObjStr = self.cleanArticles(self.__iObjStr)

		self.debug(f'executing action: "{action.__class__}".')

		# Debug: show the parameters
		if self.__showParsingProcess:
			if self.__dObjStr:
				msg = f"Params 1={self.__dObjStr}"
				if self.__iObjStr:
					msg += f", 2={self.__iObjStr}."
				self.debug(msg)

		action.execute()


	def checkSyntax(self, verb: "entities.Verb", tokens: typing.List[str]) -> "action.Action":
		# Instantiate the verb's action
		actionClass = verb.action
		action = actionClass()
		action.game = self.__game
		action.verb = verb

		syntax = verb.syntax

		# CASE 0
		#TODO: multiparameter verb
		if syntax:
			if syntax[-1] == "...":
				pass

		# CASE 1: Verb without parameters
		if not syntax:
			if len(tokens) > 1: return None
			return action

		# CASE 2: Wait for direct object
		if len(syntax) == 1:
			if syntax[0] == "1":
				# Token is only the verb ...
				if len(tokens) == 1:
					# Requires a direct object
					return None
				
				# Exclude the verb
				self.__dObjStr = " ".join(tokens[1:])
				return action
			else:
				raise DragonflyException(f"Syntax error on verb: {verb.name}.")

		# CASE 3: Wait keyword and direct object
		if len(syntax) == 2:
			if syntax[0] == "1" or syntax[0] == "2":
				raise DragonflyException(f"Syntax error on verb: {verb.name}.")

			if syntax[1] == "1":
				if len(tokens) <= 1: return None

				# Check the keyword
				if self.checkKeyword(tokens[1], syntax[0]):
					self.__keyword = tokens[1]
					self.__dObjStr = " ".join(tokens[2:])
					return action
				else:
					# Keyword not found
					return None

			else:
				raise DragonflyException(f"Syntax error on verb: {verb.name}.")

		# CASE 4: Wait for 3 things
		if len(syntax) == 3:
			# CASE 4A: Object, keyword, object
			if syntax[1] != "1" and syntax[1] != "2":
				if (syntax[0] == "1" and syntax[2] == "2") or (syntax[0] == "2" and syntax[2] == "1"):
					# Read the first object until the keyword
					ti = 1
					while ti < len(tokens) and not self.checkKeyword(tokens[ti], syntax[1]):
						if syntax[0] == "1":
							self.__dObjStr += tokens[ti] + " "
						else:
							self.__iObjStr += tokens[ti] + " "
						ti += 1

					# Keyword not found
					if ti >= len(tokens): return None

					# Set the keyword
					self.__keyword = tokens[ti]

					# Now, search for the other object
					ti += 1
					while ti < len(tokens):
						if syntax[2] == "1":
							self.__dObjStr += tokens[ti] + " "
						else:
							self.__iObjStr += tokens[ti] + " "
						ti += 1

					# If the object is null
					if syntax[2] == "1":
						if not self.__dObjStr: return None
					else:
						if not self.__iObjStr: return None

					# Ok
					return action
				else:
					raise DragonflyException(f"Syntax error on verb: {verb.name}.")

			# CASE 4B: Keyword, object, object
			if syntax[0] != "1" and syntax[1] != "2":
				# Expected keyword first
				if not self.checkKeyword(tokens[1], syntax[0]):
					return None

				# Search for the first object until an article definited in dictionary
				ti = 2
				while ti < len(tokens) and not self.game.dictionary.article(tokens[ti]):
					if syntax[1] == "1":
						self.__dObjStr += tokens[ti] + " "
					else:
						self.__iObjStr += tokens[ti] + " "

					ti += 1

				# Article not found
				if (ti >= len(tokens)): return None

				# Search for the second object
				while ti < len(tokens):
					if syntax[2] == "1":
						self.__dObjStr += tokens[ti] + " "
					else:
						self.__iObjStr += tokens[ti] + " "

					ti += 1

				# OK
				self.__keyword = tokens[1]
				return action

			
	def checkKeyword(self, keyword: str, kwList: str) -> bool:
		return keyword in kwList.split("/")

	def cleanArticles(self, obj: str) -> str:
		result = []
		words = obj.split(" ")
		for w in words:
			if self.game.dictionary.article(w): continue
			result.append(w)

		return " ".join(result)

	def debug(self, msg: str) -> None:
		if self.__showParsingProcess:
			Console.println(f"Parser: {msg}", "family: 'Courier'")
