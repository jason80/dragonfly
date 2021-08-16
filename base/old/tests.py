from test_game import TestGame
import unittest


class DictionaryTests(unittest.TestCase):
	def __init__(self, methodName: str) -> None:
		super().__init__(methodName=methodName)
		self.game = TestGame()
		self.game.init()
		self.dict = self.game.dictionary

	def testGetNouns(self):
		nouns = self.dict.nouns("chest")
		self.assertEqual(len(nouns), 1)
		self.assertEqual(nouns[0].name, "chest")

		doors = self.dict.nouns("door")
		self.assertEqual(len(doors), 2)

	def testGetVerbs(self):
		verbs = self.dict.verbs("cut")
		self.assertEqual(len(verbs), 2)
		verbs = self.dict.verbs("jump")
		self.assertEqual(len(verbs), 1)

		self.assertEqual(verbs[0].name, "jump")

	def testContains(self):
		nouns = self.dict.nouns("chest")
		self.assertTrue(nouns[0].contains("vase"))

	def testAttributes(self):
		nouns = self.dict.nouns("keys")
		self.assertTrue(nouns[0].isSet("female"))
		self.assertTrue(nouns[0].isSet("plural"))
		self.assertFalse(nouns[0].isSet("countless"))

	def testVariables(self):
		nouns = self.dict.nouns("coffer")
		self.assertEqual(nouns[0].getVariable("closed"), "yes")

	def testArticles(self):
		article = self.dict.article("el")
		self.assertEqual("el", article.name)
		self.assertFalse(article.female)
		self.assertFalse(article.plural)
		self.assertFalse(article.indefinited)

		article = self.dict.article("una")
		self.assertTrue(article.female)
		self.assertFalse(article.plural)
		self.assertTrue(article.indefinited)


if __name__ == "__main__":
	unittest.main()
