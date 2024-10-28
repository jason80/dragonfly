import { DFMLNode } from "../dfml/js/main/node.js";
import { DFMLValue } from "../dfml/js/main/value.js"

/**
 * Female-Plural representation of the nouns. Can be definited of indefinited
 *
 * @export
 * @class Article
 */
export class Article {

	/**
	 * Creates an instance of Article.
	 * @memberof Article
	 */
	constructor() {
		this.name = "";
		this.female = false;
		this.plural = false;
		this.indefinited = false;
	}

	/**
	 * Load the article from dfml element.
	 *
	 * @param {DFMLNode} node the dfml node.
	 * @memberof Article
	 */
	load(node) {
		this.name = node.getAttr("name").getValue();
		this.female = node.getAttr("genre").getValue() === "female";
		this.plural = node.getAttr("number").getValue() === "plural";
		this.indefinited = node.getAttr("indefinited").getValue() === "true";
	}

	/**
	 * Article string description.
	 * @return {string} string of the entity.
	 *
	 * @memberof Article 
	 */
	toString() {
		return `Article: ${this.name} ${this.female ? "'female'" : "'male'"} ${this.plural ? "'plural'" : "'singular'"} ${this.indefinited ? "'indefinited'" : "'definited'"}`;
	}

}
