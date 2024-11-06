import { Book } from "./book.js";

/**
 * Control de la salida del juego.
 *
 * @export
 * @class Output
 */
export class Output {

	/**
	 * Inicializa la salida con el div que la representa.
	 *
	 * @static
	 * @param {Book} book Instancia del juego actual.
	 * @param {string} output Salida principal del juego.
	 * @memberof Output
	 */
	static init(book, output) {
		Output.outputDiv = document.getElementById(output);
		Output.book = book;
	}

	/**
	 *
	 *
	 * @static Aplica el estilo al elemento dado.
	 * @param {*} element elemento a aplicar el estilo.
	 * @param {*} style estilo a aplicar.
	 * @memberof Output
	 */
	static #applyStyle(element, style) {

		const defStyle = Output.book.getProperty("text-style");
		if (defStyle !== undefined) {
			if (typeof defStyle === "object") {
				Object.assign(element.style, defStyle);
			} else {
				element.className = defStyle;
			}
		}
		if (style !== undefined) {
			if (typeof style === "object") {
				Object.assign(element.style, style);
			} else {
				element.className = style;
			}
		}
	}

	/**
	 * Imprime un mensaje en la pantalla.
	 *
	 * @static
	 * @param {string} message Cadena a imprimir.
	 * @param {*} style Estilo del texto en css.
	 * @memberof Output
	 */
	static print(message, style) {

		const p = document.createElement('p');
		p.textContent = this.replaceObjects(message);

		Output.#applyStyle(p, style);

		Output.outputDiv.appendChild(p);
		Output.outputDiv.scrollTop = Output.outputDiv.scrollHeight; // Desplazar hacia abajo
	}

	/**
	 * Agrega texto al útimo párrafo.
	 *
	 * @static
	 * @param {string} message
	 * @param {*} style
	 * @memberof Output
	 */
	static append(message, style) {
		const lastP = Output.outputDiv.lastChild;

		// Si existe un <p>, agregar un nuevo nodo de texto al final
		if (lastP && lastP.tagName === 'P') {
			
			const span = document.createElement('span');
			span.textContent = " " + Output.replaceObjects(message);

			Output.#applyStyle(span, style);
			
			lastP.appendChild(span);
		} else {
			Output.print(message, style);
		}
	
		Output.outputDiv.scrollTop = Output.outputDiv.scrollHeight;
	}

	static error(message) {
		Output.print(`[Dragonfly Error] ${message}`, {
			color: 'white',
			background: 'darkred',
  			fontFamily: 'monospace'
		});
	}

	/**
	 * Replace the special commands with the objects.
	 * 
	 * Special commands:
	 * #: definite article ("the")
	 * %: indefinite article ("a")
	 * 1: direct object
	 * 2: indirect object
	 * 3: parameters
	 * ^: capitalize
	 * 
	 * Examples:
	 * "#1" --> "the table"
	 * "%1" --> "a chair"
	 * "#^1" --> "The chair"
	 * 
	 * Special commands 2:
	 * @: replace with a specified text form
	 * Format: (a,b,c,d) where:
	 * - a: singular male
	 * - b: singular female
	 * - c: plural male
	 * - d: plural female
	 * 
	 * Examples:
	 * "#^1 @1(is,is,are,are) in the box" --> "The ball is in the box"
	 * (assuming "the ball" is male plural)
	 *
	 * @param {string} text The text to process and replace.
	 * @return {string} The resulting text with replacements.
	 * @memberof Output
	 */
	static replaceObjects(text) {
		let result = "";
		let i = 0;

		while (i < text.length) {
			let ch = text[i];

			if (ch === "#" || ch === "%" || ch === "@") {
				let obj = null;
				let capitalize = false;
				i++;

				// Check if we need to capitalize the result
				if (text[i] === "^") {
					capitalize = true;
					i++;
				}

				// Determine the object type
				if (text[i] === "1") {
					obj = this.book.parser.directObject;
				} else if (text[i] === "2") {
					obj = this.book.parser.indirectObject;
				} else if (text[i] === "3") {
					result += this.book.parser.parameters;
					i++;
					continue;
				}

				if (!obj) {
					result += "(NONE)";
				} else {
					let objName = null;

					if (ch === "%") {
						objName = obj.a(); // Indefinite article
					} else if (ch === "#") {
						objName = obj.the(); // Definite article
					} else if (ch === "@") {
						i ++;
						if (text[i] === "(") {
							i ++;
							let params = "";
							while (i < text.length) {
								if (text[i] === ")") {
									result += this.replaceGenderNumber(obj, params, capitalize);
									break;
								}
								params += text[i];
								i ++;
							}
							i ++;
							continue;
						} else {
							Output.error('Outuput: expected character "(" after @.');
						}
					}

					// Apply capitalization if required
					if (capitalize) {
						result += objName.charAt(0).toUpperCase() + objName.slice(1);
					} else {
						result += objName;
					}
				}
			} else {
				result += ch;
			}
			i ++;
		}

		return result;
	}
	
	/**
	 * Selects the parameter based on the gender and number of the noun.
	 *
	 * @param {Noun} obj The noun object with gender and number information.
	 * @param {string} params Comma-separated list of forms (e.g., "is,is,are,are").
	 * @param {boolean} capitalize If true, capitalizes the selected form.
	 * @return {string} The text form that matches the noun's gender and number.
	 * @memberof Output
	 */
	static replaceGenderNumber(obj, params, capitalize) {
		const members = params.split(",");
		if (members.length !== 4) {
			Output.error("Console: expected 4 parameters after @.");
		}

		let result = "";
		if (!obj.isSet("female") && !obj.isSet("plural")) {
			result = members[0]; // Singular male
		} else if (obj.isSet("female") && !obj.isSet("plural")) {
			result = members[1]; // Singular female
		} else if (!obj.isSet("female") && obj.isSet("plural")) {
			result = members[2]; // Plural male
		} else if (obj.isSet("female") && obj.isSet("plural")) {
			result = members[3]; // Plural female
		}

		// Apply capitalization if needed
		return capitalize ? result.charAt(0).toUpperCase() + result.slice(1) : result;
	}
}
