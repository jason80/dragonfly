import { DFMLElement } from "../dfml/js/main/element.js";
import { DFMLNode } from "../dfml/js/main/node.js";
import { DFMLValue } from "../dfml/js/main/value.js";
import { Action  } from "./action.js";
import { Output } from "./output.js";
import { actions } from "./actions.js";
import { responses } from "./responses.js";
import { conditions } from "./conditions.js";

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
				Output.error(`action class "${actionClassName}" not exists.`);
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
					this.loadResponse(child);
				} else if (child.getName() === "if") {
					this.loadCondition(child);
				} else { // Refers to Condition or Response class name

					// Convert to class name style
					let className = child.getName()
							.split('-')
							.map(word => word.charAt(0).toUpperCase() + word.slice(1))
							.join('');

					if (className.startsWith("If")) {
						child.setAttrString("class", className.slice(2));
						this.loadCondition(child);
					} else {
						child.setAttrString("class", className);
						this.loadResponse(child);
					}
				}
			}
		});
	}

	loadResponse(node) {
		const responseClassName = node.getAttr("class").getValue();
		const responseClass = responses[responseClassName];
		if (!responseClass) {
			Output.error(`response class "${responseClassName}" not exists.`);
		} else {
			const response = new responseClass();
			response.load(node);
			this.addResponse(response);
		}
	}

	loadCondition(node) {
		const condClassName = node.getAttr("class").getValue();
		const condClass = conditions[condClassName];
		if (!condClass) {
			Output.error(`condition class "${condClassName}" not exists.`);
		} else {
			const cond = new condClass();
			cond.load(node);
			this.addCondition(cond);
		}
	}
};
