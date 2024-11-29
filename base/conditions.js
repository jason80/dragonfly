import { Condition } from "./condition.js";
import { Output } from "./output.js";

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
		const noun = action.book.dictionary.getNouns(this.instance);
		if (noun.length === 0) {
			 
			Output.error(`On IsSet condition: instance "${this.instance}" not found in dictionary.`);
		}
	
		return noun[0].isSet(this.attr);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue();
		this.attr = node.getAttr("attr").getValue();
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
		const noun = action.book.dictionary.getNouns(this.instance)
		if (noun.length === 0) {
			 
			Output.error(`On IsNotSet condition: instance "${this.instance}" not found in dictionary.`);
		}
		return !noun[0].isSet(this.attr);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue();
		this.attr = node.getAttr("attr").getValue();
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
		const e = action.book.dictionary.getExit(this.exit);
		if (!e) {
			 
			Output.error(`On DirectEqualsExit condition: exit "${this.exit}" not found in dictionary.`);
		}

		return e.responds(action.book.parser.directObjectString);
	}

	load(node) {
		this.exit = node.getAttr("exit").getValue();
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
		cont = action.book.dictionary.getNouns(this.container)
		if (cont.length === 0) {
			 
			Output.error(`On Contains condition: container "${this.container}" not found in dictionary.`);
		}

		return cont[0].contains(this.instance);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue();
		this.container = node.getAttr("container").getValue();
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
		cont = action.book.dictionary.getNouns(this.container)
		if (cont.length === 0) {
			
			Output.error(`On NotContains condition: container "${this.container}" not found in dictionary.`);
		}

		return !cont[0].contains(this.instance);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue();
		this.container = node.getAttr("container").getValue();
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
		const obj = action.book.parser.directObject;
		if (!obj) return false;

		return obj.responds(this.instance);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue();
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
		obj = action.book.parser.directObject;
		if (!obj) return true;

		return !obj.responds(this.instance);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue();
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
		const obj = action.book.parser.indirectObject;
		if (!obj) return false;

		return obj.responds(this.instance);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue();
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
		const obj = action.book.parser.indirectObject;
		if (!obj) return true;

		return !obj.responds(this.instance);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue();
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
		const obj = action.book.dictionary.getNouns(this.instance);

		if (obj.length === 0) {
			
			Output.error(`On condition "VariableEquals" instance "${this.instance}" not found in dictionary.`);
		}

		return obj[0].getVariable(this.variable) === this.value;
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue();
		this.variable = node.getAttr("variable").getValue();
		this.value = node.getAttr("value").getValue();
	}
} conditions.VariableEquals = VariableEquals;

export class ConnectionExists extends Condition {
	constructor() {
		super();
		this.instance = "";
		this.exit = "";
	}

	toString() {
		return `Connection "${this.exit}" exists in "${this.instance}."`;
	}

	check(action) {
		const place = action.book.dictionary.getNouns(this.instance);
		if (place.length === 0) {
			Output.error(`On condition "ConnectionExists" instance "${this.instance}" not found in dictionary.`);
		}

		return place[0].getConnection(this.exit) != null;
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue();
		this.exit = node.getAttr("exit").getValue();
	}

} conditions.ConnectionExists = ConnectionExists;

export class ConnectionNotExists extends Condition {
	constructor() {
		super();
		this.instance = "";
		this.exit = "";
	}

	toString() {
		return `Connection "${this.exit}" not exists in "${this.instance}."`;
	}

	check(action) {
		const place = action.book.dictionary.getNouns(this.instance);
		if (place.length === 0) {
			Output.error(`On condition "ConnectionNotExists" instance "${this.instance}" not found in dictionary.`);
		}

		return place[0].getConnection(this.exit) == null;
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue();
		this.exit = node.getAttr("exit").getValue();
	}

} conditions.ConnectionNotExists = ConnectionNotExists;
