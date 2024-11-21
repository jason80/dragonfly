/**
 * An ActionEvent is executed under an action triggered by the player.
 * A Noun can have one or more ActionEvents for "before" and 
 * one or more for "after."
 *
 */

import { actions } from "./actions.js";
import { responses } from "./responses.js";
import { conditions } from "./conditions.js"
import { DFMLElement } from "../dfml/js/main/element.js";
import { DFMLValue } from "../dfml/js/main/value.js";

export class ActionEvent {

	/**
	 * Creates an instance of ActionEvent.
	 * @memberof ActionEvent
	 */
	constructor() {
		this.actions = [];
		this.cancel = false;
		this.responses = []
		this.conditions = []
	}

	/**
	 * Checks if this ActionEvent responds to the action to be handled.
	 *
	 * @param {Action} action action to check.
	 * @return {boolean} true if the action matches any of this ActionEvent.
	 * @memberof ActionEvent
	 */
	match(action) {
		return this.actions.includes(action.constructor);
	}

	/**
	 * Adds an ActionResponse to this event.
	 *
	 * @param {ActionResponse} response ActionResponse to add.
	 * @memberof ActionEvent
	 */
	addResponse(response) {
		this.responses.push(response);
	}

	/**
	 * Adds a Condition to this event.
	 *
	 * @param {Condition} condition Condition to add.
	 * @memberof ActionEvent
	 */
	addCondition(condition) {
		this.conditions.push(condition);
	}

	/**
	 * Checks the conditions of the event to be executed.
	 *
	 * @param {Action} action Current action to be executed.
	 * @return {boolean} true if all conditions are met.
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
	 * Executes all responses in the order they were added.
	 *
	 * @param {Action} action current action.
	 * @memberof ActionEvent
	 */
	execute(action) {
		this.responses.forEach(r => {
			r.execute(action);
		});
	}

	/**
	 * Loads the event from a DFML node.
	 *
	 * @param {DFMLNode} node DFML node.
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

	/**
	 * Loads an ActionResponse from a DFML node.
	 *
	 * @param {DFMLNode} node DFML node.
	 * @memberof ActionEvent
	 */
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

	/**
	 * Loads a Condition from a DFML node.
	 *
	 * @param {DFMLNode} node DFML node.
	 * @memberof ActionEvent
	 */
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
