import { DFMLBuilder } from "../dfml/js/main/builder.js"
import { DFMLData } from "../dfml/js/main/data.js";
import { DFMLElement } from "../dfml/js/main/element.js";
import { DFMLNode } from "../dfml/js/main/node.js";
import { DFMLValue } from "../dfml/js/main/value.js";
import { DFMLParser } from "../dfml/js/main/parser.js";
import { Connection } from "./movement.js";
import { Output } from "./output.js"

class PersistenceSystem {

	constructor(dictionary) {
		this.dictionary = dictionary;
	}

	save() {}

	load() {}
};

export class DFMLPersistenceSystem extends PersistenceSystem {

	constructor(dictionary) {
		super(dictionary);
	}

	save() {
		const root = DFMLNode.create("dragonfly");

		for (const noun of this.dictionary.nouns) {
			root.children.push(this.saveNoun(noun));
		}

		const builder = DFMLBuilder.create();
		return builder.buildNode(root);
	}

	saveNoun(noun) {

		const node = DFMLNode.create("noun");

		node.setAttrInteger("id", noun.id);
		node.setAttrString("names", Array.from(noun.names).join(", "));

		if (noun.container)
			node.setAttrInteger("container", noun.container.id);
		else
			node.setAttrInteger("container", "0");

		// Attributes
		const setNode = DFMLNode.create("set");
		node.addChild(setNode);
		for (const a of noun.attrs) {
			setNode.children.push(DFMLData.createString(a));
		}

		// Variables
		for (const key in noun.variables) {
			const varNode = DFMLNode.create("variable");
			varNode.setAttrString("name", key);
			varNode.setAttrString("value", noun.variables[key]);
			node.addChild(varNode);
		}

		// Connections
		for (const c of noun.connections) {
			const connNode = DFMLNode.create("connection");
			connNode.setAttrString("exit", c.exit);
			connNode.setAttrString("destiny", c.destiny);
			node.addChild(connNode);
		}

		return node;
	}

	load(str) {

		const parser = new DFMLParser(str);

		let root = null;

		for (const r of parser.parse()) {
			if (r.getElementType() === DFMLElement.NODE) {
				if (r.getName() === "dragonfly") {
					root = r; break;
				}
			}
		}

		for (const n of root.children) {
			if (n.getElementType() === DFMLElement.NODE) {
				if (n.getName() === "noun") {
					this.loadNoun(n);
				}
			}
		}
	}

	loadNoun(node) {
		const id = parseInt(node.getAttr("id").getValue(), 10);

		const noun = this.dictionary.nounByID(id)
		if (!noun) {
			Output.error(`Loading saved state: noun id=${id} not found in dictionary.`);
			return;
		}

		// Clear all
		noun.attrs = new Set();
		noun.variables = {};
		noun.connections = [];

		// Set container
		const contID = parseInt(node.getAttr("container").getValue(), 10);
		if (contID !== 0) {
			noun.container = this.dictionary.nounByID(contID);
			if (!noun.container) {
				Output.error(`Loading saved state: container id=${id} not found in dictionary.`);
				return;
			}
		}
		else noun.container = null;

		// Load names
		noun.names = [];
		node.getAttr("names").getValue().split(',').forEach(n => {
			noun.names.push(n.trim());
		});

		for (const child of node.children) {
			if (child.getElementType() === DFMLElement.NODE) {
				if (child.getName() === "set") {
					const sets = child.getChildren();
					sets.forEach(c => {
						if (c.getElementType() === DFMLElement.DATA &&
							c.getValue().getType() === DFMLValue.STRING) {
							noun.set([ c.getValue().getValue() ]);
						}
					});
				} else if (child.getName() === "variable") {
					noun.setVariable(child.getAttr("name").getValue(),
					child.getAttr("value").getValue());
				} else if (child.getName() === "connection") {
					const conn = new Connection();
					conn.exit = child.getAttr("exit").getValue();
					conn.destiny = child.getAttr("destiny").getValue();
					noun.connections.push(conn);
				}
			}
		}
	}
};

