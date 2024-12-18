
export class Utils {
	/**
	 * Returns the 'text' without the accents for sentence comparison.
	 * (previously normalized NFC).
	 * 
	 *
	 * @static
	 * @param {string} text tarjet text.
	 * @return {string} text with no acents.
	 * @memberof Utils
	 */
	static noAccents(text) {
		// 
		let copy = '';
		text = text.normalize('NFC');
	
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
  
	/**
	 * Compare both texts regardless of accentuation.
	 *
	 * @static
	 * @param {string} text1 text1.
	 * @param {string} text2 text2.
	 * @return {boolean} true if both texts are equal.
	 * @memberof Utils
	 */
	static isEquals(text1, text2) {
		return Utils.noAccents(
			text1.trim().toLowerCase()
		) === 
		Utils.noAccents(
			text2.trim().toLowerCase()
		);
	}
}
