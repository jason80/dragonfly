import { Book } from "./book.js";

import { Node } from "../dfml/js/main/node.js";
import { Article } from "./article.js";
import { Noun } from "./noun.js";

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
	}

	/**
	 * Load the dictionary from dfml document.
	 *
	 * @param {Node} node dfml node.
	 * @memberof Dictionary
	 */
	load(node) {
		if (node.getName() === "article") {
			const article = new Article();
			article.load(node);
			this.articles.push(article);
		} else if (node.getName() === "noun") {
			const noun = new Noun();
			noun.load(node);
			this.nouns.push(noun);
		}
	}
}
