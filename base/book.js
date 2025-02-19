import { Output } from "./output.js";
import { Input } from "./input.js";
import { Dictionary } from "./dictionary.js";
import { Parser } from "./parser.js";
import { DFMLParser } from "../dfml/js/main/parser.js";
import { DFMLNode } from "../dfml/js/main/node.js";
import { DFMLElement } from "../dfml/js/main/element.js";
import { Help } from "./help.js";
import { DFMLValue } from "../dfml/js/main/value.js";
import { DFMLPersistenceSystem } from "./persistence.js";
import { Utils } from "./utils.js";

/** Main object which contains all of the game.
 *
 * @export
 * @class Book
 */
export class Book {

	/**
	 * Creates an instance of Book.
	 * @param {string} outputID div element will be the main screen of the game.
	 * @param {string} initialDFMLFile include initial dfml file
	 * @memberof Book
	 */
	constructor(outputID, initialDFMLFile = "") {
		this.title = "";
		this.author = "";

		this.player = null;

		this.dictionary = new Dictionary(this);
		this.parser = new Parser(this);
		Output.init(this, outputID);
		Help.book = this;

		this.input = new Input(this);

		this.includeFiles = [];

		this.properties = {
			"show-parsing-process": false,
			"look-around": "always",
			"hide-title": false,
			"parser-clean": "-_#$@&+*;/",
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
			},
			"tip-style": {
				fontFamily: "Georgia, serif",
				fontSize: "14px",
				fontStyle: "italic",
				color: "#A30"
			}
		};

		this.initialState = "";

		if (initialDFMLFile !== "") this.include(initialDFMLFile);
	}

	/**
	 * Sets the property value.
	 *
	 * @param {string} name name of the property.
	 * @param {*} value value of the property.
	 * @memberof Book
	 */
	setProperty(name, value) {
		this.properties[name] = value;
	}

	/**
	 * Gets the value of the property.
	 *
	 * @param {string} name name of the property.
	 * @return {*} el value of the property.
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
			const dfmlParser = new DFMLParser(data, path);
			
			try {

				dfmlParser.parse().forEach(e => {
					if (e.getElementType() === DFMLElement.NODE) {
						if (e.getName() === "book") this.#load(e);
						else if (e.getName() === "dictionary") this.dictionary.load(e);
					}
				});

			} catch(e) {
				Output.error(e);
			}

		}).catch(error => {
			console.error(error);
		});
	}

	/**
	 * Runs the game.
	 *
	 * @memberof Book
	 */
	async run() {

		// Ever focus last input created
		document.addEventListener("click", () => {
			const enabledInput = document.querySelector("input:enabled");
			if (enabledInput) {
				enabledInput.focus();
			}
		});

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
			if (lookVerb)
				await this.execute(lookVerb.getName());
			else
				Output.error("Possible missing dictionary template?");
		}

		// Initial save state
		const p = new DFMLPersistenceSystem(this.dictionary);
		this.initialState = p.save();

		await this.input.createInput();
	}

	/**
	 * Execute a sentence.
	 *
	 * @param {string} text sentence to execute.
	 * @memberof Book
	 */
	async execute(text) {
		await this.parser.parse(text);
	}

	/**
	 * Show the book title and the author.
	 */
	showTitle() {
		Output.print(this.title, this.getProperty("main-title-style"));
		Output.print(this.author, this.getProperty("author-style"));
	}

	restart() {
		const p = new DFMLPersistenceSystem(this.dictionary);
		p.load(this.dictionary.book.initialState);
	}

	/**
	 * Loads the book info from dfml node.
	 *
	 * @param {DFMLNode} node
	 * @memberof Book
	 */
	#load(node) {
		if (node.hasAttr("title"))
			this.title = node.getAttr("title").getValue();

		if (node.hasAttr("author"))
			this.author = node.getAttr("author").getValue();

		for (const child of node.children) {
			if (child.getElementType() === DFMLElement.NODE) {
				if (child.getName() === "property") {

					if (!Utils.expectedAttributes(child, "name", "value")) continue;

					const name = child.getAttr("name").getValue();
					const value = child.getAttr("value");

					if (value.getType() === DFMLValue.STRING) {
						this.setProperty(name, value.getValue());
					} else if (value.getType() === DFMLValue.BOOLEAN) {
						this.setProperty(name, value.getValue() === "true");
					}
				}

				if (child.getName() === "include") {

					Utils.expectedAttributes(child, "src");

					this.include(child.getAttr("src").getValue());
				}
			}
		}
	}
}
