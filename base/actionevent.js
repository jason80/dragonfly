/**
 * An ActionEvent is executed under an action triggered by the player.
 * A Noun can have one or more ActionEvents for "before" and 
 * one or more for "after."
 *
 */

import { Output } from "./output.js";
import { actions } from "./actions.js";
import { loadResponses } from "./eventloader.js";
import { Utils } from "./utils.js";

export class ActionEvent {

	/**
	 * Creates an instance of ActionEvent.
	 * @memberof ActionEvent
	 */
	constructor() {
		this.actions = [];
		this.cancel = false;
		this.initialCancel = false;
		this.responses = []
		this.allActions = false;
	}

	/**
	 * Checks if this ActionEvent responds to the action to be handled.
	 *
	 * @param {Action} action action to check.
	 * @return {boolean} true if the action matches any of this ActionEvent.
	 * @memberof ActionEvent
	 */
	match(action) {
		return this.allActions ?
			!this.actions.includes(action.constructor) :
			this.actions.includes(action.constructor);
	}

	/**
	 * Executes all responses in the order they were added.
	 *
	 * @param {Action} action current action.
	 * @memberof ActionEvent
	 */
	async execute(action) {
		action.eventControl = { cancel: this.initialCancel, brk: false };

		for (const r of this.responses) {
			await r.execute(action);

			if (action.eventControl.brk) break;
		}

		this.cancel = action.eventControl.cancel;
	}

	/**
	 * Loads the event from a DFML node.
	 *
	 * @param {DFMLNode} node DFML node.
	 * @memberof ActionEvent
	 */
	load(node) {

		if (!Utils.expectedAttributes(node, "actions")) return;

		let strActions = "";
		if (node.getAttr("actions").getValue() === "*") {

			if (!Utils.expectedAttributes(node, "except")) return;

			// All actions except ...
			this.allActions = true;
			strActions = node.getAttr("except").getValue();
		} else strActions = node.getAttr("actions").getValue();

		strActions.split(",").forEach(a => {
			const actionClassName = a.trim();
			const actionClass = actions[actionClassName];

			if (!actionClass) {
				Output.error(`action class "${actionClassName}" not exists.`);
			} else {
				this.actions.push(actionClass);
			}
		});

		if (node.hasAttr("cancel"))
			this.initialCancel = node.getAttr("cancel").getValue() === "true";
		else this.initialCancel = false;

		loadResponses(node, this.responses);
	}

};
