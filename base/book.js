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
		this.version = ""; // Any format
		this.description = "";
		this.genre = "Adventure";
		this.year = 0;
		this.language = ""; // en, es, fr, etc.
		this.storyLength = "Medium"; // Tiny, Short, Medium, Long, Huge
		this.parental = 0; // 0 = All

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
			"text-style": "class:df-default-text",
			"prompt-style": "class:df-prompt",
			"input-style": "class:df-input",
			"main-title-style": "class:df-main-title",
			"author-style": "class:df-author",
			"place-title-style": "class:df-place-title",
			"tip-style": "class:df-tip",
			"theme": "style/dragonfly-light.css"
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

		// Load theme
		Utils.loadCSS(this.properties["theme"]);

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

		if (node.hasAttr("version"))
			this.version = node.getAttr("version").getValue();

		if (node.hasAttr("genre"))
			this.genre = node.getAttr("genre").getValue();

		if (node.hasAttr("year"))
			this.year = node.getAttr("year").getValue();

		if (node.hasAttr("language"))
			this.language = node.getAttr("language").getValue();

		if (node.hasAttr("story-length")) {
			const names = ["Tiny", "Short", "Medium", "Long", "Huge"];
			this.storyLength = node.getAttr("story-length").getValue();

			if (names.includes(this.storyLength) === false) {
				Output.error(`Book Review: Invalid story length: ${this.storyLength}`);
				Output.error("Expected Tiny, Short, Medium, Long or Huge.");
				this.storyLength = "Medium";
			}
		}

		if (node.hasAttr("parental")) {
			const n = parseInt(node.getAttr("parental").getValue(), 10);
			if (Number.isNaN(n)) {
				Output.error(`Book Review: Invalid parental: ${node.getAttr("parental").getValue()}`);
				Output.error("Expected a number.");
			} else {
				this.parental = n;
			}
		}

		for (const child of node.children) {
			if (child.getElementType() === DFMLElement.NODE) {

				if (child.getName() === "description") {

					let error = false;

					if (child.children.length > 1) error = true;
					if (child.children.length === 1) {
						if (child.children[0].getElementType() !== DFMLElement.DATA) {
							error = true;
						} else {
							if (child.children[0].getValue().getType() !== DFMLValue.STRING) error = true;
						}
					}

					if (error) {
						Output.error("Book Review: Invalid description node.");
					} else {
						this.description = child.children[0].getValue().getValue();
					}
				}

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
