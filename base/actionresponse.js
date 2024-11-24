/**
 * An ActionResponse is a component that changes the behavior of a Noun. They are 
 * added to ActionEvents and executed when the event's action and conditions are met.
 *
 */

import { DFMLNode } from "../dfml/js/main/node.js";
import { Action } from "./action.js";

/**
 * Base class representing an action response. When the action matches the event
 * and the conditions are met, the ActionResponse is executed.
 *
 * @export
 * @class ActionResponse
 */
export class ActionResponse {
	/**
	 * Creates an instance of ActionResponse.
	 * @memberof ActionResponse
	 */
	constructor() { }

	/**
	 * Executes the ActionResponse. This method is called by the event when
	 * the requirements are met.
	 *
	 * @param {Action} action Current action
	 * @abstract
	 * @memberof ActionResponse
	 */
	async execute(action) {}

	/**
	 * Loads the ActionResponse from a DFML node.
	 *
	 * @param {DFMLNode} node DFML node.
	 * @abstract
	 * @memberof ActionResponse
	 */
	load(node) {}
};
