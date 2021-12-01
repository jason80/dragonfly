def noAccents(text: str) -> str:
	copy = ""

	for c in text:
		if c == '\u00E0' or c == '\u00E1' or c == '\u00E2' or c == '\u00E3' or c == '\u00E4' or c == '\u00E5':
			copy += "a"
		elif c == '\u00E8' or c == '\u00E9' or c == '\u00EA' or c == '\u00EB':
			copy += "e"
		elif c == '\u00EC' or c == '\u00ED' or c == '\u00EE' or c == '\u00EF':
			copy += "i"
		elif c == '\u00F2' or c == '\u00F3' or c == '\u00F4' or c == '\u00F5' or c == '\u00F6':
			copy += "o"
		elif c == '\u00F9' or c == '\u00FA' or c == '\u00FB' or c == '\u00FC':
			copy += "u"
		elif c == '\u00F1':
			copy += "n"
		else: copy += c

	return copy

def isEquals(text1: str, text2: str) -> bool:
	return noAccents(text1.strip().lower()) == noAccents(text2.strip().lower())