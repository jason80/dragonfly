import { DFMLElement } from "../dfml/js/main/element.js";
import { DFMLNode } from "../dfml/js/main/node.js";
import { DFMLValue } from "../dfml/js/main/value.js";
import { Action  } from "./action.js";
import { actions } from "./actions.js";
import { responses } from "./responses.js";

export class ActionEvent {
	constructor() {
		this.actions = [];
		this.cancel = false;
		this.responses = []
		this.conditions = []
	}

	
	/**
	 *
	 *
	 * @param {Action} action
	 * @return {boolean} 
	 * @memberof ActionEvent
	 */
	match(action) {
		return this.actions.includes(action.constructor);
	}

	/**
	 *
	 *
	 * @param {ActionResponse} response
	 * @memberof ActionEvent
	 */
	addResponse(response) {
		this.responses.push(response);
	}

	/**
	 *
	 *
	 * @param {Condition} condition
	 * @memberof ActionEvent
	 */
	addCondition(condition) {
		this.conditions.push(condition);
	}

	/**
	 *
	 *
	 * @param {Action} action
	 * @return {boolean} 
	 * @memberof ActionEvent
	 */
	checkConditions(action) {
		let check = true;
		this.conditions.forEach(c => {
			if (!c.check(action)) check = false;
		});

		return check;
	}

	/**
	 *
	 *
	 * @param {Action} action
	 * @memberof ActionEvent
	 */
	execute(action) {
		this.responses.forEach(r => {
			r.execute(action);
		});
	}

	/**
	 * 
	 *
	 * @param {DFMLNode} node
	 * @memberof ActionEvent
	 */
	load(node) {
		node.getAttr("actions").getValue().split(",").forEach(a => {
			const actionClassName = a.trim();
			const actionClass = actions[actionClassName];

			if (!actionClass) {
				// TODO: Error
			} else {
				this.actions.push(actionClass);
			}
		});

		if (node.hasAttr("cancel"))
			this.cancel = node.getAttr("cancel").getValue() === "true";
		else this.cancel = false;

		// Load responses and conditions
		node.children.forEach(child => {

			// Simple text found: create a message response:
			if (child.getElementType() === DFMLElement.DATA && child.getValue().getType() == DFMLValue.STRING) {
				const text = child.getValue().getValue();
				const message = new responses["Print"]();
				message.message = text;
				this.addResponse(message);
			}

			// Condition or response found:
			if (child.getElementType() === DFMLElement.NODE) {
				if (child.getName() === "response") {
					const responseClassName = child.getAttr("class").getValue();
					const responseClass = responses[responseClassName];
					if (!responseClass) {
						// TODO: Error
					} else {
						const response = responseClass();
						response.load(child);
						this.addResponse(response);
					}
				}

				if (child.getName() === "if") {
					const condClassName = child.getAttr("class").getValue();
					const condClass = conditions[condClassName];
					if (!condClass) {
						// TODO: Error
					} else {
						const cond = condClass();
						cond.load(child);
						this.addCondition(cond);
					}
				}
			}
		});
	}
};
