import { DFMLNode } from "../dfml/js/main/node.js";

/** Represents an exit and a destiny association for add to place.
 *
 * @export
 * @class Connection
 */
export class Connection {
	/**
	 * Creates an instance of Connection.
	 * @memberof Connection
	 */
	constructor() {
		this.exit = "";
		this.destiny = "";
	}

	toString() {
		return `${this.exit} --> ${this.destiny}`;
	}
	
	/**
	 * Loads a connection from dfml node.
	 *
	 * @param {DFMLNode} node the connection dfml node.
	 * @memberof Connection
	 */
	load(node) {
		this.exit = node.getAttr("exit").getValue();
		this.destiny = node.getAttr("destiny").getValue();
	}
};
