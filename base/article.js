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
		this.female = node.getAttr("genre").getValue() === "famale";
		this.female = node.getAttr("number").getValue() === "plural";
		this.indefinited = node.getAttr("indefinited").getValue() === "true";
	}

}
