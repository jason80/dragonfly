import { Entity } from "./entity.js";
import { actions } from "./actions.js";
import { debugActions } from "./debug.js";
import { Output } from "./output.js";

import { DFMLNode } from "../dfml/js/main/node.js";
import { DFMLElement } from "../dfml/js/main/element.js";

import { Utils } from "./utils.js";

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
	 * Load verb from dfml node.
	 *
	 * @param {DFMLNode} node
	 * @memberof Verb
	 */
	load(node) {
		super.load(node);

		if (!Utils.expectedAttributes(node, "action")) return ;

		const actionClassName = node.getAttr("action").getValue();
		let actionClass = actions[actionClassName];

		if (!actionClass) {
			actionClass = debugActions[actionClassName];
		}

		if (!actionClass) {
			Output.error(`action class "${actionClassName}" not exists.`);
		} else {
			this.action = actionClass;
			this.action.book = this.book;
			this.action.verb = this;
		}

		if (node.hasAttr("syntax")) {
			node.getAttr("syntax").getValue().split(',').forEach(n => {
				this.syntax.push(n.trim());
			});
		}

		// Responses
		node.children.forEach((e) => {
			if (e.getElementType() === DFMLElement.NODE) {
				if (e.getName() === "response") {

					if (!Utils.expectedAttributes(e, "id", "string")) return ;

					this.setResponse(e.getAttr("id").getValue(), 
					e.getAttr("string").getValue());
				}
			}
		});

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
