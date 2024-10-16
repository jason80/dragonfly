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
		p.textContent = message;

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
			span.textContent = " " + message;

			Output.#applyStyle(span, style);
			
			lastP.appendChild(span);
		} else {
			Output.print(message, style);
		}
	
		Output.outputDiv.scrollTop = Output.outputDiv.scrollHeight;
	}
}
