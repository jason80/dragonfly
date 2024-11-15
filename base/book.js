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

		this.includeFiles = [];

		this.properties = {
			"show-parsing-process": false,
			"look-around": "always",
			"hide-title": false,
			"player": "",
			"prompt": "> ",
			"text-style": {
				fontFamily: 'Georgia, serif',
				fontSize: '14px',
				color: '#333'
			},
			"prompt-style": {
				fontFamily: 'Georgia, serif',
				fontSize: '14px',
				color: '#731',
			},
			"input-style": {
				fontFamily: 'Georgia, serif',
				fontSize: '14px',
				color: '#731',
				border: "None",
				outline: "None",
				flex: "1"
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
			},
			"place-title-style": {
				fontFamily: "Georgia, serif",
				fontWeight: "bold",
				fontSize: '14px',
				color: '#505'
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
	 * Add a dfml path to include list.
	 *
	 * @param {string} path path to dfml file.
	 * @memberof Book
	 */
	include(path) {
		this.includeFiles.push(path);
	}

	/**
	 * Loads a DFMLFile
	 *
	 * @param {string} path Path to DFML file.
	 * @return {Promise} Return a promise.
	 * @memberof Book
	 */
	#loadDFMLFile(path) {
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
	async run() {

		// Include files
		for (const i of this.includeFiles) {
			await this.#loadDFMLFile(i);
		};

		if (this.title.trim() === "") {
			Output.error("the book title has not been defined");
			return ;
		}

		if (this.author.trim() === "") {
			Output.error("the book's author has not been defined");
			return ;
		}

		if (!this.getProperty("hide-title"))
			this.showTitle();

		this.parser.showParsingProcess = this.properties["show-parsing-process"];
		
		if (this.properties["player"].trim() === "") {
			Output.error("the player is not declared");
			return ;
		}

		const plList = this.dictionary.getNouns(this.properties["player"]);
		if (plList.length === 0) {
			Output.error(`player "${this.properties['player']}" not found in dictionary`);
			return ;
		}

		// Sets the player.
		this.player = plList[0];

		if (this.properties["look-around"] === "always" ||
			this.properties["look-around"] === "on-start") {
			const lookVerb = this.dictionary.verbByAction("LookAround");
			this.execute(lookVerb.getName());
		}

		this.createInput();
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
		Object.assign(inputContainer.style, {
			display: "inline-flex",
			width: "100%",
			alignItems: "center"
		});
	
		const promptSpan = document.createElement('span');
		Object.assign(promptSpan.style, this.getProperty("prompt-style"));
		promptSpan.textContent = this.getProperty("prompt");
		
		const input = document.createElement('input');
		input.type = 'text';
		Object.assign(input.style, this.getProperty("input-style"));
		
		inputContainer.appendChild(promptSpan);
		inputContainer.appendChild(input);
		Output.outputDiv.appendChild(inputContainer);
	
		input.focus();
		
		// Handle user input
		input.addEventListener('keydown', (event) => {
		if (event.key === 'Enter') {
			const userInput = input.value;
			input.disabled = true;
			
			this.handleInput(userInput);
			this.createInput();
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
