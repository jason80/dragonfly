import { DFMLNode } from "../dfml/js/main/node.js";
import { Action } from "./action.js";

export class Condition {
	constructor() {}

	/**
	 *
	 *
	 * @param {Action} action
	 * @return {boolean} 
	 * @abstract
	 * @memberof Condition
	 */
	check(action) {
		return false;
	}

	/**
	 *
	 *
	 * @param {DFMLNode} node
	 * @abstract
	 * @memberof Condition
	 */
	load(node) {

	}
};
