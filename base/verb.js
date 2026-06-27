import { Entity } from "./entity.js";

/**
 * Represents the multi-name command wich is associated to Action.
 *
 * @export
 * @class Verb
 * @extends {Entity}
 */
export class Verb extends Entity {
	constructor() {
		super();
		this.action = null;
		this.syntax = [];
		this.responses = {};
	}

	/**
	 * Return the response indicating the if of self. The responses are quieried by the
	 * action associated.
	 *
	 * @param {string} name the response's id.
	 * @return {string} the response.
	 * @memberof Verb
	 */
	getResponse(name) {
		if (name in this.responses) return this.responses[name];
		return "";
	}

	/**
	 * Sets a response. The responses are quieried by the
	 * action associated.
	 *
	 * @param {string} name the response id.
	 * @param {string} str the response message.
	 * @memberof Verb
	 */
	setResponse(name, str) {
		this.responses[name] = str;
	}

	/**
	 * Check if response exists.
	 *
	 * @param {string} id the id of the response.
	 * @return {boolean} True if and only if the verb contains the response.
	 * @memberof Verb
	 */
	hasResponse(id) {
		return id in this.responses;
	}

	/**
	 * Verb string description.
	 * @return {string} string of the entity.
	 *
	 * @memberof Verb 
	 */
	toString() {
		return `Verb: ${super.toString()} [${this.action.constructor.name}]`;
	}
};
