import { Output } from "./output.js";

/** Objeto principal que contiene todo el juego.
 *
 * @export
 * @class Book
 */
export class Book {

	/**
	 * Creates an instance of Book.
	 * @param {string} outputID elemento div que será la pantalla principal del juego.
	 * @memberof Book
	 */
	constructor(outputID) {
		this.title;
		this.author;

		this.dictionary = null;
		this.parser = null;
		Output.init(this, outputID);

		this.properties = {
			"show-parsing-process": false,
			"look-around": "never",
			"hide-title": false,
			"player": "",
			"text-style": {
				fontFamily: 'Georgia, serif',
				fontSize: '14px',
				color: '#333'
			}
		};
	}

	/**
	 * Establece el valor de una propiedad global.
	 *
	 * @param {string} name Nombre de la propiedad.
	 * @param {*} value Valor de la propiedad.
	 * @memberof Book
	 */
	setProperty(name, value) {
		this.properties[name] = value;
	}

	/**
	 * Devuelve el valor de una propiedad global.
	 *
	 * @param {string} name nombre de la propiedad.
	 * @return {*} el valor de la propiedad.
	 * @memberof Book
	 */
	getProperty(name) {
		return this.properties[name];
	}

	/**
	 * Inicializa el juego.
	 *
	 * @memberof Book
	 */
	init() {
		Output.append("Rojo", { color: "red" });
		Output.append("Verde", { color: "green" });
		Output.append("Azúl", { color: "blue" });

		Output.print("Rojo", { color: "red" });
		Output.print("Verde", { color: "green" });
		Output.print("Azúl", { color: "blue" });

		Output.print("Estilo por defecto");
	}

	/**
	 * Inicia la ejecución del juego.
	 *
	 * @memberof Book
	 */
	run() {
		this.init();
	}
}
