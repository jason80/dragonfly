import { Entity } from "./entity.js";
import { DFMLNode } from "../dfml/js/main/node.js";

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
	 * Load verb from dfml node.
	 *
	 * @param {DFMLNode} node
	 * @memberof Verb
	 */
	load(node) {
		super.load(node);

		import('./actions.js').then((module) => {
			const actionClassName = node.getAttr("action").getValue();
			const actionClass = module[actionClassName];
			this.action = new actionClass();
			this.action.book = this.book;
			this.action.Verb = this;
		}).catch(error => {
			console.error("Class not found:", error);
		});

		if (node.hasAttr("syntax")) {
			node.getAttr("syntax").getValue().split().forEach(n => {
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
