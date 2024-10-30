import { DFMLElement } from "../dfml/js/main/element.js";
import { Article } from "./article.js";
import { Book } from "./book.js";
import { Noun } from "./noun.js";
import { Verb } from "./verb.js";
import { Exit } from "./exit.js";

/**
 * Contains a list of nouns, verbs and exits.
 *
 * @export
 * @class Dictionary
 */
export class Dictionary {
	/**
	 * Creates an instance of Dictionary.
	 * @param {Book} book the book instance.
	 * @memberof Dictionary
	 */
	constructor(book) {
		this.book = book;

		this.articles = [];
		this.nouns = [];
		this.verbs = [];
		this.exits = [];
	}

	/**
	 * Returns the verbs that match the given name. 
	 * If the name is empty, returns all of them.
	 *
	 * @param {string} [name=""] name of the verb.
	 * @return {Array.<Verb>} list of verbs.
	 * @memberof Dictionary
	 */
	getVerbs(name = "") {
		if (name === "") return this.verbs;

		let result = [];
		this.verbs.forEach(v => {
			if (v.responds(name)) result.push(v);
		});

		return result;
	}

	/**
	 * Returns the nouns that match the given name. 
	 * If the name is empty, returns all of them.
	 *
	 * @param {string} [name=""] name of the noun.
	 * @return {Array.<Noun>} list of nouns.
	 * @memberof Dictionary
	 */
	getNouns(name = "") {
		if (name === "") return this.nouns;

		let result = [];
		this.nouns.forEach(n => {
			if (n.responds(name)) result.push(n);
		});

		return result;
	}

	/**
	 * Load the dictionary from dfml document.
	 *
	 * @param {Node} node dfml node.
	 * @memberof Dictionary
	 */
	load(node) {

		node.children.forEach((child) => {
			if (child.getElementType() === DFMLElement.NODE) {
				if (child.getName() === "noun") {
					const noun = new Noun();
					noun.load(child);
					this.nouns.push(noun);
				} else if(child.getName() === "verb") {
					const verb = new Verb();
					verb.load(child);
					this.verbs.push(verb);
				} else if (child.getName() === "article") {
					const article = new Article();
					article.load(child);
					this.articles.push(article);
				} else if (child.getName() === "exit") {
					const exit = new Exit();
					exit.load(child);
					this.exits.push(exit);
				}
			}
		});

	}
}
