import { Condition } from "./condition.js";

export const conditions = {};

export class IsSet extends Condition {
	constructor() {
		super();

		this.instance = "";
		this.attr = "";
	}

	toString() {
		return `Is set "${this.attr}" on "${this.instance}"`;
	}

	check(action) {
		// Gets the noun
		const noun = action.dictionary.getNouns(this.instance);
		if (noun.length === 0) {
			// TODO: 'On IsSet condition: instance "{this.instance}" not found in dictionary.')
		}
	
		return noun[0].isSet(this.attr);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue().getValue();
		this.attr = node.getAttr("attr").getValue().getValue();
	}
} conditions.IsSet = IsSet;

export class IsNotSet extends Condition {
	constructor() {
		super();

		this.instance = "";
		this.attr = "";
	}

	toString() {
		return `Is not set "${this.attr}" on "${this.instance}"`;
	}

	check(action) {
		// Gets the noun
		noun = action.dictionary.getNouns(this.instance)
		if (noun.length === 0) {
			// TODO: 'On IsNotSet condition: instance "{this.instance}" not found in dictionary.')
		}
		return !noun[0].isSet(this.attr);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue().getValue();
		this.attr = node.getAttr("attr").getValue().getValue();
	}
} conditions.IsNotSet = IsNotSet;

export class DirectEqualsExit extends Condition {
	constructor() {
		super();
		this.exit = "";
	}

	toString() {
		return `Direct equals exit: "${this.exit}"`;
	}

	check(action) {
		const e = action.dictionary.getExit(this.exit);
		if (!e) {
			// TODO: 'On DirectEqualsExit condition: exit "{this.exit}" not found in dictionary.')
		}

		return e.responds(action.parser.directObjectString);
	}

	load(node) {
		this.exit = node.getAttr("exit").getValue().getValue();
	}
} conditions.DirectEqualsExit = DirectEqualsExit;
		
export class Contains extends Condition {
	constructor() {
		super();
		this.container = "";
		this.instance = "";
	}

	toString() {
		return `"${this.container}" contains "${this.instance}"`;
	}

	check(action) {
		cont = action.dictionary.getNouns(this.container)
		if (cont.length === 0) {
			// TODO: 'On Contains condition: container "{this.container}" not found in dictionary.')
		}

		return cont[0].contains(this.instance);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue().getValue();
		this.container = node.getAttr("container").getValue().getValue();
	}
} conditions.Contains = Contains;

export class NotContains extends Condition {
	constructor() {
		super();
		this.container = "";
		this.instance = "";
	}

	toString() {
		return `"${this.container}" not contains "${this.instance}"`;
	}

	check(action) {
		cont = action.dictionary.getNouns(this.container)
		if (cont.length === 0) {
			// TODO: 'On NotContains condition: container "{this.container}" not found in dictionary.')
		}

		return !cont[0].contains(this.instance);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue().getValue();
		this.container = node.getAttr("container").getValue().getValue();
	}
} conditions.NotContains = NotContains;

export class DirectEquals extends Condition {
	constructor() {
		super();
		this.instance = "";
	}

	toString() {
		return `Direct equals "${this.instance}"`;
	}

	check(action) {
		const obj = action.parser.directObject;
		if (!obj) return false;

		return obj.responds(this.instance);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue().getValue();
	}
} conditions.DirectEquals = DirectEquals;

export class DirectNotEquals extends Condition {
	constructor() {
		super();
		this.instance = "";
	}

	toString() {
		return `Direct not equals "${this.instance}"`;
	}

	check(action) {
		obj = action.parser.directObject;
		if (!obj) return true;

		return !obj.responds(this.instance);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue().getValue();
	}
} conditions.DirectNotEquals = DirectNotEquals;

export class IndirectEquals extends Condition {
	constructor() {
		super();
		this.instance = "";
	}

	toString() {
		return `Indirect equals "${this.instance}"`;
	}

	check(action) {
		obj = action.parser.indirectObject;
		if (!obj) return false;

		return obj.responds(this.instance);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue().getValue();
	}
} conditions.IndirectEquals = IndirectEquals;

export class IndirectNotEquals extends Condition {
	constructor() {
		super();
		this.instance = "";
	}

	toString() {
		return `Indirect equals "${this.instance}"`;
	}

	check(action) {
		obj = action.parser.indirectObject;
		if (!obj) return true;

		return !obj.responds(this.instance);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue().getValue();
	}
} conditions.IndirectNotEquals = IndirectNotEquals;

export class VariableEquals extends Condition {
	constructor() {
		super();
		this.instance = "";
		this.variable = "";
		this.value = "";
	}

	toString() {
		return `Variable "${this.variable}" equals to "${this.value}."`;
	}

	check(action) {
		const obj = action.dictionary.getNouns(this.instance);

		if (obj.length === 0) {
			// TODO: 'On condition "VariableEquals" instance "{this.instance}" not found in dictionary.')
		}

		return obj[0].getVariable(this.variable) === this.value;
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue().getValue();
		this.variable = node.getAttr("variable").getValue().getValue();
		this.value = node.getAttr("value").getValue().getValue();
	}
} conditions.VariableEquals = VariableEquals;
