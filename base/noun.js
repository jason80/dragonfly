import { DFMLElement } from "../dfml/js/main/element.js";

import { DFMLNode } from "../dfml/js/main/node.js";
import { Action } from "./action.js";
import { Entity } from "./entity.js";
import { ActionEvent } from "./actionevent.js";

/**
 * Nouns represents the objects of the game. Can be contained by other nouns.
 *		and has attributes and variables.
 *
 * @export
 * @class Noun
 * @extends {Element}
 */
export class Noun extends Entity {
	static #idMax = 0;

	/**
	 * Creates an instance of Noun.
	 * @param {Noun} container
	 * @memberof Noun
	 */
	constructor(container = null) {

		super();

		this.container = null;

		if (container != undefined) this.container = container;

		this.book = null;
		this.dictionary = null;

		Noun.#idMax ++;
		this.id = Noun.#idMax;

		this.attrs = new Set();
		this.variables = {};

		this.beforeEvents = [];
		this.afterEvents = [];

		this.connections = [];
	}

	/**
	 * Check if this noun contains a noun.
	 *
	 * @param {string} name the name of the child.
	 * @return {boolean} true if and only if this contains the child.
	 * @memberof Noun
	 */
	contains(name) {
		self.dictionary.nouns.array.forEach(n => {
			if (n.container === this) {
				if (n.responds(name)) return true;
			}
		});

		return false;
	}

	/**
	 * Return a list with chils wich responds to name.
	 * If the name = "", return all childs.
	 *
	 * @param {string} name
	 * @memberof Noun
	 */
	children(name) {
		let result = [];
		this.dictionary.nouns.forEach(n => {
			if (n.container == this) {
				if (name === undefined) {
					result.push(n);
				} else {
					if (n.responds(name)) result.push(n);
				}
			}
		});
		return result;
	}

	/**
	 * Set a list of attributes.
	 *
	 * @param {List} values
	 * @memberof Noun
	 */
	set(values) {
		this.attrs = new Set(...this.attrs, ...values);
	}

	/**
	 * Check if an attribute is setted.
	 */
	isSet(value) {
		return this.attrs.has(value);
	}

	/**
	 * Unset a list of attributes.
	 */
	unset(values) {
		values.array.forEach(v => {
			self.attrs.delete(v);
		});
	}


	/**
	 * Return the value of the variable.
	 *
	 * @param {string} name name of the variable.
	 * @return {string} the value of the variable.
	 * @memberof Noun
	 */
	getVariable(name) {
		if (name in variables) {
			return variables[name];
		}
		
		return "";
	}

	/**
	 * Set the value of the variable.
	 *
	 * @param {string} name name of the variable.
	 * @param {string} value value of the variable.
	 * @memberof Noun
	 */
	setVariable(name, value) {
		self.variables[name] = value;
	}

	/**
	 * Add a new Before action evento to the list.
	 *
	 * @param {ActionEvent} actionEvent Before ActionEvent.
	 * @memberof Noun
	 */
	addBefore(actionEvent) {
		this.beforeEvents.push(actionEvent);
	}

	/**
	 * Add a new After action evento to the list.
	 *
	 * @param {ActionEvent} actionEvent After ActionEvent.
	 * @memberof Noun
	 */
	addAfter(actionEvent) {
		this.afterEvents.push(actionEvent);
	}

	/**
	 * Perform ActionEvent match with the Action, check if it meets the condition, and executes
	 * the event.

	 * eventList argument allows especify Before or After events.
	 *
	 * @param {Action} action target Action.
	 * @param {Array.<ActionEvent>} eventList list of the events.
	 * @return {boolean} 
	 * @memberof Noun
	 */
	#doEvent(action, eventList) {
			
		let result = true;
		for (const actionEvent of eventList) {
			// If match action with list
			if (actionEvent.match(action)) {
				// Check if actionevent's conditions return true
				if (!actionEvent.checkConditions(action)) continue;
				
				// Execute responses
				actionEvent.execute(action);
				result = !actionEvent.cancel;
			}
		}

		return result;
	}

	/**
	 * Perform Before ActionEvent match with the Action, check if it meets the condition, and executes
     * the event.
	 *
	 * @param {Action} action target Action.
	 * @return {boolean} True if and only if the event has not cacelled.
	 * @memberof Noun
	 */
	doBefore(action) {
		return this.#doEvent(action, this.beforeEvents);
	}
	
	/**
	 * Perform After ActionEvent match with the Action, check if it meets the condition, and executes
	 * the event.
	 *
	 * @param {Action} action target Action.
	 * @return {boolean}  True if and only if the event has not cacelled.
	 * @memberof Noun
	 */
	doAfter(action) {
		return this.#doEvent(action, this.afterEvents);
	}

	/**
	 * Load the noun from dfml element.
	 *
	 * @param {DFMLNode} node dfml element.
	 * @memberof Noun
	 */
	load(node) {
		super.load(node);

		node.getChildren().forEach(e => {
			if (e.getElementType() === DFMLElement.NODE) {
				if (e.getName() === "set") {
					const children = e.getChildren();
					children.array.forEach(c => {
						if (c.getElementType() === DFMLElement.DATA &&
							c.getValue().getType() === Value.STRING) {
							this.set([ c.getValue().getValue() ]);
						} else { /* TODO: Error */ }
					});
				} else if (e.getName() === "variable") {
					this.setVariable(e.getAttr("name").getValue());
				} else if (e.getName() === "noun") {
					const noun = new Noun(this);
					noun.book = this.book;
					noun.dictionary = this.dictionary;
					noun.load(e);
					this.dictionary.nouns.push(noun);
				} else if (e.getName() === "before") {
					const event = new ActionEvent();
					event.load(e);
					this.beforeEvents.push(event);
				} else if (e.getName() === "after") {
					const event = new ActionEvent();
					event.load(e);
					this.afterEvents.push(event);
				}
			}
		});
	}
}
