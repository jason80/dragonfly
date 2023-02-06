from PyQt5.QtXml import QDomElement

class Article:
	"""Female-Plural representation of the nouns. Can be definited of indefinited
	"""
	def __init__(self) -> None:
		self.__name = ""
		self.__female = False
		self.__plural = False
		self.__indefinited = False

	def __str__(self) -> str:
		return f"{self.name} ({'female' if self.female else 'male'}, {'plural' if self.plural else 'singular'}{', indefinited)' if self.indefinited else ')'}"

	@property
	def name(self) -> str:
		"""Name of the article.
		"""
		return self.__name

	@name.setter
	def name(self, name: str) -> None: self.__name = name

	@property
	def female(self) -> bool:
		"""Return True if the article is female.
		"""
		return self.__female

	@female.setter
	def female(self, female: bool) -> None: self.__female = female

	@property
	def plural(self) -> bool:
		"""Return True if the article is plural.
		"""
		return self.__plural

	@plural.setter
	def plural(self, plural: bool) -> None: self.__plural = plural

	@property
	def indefinited(self) -> bool:
		"""Return True if the article is indefinited.
		"""
		return self.__indefinited

	@indefinited.setter
	def indefinited(self, indefinited: bool) -> None: self.__indefinited = indefinited

	def load(self, element: QDomElement) -> None:
		"""Load the article from xml element.

		Args:
			element (QDomElement): the xml element
		"""
		self.__name = element.attribute("name")
		self.__female = element.attribute("genre") == "female"
		self.__plural = element.attribute("number") == "plural"
		self.__indefinited = element.attribute("indefinited") == "true"
