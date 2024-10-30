import { DFMLNode } from "../dfml/js/main/node.js";
import { Action } from "./action.js";

export class ActionResponse {
	constructor() { }

	/**
	 *
	 *
	 * @param {Action} action
	 * @abstract
	 * @memberof ActionResponse
	 */
	execute(action) {}

	/**
	 *
	 *
	 * @param {DFMLNode} node
	 * @abstract
	 * @memberof ActionResponse
	 */
	load(node) {}
};
