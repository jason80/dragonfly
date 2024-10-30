import { DFMLNode } from "../dfml/js/main/node.js";
import { DFMLValue } from "../dfml/js/main/value.js";

/**
 * Base of the nouns, verbs and exits.
	Contains the multi-name property, and game and dictionary instances.
 *
 * @export
 * @class Entity
 */
export class Entity {
	constructor() {
		this.names = [];
		this.book = null;
		this.dictionary = null;
	}

	/**
	 * Returns true if the entity responds to the name.
	 *
	 * @param {string} name name to compare.
	 * @return {boolean} true if the entity responds to the name.
	 * @memberof Entity
	 */
	responds(name) {
		this.names.forEach(n => {
			if (n, name) return true;
			// TODO: helper isEquals(s1, s2)
		});

		return false;
	}

	/**
	 * Returns the first name of the multiname property
	 *
	 * @return {string} the first name of the entity 
	 * @memberof Entity
	 */
	getName() {
		if (this.names.length === 0) return "";
		return this.names[0];
	}

	/**
	 * Add a new name at top of the list of names if it not responds to the name.
	 *
	 * @param {string} name name to add to list.
	 * @memberof Entity
	 */
	appendName(name) {
		if (!this.responds(name))
			this.names.unshift(name);
	}

	/**
	 * Load the entity from xml element.
	 *
	 * @param {Node} node
	 * @memberof Entity
	 */
	load(node) {
		this.names = [];
		node.getAttr("names").getValue().split().forEach(n => {
			this.names.push(n.trim());
		});
	}

	/**
	 * Entity string description.
	 *
	 * @return {string} string of the entity.
	 * @memberof Entity
	 */
	toString() {
		return this.names.toString();
	}
}
