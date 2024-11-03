import { DFMLElement } from "../dfml/js/main/element.js";
import { Article } from "./article.js";
import { Book } from "./book.js";
import { Noun } from "./noun.js";
import { Verb } from "./verb.js";
import { Exit } from "./exit.js";
import { actions } from "./actions.js";

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
		if (name === undefined || name === "") return this.verbs;

		let result = [];
		this.verbs.forEach(v => {
			if (v.responds(name)) result.push(v);
		});

		return result;
	}

	/**
	 * Return a first ocurrence of the verb indicating the action class name.
	 * Action class name must be fully name (module.Class), for otherwise use 'actions'
	 * module by default.
	 *
	 * @param {string} className action class name
	 * @return {Verb} result verb 
	 * @memberof Dictionary
	 */
	verbByAction(className) {
		const actionClass = actions[className];

		if (!actionClass) {
			// TODO: error
		}

		let result = null;

		this.verbs.forEach(v => {
			if (v.action === actionClass) {
				result = v;
			}
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
	 * Returns the exit that match the given name.
	 *
	 * @param {string} name name of the exit.
	 * @return {Exit} the exit.
	 * @memberof Dictionary
	 */
	getExit(name) {
		this.exits.forEach(e => {
			if (e.responds(name)) return e;
		});

		return null;
	}

	getArticle(name) {
		let article = null;

		this.articles.forEach(a => {
			if (a.name === name) article = a;
		});

		return article;
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
					const noun = new Noun(null);
					noun.book = this.book;
					noun.dictionary = this;
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
