import { DFMLElement } from "../dfml/js/main/element.js";
import { DFMLNode } from "../dfml/js/main/node.js";
import { DFMLValue } from "../dfml/js/main/value.js";
import { Action } from "./action.js";
import { Entity } from "./entity.js";
import { ActionEvent } from "./actionevent.js";
import { Output } from "./output.js";
import { Connection } from "./movement.js";
import { Utils } from "./utils.js";

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

		for (const n of this.dictionary.nouns) {
			if (n.container === this) {
				if (n.responds(name)) return true;
			}
		}

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
		this.attrs = new Set([...this.attrs, ...values]);
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
		values.forEach(v => {
			this.attrs.delete(v);
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
		this.variables[name] = value;
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
	async doEvent(action, eventList) {
			
		let result = true;
		for (const actionEvent of eventList) {
			// If match action with list
			if (actionEvent.match(action)) {
				// Check if actionevent's conditions return true
				if (!actionEvent.checkConditions(action)) continue;
				
				// Execute responses
				await actionEvent.execute(action);
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
	async doBefore(action) {
		return await this.doEvent(action, this.beforeEvents);
	}
	
	/**
	 * Perform After ActionEvent match with the Action, check if it meets the condition, and executes
	 * the event.
	 *
	 * @param {Action} action target Action.
	 * @return {boolean}  True if and only if the event has not cacelled.
	 * @memberof Noun
	 */
	async doAfter(action) {
		return await this.doEvent(action, this.afterEvents);
	}

	/**
	 * Construct the first name of the noun adding the definite article depending on the
	 * gender and the number of `this`.
	 *
	 * @return {string} The name with the article.
	 * @memberof Noun
	 */
	the() {
        
        let result = "";

        // If it's a proper noun:
        if (this.isSet("proper")) {
            result = this.getName();
        } else {
            for (const a of this.dictionary.articles) {
                if (a.female === this.isSet("female") && a.plural === this.isSet("plural") && !a.indefinited) {
                    result = `${a.name} ${this.getName()}`;
                    break;
                }
            }
        }

        return result;
    }

	/**
	 * Construct the first name of the noun adding the indefinite article depending on the
	 * gender and the number of `this`. If the noun is countless, return only the first name.
	 *
	 * @return {string} The name with the article.
	 * @memberof Noun
	 */
	a() {
        if (this.isSet("countless")) return this.getName();

        let result = "";
        for (const a of this.dictionary.articles) {
            if (a.female === this.isSet("female") && a.plural === this.isSet("plural") && a.indefinited) {
                
				if (a.name === 'a' && this.isSet('an')) {
					result = `an ${this.getName()}`;
					break;
				}
				
				result = `${a.name} ${this.getName()}`;
                break;
            }
        }

        return result;
    }

	/**
	 * Return the definite article if the noun is defined; otherwise, return the indefinite article.
	 *
	 * @return {string} The article depending on the noun.
	 * @memberof Noun
	 */
	article() {
        return this.isSet("definited") ? this.the() : this.a();
    }

	/**
	 * Return a connection indicating the associated exit.
	 *
	 * @param {string} exit The exit to match connection.
	 * @return {Connection} the connection associated to exit. If not exists any connection
	 *					with the exit, return null.
	 * @memberof Noun
	 */
	getConnection(exit) {
		let conn = null;

		const exitObj = this.dictionary.getExit(exit);
		if (!exitObj) {
			Output.error(`Get connection from "${this.getName()}": exit "${exit}" not found in dictionary.`);
			return null;
		}

		this.connections.forEach((c) => {
			if (exitObj.responds(c.exit)) conn = c;
		});

		return conn;
	}

	/**
	 * Remove connection giving the exit.
	 *
	 * @param {string} exit associated exit to connection to remove.
	 * @memberof Noun
	 */
	removeConnection(exit) {

		const exitObj = this.dictionary.getExit(exit);
		if (!exitObj) {
			Output.error(`Removing connection from "${this.getName()}": exit "${exit} not found in dictionary."`);
			return ;
		}

		// Gets the index
		let index = 0;
		for (const conn of this.connections) {
			if (exitObj.responds(conn.exit)) break;
			index ++;
		}

		// Connection not found
		if (index >= this.connections.length) {
			Output.error(`Removing connection from "${this.getName()}": connection "${exit}" not found.`)
			return ;
		}

		// Remove connection
		this.connections.splice(index, 1);

	}

	/**
	 * Clone the object on dictionary inner especified container.
	 * Utilice clone to add generic objects like floor, walls and roof.
	 *
	 * @param {Noun} container
	 * @memberof Noun
	 */
	clone(container) {
		const copy = Object.assign(Object.create(Object.getPrototypeOf(this)), this);
		copy.container = container;

		this.dictionary.nouns.push(copy);

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
					children.forEach(c => {
						if (c.getElementType() === DFMLElement.DATA &&
							c.getValue().getType() === DFMLValue.STRING) {
							this.set([ c.getValue().getValue() ]);
						} else {
							Output.error(`(Set) on load noun '${this.getName()}': no string data attribute.`);
						}
					});
				} else if (e.getName() === "variable") {

					if (Utils.expectedAttributes(e, "name", "value")) {
						this.setVariable(e.getAttr("name").getValue(),
						e.getAttr("value").getValue());
					}
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
				} else if (e.getName() === "connection") {
					const connection = new Connection();
					connection.load(e);
					this.connections.push(connection);
				} else if (e.getName() === "describe-place") {
					e.setName("after");
					e.setAttrString("actions", "LookAround");
					const event = new ActionEvent();
					event.load(e);
					this.afterEvents.push(event);
				} else if (e.getName() === "describe-object") {
					e.setName("after");
					e.setAttrString("actions", "ExamineObject");
					const event = new ActionEvent();
					event.load(e);
					this.afterEvents.push(event);
				} else if (e.getName() === "clone") {

					if (Utils.expectedAttributes(e, "instance")) {

						const instance = e.getAttr("instance").getValue();
						const lst = this.dictionary.getNouns(instance);

						if (lst.length === 0) {
							Output.error(`Clone: noun target "${instance}" not found in dictionary.`);
							return ;
						}

						lst[0].clone(this);

					}

				}
			}
		});
	}
}
