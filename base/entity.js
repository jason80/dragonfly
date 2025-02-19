import { Utils } from "./utils.js"

/**
 * Base of the nouns, verbs and exits.
	Contains the multi-name property, and game and dictionary instances.
 *
 * @export
 * @class Entity
 */
export class Entity {
	/**
	 * Creates an instance of Entity.
	 * @memberof Entity
	 */
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

		for (const n of this.names) {
			if (Utils.isEquals(n, name)) return true;
		}

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

		if (!Utils.expectedAttributes(node, "names")) return ;

		this.names = [];
		node.getAttr("names").getValue().split(',').forEach(n => {
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
