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
	 * @param {string} output
	 * @memberof Output
	 */
	static init(output) {
		Output.outputDiv = document.getElementById(output);
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

		if (style !== undefined) {
			if (typeof style === "object") {
				Object.assign(p.style, style);  // Aplica estilos en línea
			} else {
				p.className = style;
			}
		}

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

			if (style !== undefined) {
		
				if (typeof style === "object") {
					Object.assign(span.style, style);
				} else {
					span.className = style;
				}

			}
			
			lastP.appendChild(span);
		} else {
			Output.print(message, style);
		}
	
		Output.outputDiv.scrollTop = Output.outputDiv.scrollHeight;
	}
}
