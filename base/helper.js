
export class Helper {
	static noAccents(text) {
		// Returns the 'text' without the accents for sentence comparison.
		let copy = '';
	
		for (let i = 0; i < text.length; i++) {
			let c = text[i];
			if (c === '\u00E0' || c === '\u00E1' || c === '\u00E2' || c === '\u00E3' || c === '\u00E4' || c === '\u00E5') {
				copy += 'a';
			} else if (c === '\u00E8' || c === '\u00E9' || c === '\u00EA' || c === '\u00EB') {
				copy += 'e';
			} else if (c === '\u00EC' || c === '\u00ED' || c === '\u00EE' || c === '\u00EF') {
				copy += 'i';
			} else if (c === '\u00F2' || c === '\u00F3' || c === '\u00F4' || c === '\u00F5' || c === '\u00F6') {
				copy += 'o';
			} else if (c === '\u00F9' || c === '\u00FA' || c === '\u00FB' || c === '\u00FC') {
				copy += 'u';
			} else if (c === '\u00F1') {
				copy += 'n';
			} else {
				copy += c;
			}
		}
	
		return copy;
	}
  
	static isEquals(text1, text2) {
		// Compare both texts regardless of accentuation.
		return Helper.noAccents(text1.trim().toLowerCase()) === Helper.noAccents(text2.trim().toLowerCase());
	}
}
