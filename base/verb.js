import { Entity } from "./entity.js";
import { DFMLNode } from "../dfml/js/main/node.js";
import { actions } from "./actions.js";

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
	 * Load verb from dfml node.
	 *
	 * @param {DFMLNode} node
	 * @memberof Verb
	 */
	load(node) {
		super.load(node);

		const actionClassName = node.getAttr("action").getValue();
		const actionClass = actions[actionClassName];

		if (!actionClass) {
			// TODO: error
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
			if (e.getElementType() === Element.NODE) {
				if (e.getName() === "response") {
					this.setResponse(e.getAttr("id").getValue(), 
					e.getAttr("id").getValue());
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
