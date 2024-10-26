import { Entity } from "./entity.js";
import * as actions from "./actions.js";

import { Node } from "../dfml/js/main/node.js";



/**
 * Represents the multi-name command wich is associated to Action.
 *
 * @export
 * @class Verb
 * @extends {Entity}
 */
export class Verb extends Entity {
	constructor() {
		this.action = null;
		this.syntax = [];
		this.responses = {};
	}

	/**
	 * Load verb from dfml node.
	 *
	 * @param {Node} node
	 * @memberof Verb
	 */
	load(node) {
		super.load(node);

		const actionString = node.getAttr("action");
		this.action = eval(`new actions.${actionString}()`);
		// TODO: handle forname error

		if (node.hasAttribute("syntax")) {
			node.getAttr("syntax").getValue().split().forEach(n => {
				self.syntax.append(member.strip());
			});
		}

		// Responses
		node.children.forEach(e => {
			if (e.getElementType() === Element.NODE) {
				if (e.getName() === "response") {
					this.setResponse(e.getAttr("id").getValue(), 
					e.getAttr("id").getValue());
				}
			}
		});

	}
};
