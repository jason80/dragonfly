//import { Element } from "../dfml/js/main/element.js";

//import { Node } from "../dfml/js/main/node.js";

/**
 * Nouns represents the objects of the game. Can be contained by other nouns.
 *		and has attributes and variables.
 *
 * @export
 * @class Noun
 * @extends {Element}
 */
export class Noun extends Element {
	static #idMax = 0;

	/**
	 * Creates an instance of Noun.
	 * @param {Noun} container
	 * @memberof Noun
	 */
	constructor(container) {
		this.container = container;
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
		self.dictionary.nouns.array.forEach(n => {
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
	 * Load the noun from dfml element.
	 *
	 * @param {Node} node dfml element.
	 * @memberof Noun
	 */
	load(node) {
		super.load(node);

		node.getChildren().array.forEach(e => {
			if (e.getElementType() === Element.NODE) {
				if (e.getName() === "set") {
					const children = e.getChildren();
					children.array.forEach(c => {
						if (c.getElementType() === Element.DATA &&
							c.getValue().getType() === Value.STRING) {
							this.set([ c.getValue().getValue() ]);
						} else { /* TODO: Error */ }
					});
				} else if (e.getName() === "variable") {
					this.setVariable(e.getAttr("name").getValue());
				}
			}
		});
	}
}
