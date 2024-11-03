import { Output } from "./output.js";
import { Dictionary } from "./dictionary.js";
import { Parser } from "./parser.js";
import { DFMLParser } from "../dfml/js/main/parser.js";
import { DFMLNode } from "../dfml/js/main/node.js";
import { DFMLElement } from "../dfml/js/main/element.js";

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
		this.title = "";
		this.author = "";

		this.player = null;

		this.dictionary = new Dictionary(this);
		this.parser = new Parser(this);
		Output.init(this, outputID);

		this.properties = {
			"show-parsing-process": false,
			"look-around": "always",
			"hide-title": false,
			"player": "",
			"text-style": {
				fontFamily: 'Georgia, serif',
				fontSize: '14px',
				color: '#333'
			},
			"main-title-style": {
				fontFamily: "Georgia, serif",
				fontWeight: "bold",
				fontSize: '20px',
				color: '#252',
				textAlign: 'center'
			},
			"author-style": {
				fontFamily: "Georgia, serif",
				fontSize: '12px',
				color: '#252',
				textAlign: 'center',
				fontStyle: 'italic'
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
	 * Carga un archivo dfml.
	 *
	 * @param {string} path Ruta del archivo a cargar.
	 * @return {Promise} Promesa que se resuelve cuando el archivo ha sido cargado y parseado.
	 * @memberof Book
	 */
	include(path) {
		return fetch(path).then(response => {
			if (!response.ok) {
				throw new Error(`Loading "${path}" failed.`);
			}
			return response.text();
		})
		.then(data => {
			const dfmlParser = new DFMLParser(data);
			
			dfmlParser.parse().forEach(e => {
				if (e.getElementType() === DFMLElement.NODE) {
					if (e.getName() === "book") this.#load(e);
					else if (e.getName() === "dictionary") this.dictionary.load(e);
				}
			});

		}).catch(error => {
			console.error(error);
		});
	}

	/**
	 * Inicia la ejecución del juego.
	 *
	 * @memberof Book
	 */
	run() {
		this.showTitle();

		this.parser.showParsingProcess = this.properties["show-parsing-process"];
		
		if (this.properties["player"] === "") {
			//TODO: ERROR
			return ;
		}

		const plList = this.dictionary.getNouns(this.properties["player"]);
		if (plList.length === 0) {
			// TODO: ERROR
			return ;
		}

		// Sets the player.
		this.player = plList[0];

		if (this.properties["look-around"] === "always" ||
			this.properties["look-around"] === "on-start") {
			const lookVerb = this.dictionary.verbByAction("LookAround");
			this.execute(lookVerb.getName());
		}
	}

	execute(text) {
		this.parser.parse(text);
	}

	showTitle() {
		Output.print(this.title, this.getProperty("main-title-style"));
		Output.print(this.author, this.getProperty("author-style"));
	}

	createInput() {
		const inputContainer = document.createElement('div');
		inputContainer.classList.add('input-line');
	
		const promptSpan = document.createElement('span');
		promptSpan.textContent = '> ';
		
		const input = document.createElement('input');
		input.type = 'text';
		
		inputContainer.appendChild(promptSpan);
		inputContainer.appendChild(input);
		consoleDiv.appendChild(inputContainer);
	
		input.focus();
		
		// Handle user input
		input.addEventListener('keydown', function (event) {
		if (event.key === 'Enter') {
			const userInput = input.value;
			input.disabled = true;
			
			this.handleInput(userInput);
			createInput();
		}
		});
	}

	handleInput(userInput) {
		this.execute(userInput.trim());
	}

	/**
	 * Carga la información del libro desde el nodo dfml.
	 *
	 * @param {DFMLNode} node
	 * @memberof Book
	 */
	#load(node) {
		this.title = node.getAttr("title").getValue();
		this.author = node.getAttr("author").getValue();
	}
}
