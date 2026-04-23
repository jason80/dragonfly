import { DFMLElement } from "../dfml/js/main/element.js";
import { DFMLValue } from "../dfml/js/main/value.js";
import { ActionResponse } from "./actionresponse.js";
import { Output } from "./output.js";
import { Help } from "./help.js";
import { Connection } from "./movement.js";
import { Utils } from "./utils.js";
import { loadResponses } from "./eventloader.js";
import { Action } from "./action.js";

export const responses = {};

/************************************************************/
/*					RESPONSES								*/
/************************************************************/

export class CancelEvent extends ActionResponse {

	constructor() {
		super();
	}

	toString() {
		return "cancel event";
	}

	async execute(action) {
		action.eventControl.cancel = true;
	}

	load(node) {}
	
}
responses.CancelEvent = CancelEvent;

export class ResumeEvent extends ActionResponse {

	constructor() {
		super();
	}

	toString() {
		return "resume event";
	}

	async execute(action) {
		action.eventControl.cancel = false;
	}

	load(node) {}
	
}
responses.ResumeEvent = ResumeEvent;

export class Break extends ActionResponse {

	constructor() {
		super();
	}

	toString() {
		return "break";
	}

	async execute(action) {
		action.eventControl.brk = true;
	}

	load(node) {}
}
responses.Break = Break;

export class Print extends ActionResponse {

	constructor() {
		super();
		this.message = ""
		this.style = ""
	}

	toString() {
		return `print "${this.message}"`
	}

	async execute(action) {
		Output.print(this.message, this.style);
	}

	load(node) {

		if (node.hasAttr("style"))
			this.style = node.getAttr("style").getValue();

		if (node.children.length === 1) {
			if (node.children[0].getElementType() === DFMLElement.DATA) {
				if (node.children[0].getValue().getType() === DFMLValue.STRING) {
					this.message = node.children[0].getValue().getValue();
					return ;
				}
			}
		} else if (node.children.length === 0) {
			this.message = "";
			return ;
		}
		
		Output.error(`On Print Response: Extra element found.`);
	}
} responses.Print = Print;

export class Append extends ActionResponse {
	constructor() {
		super();
		this.message = "";
		this.style = "";
	}

	toString() {
		return `append "${this.message}"`;
	}

	async execute(action) {
		Output.append(this.message, this.style);
	}

	load(node) {

		if (node.hasAttr("style"))
			this.style = node.getAttr("style").getValue();

		if (node.children.length === 1) {
			if (node.children[0].getElementType() === DFMLElement.DATA) {
				if (node.children[0].getValue().getType() === DFMLValue.STRING) {
					this.message = node.children[0].getValue().getValue();
					return ;
				}
			}
		} else if (node.children.length === 0) {
			Output.error(`On Append Response: Extra element found.`);
			return ;
		}
		
		Output.error(`On Append Response: Extra element found.`);
	}
} responses.Append = Append;

export class Attr extends ActionResponse {
	constructor() {
		super();
		this.instance = ""
		this.set = ""
		this.unset = ""
	}

	toString() {
		let list = [];
		if (this.set)
			list.push(`set "${this.set}"`);
		if (this.unset)
			list.push(`unset "${this.unset}"`);

		return " & ".join(list) + " to " + this.instance;
	}

	async execute(action) {
		const objList = action.book.dictionary.getNouns(this.instance);
		if (objList.length === 0) {
			Output.error(`On Set response: noun "${this.instance}" not found in dictionary.`);
		}

		const obj = objList[0];

		let sets = [];
		this.set.split(",").forEach( s => {
			sets.push(s.trim());
		});

		let unsets = [];
		this.unset.split(",").forEach( u => {
			unsets.push(u.trim());
		});

		obj.set(sets)
		obj.unset(unsets)
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance")) return ;

		this.instance = node.getAttr("instance").getValue();
		if (node.hasAttr("set"))
			this.set = node.getAttr("set").getValue();
		if (node.hasAttr("unset"))
			this.unset = node.getAttr("unset").getValue();
	}
} responses.Attr = Attr;

export class VariableSet extends ActionResponse {
	constructor() {
		super();
		this.instance = "";
		this.name = "";
		this.value = "";
	}

	toString() {
		return `Set "${this.value}" to variable "${this.name}", instance: "${this.instance}".`;
	}

	async execute(action) {
		list = action.book.dictionary.getNouns(this.instance);
		if (list.length === 0) {
			Output.error(`On VariableSet response: noun "${this.instance}" not found in dictionary.`);
		}

		const obj = list[0];

		obj.setVariable(this.name, this.value);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "name", "value")) return ;

		this.instance = node.getAttr("instance").getValue();
		this.name = node.getAttr("name").getValue();
		this.value = node.getAttr("value").getValue();
	}
} responses.VariableSet = VariableSet;

export class VariableAdd extends ActionResponse {
	constructor() {
		super();
		this.instance = "";
		this.name = "";
		this.value = "1";
	}

	toString() {
		return `Add "${this.value}" to variable "${this.name}", instance: "${this.instance}".`;
	}

	async execute(action) {
		const list = action.book.dictionary.getNouns(this.instance);
		if (list.length === 0) {
			Output.error(`On VariableAdd response: noun "${this.instance}" not found in dictionary.`);
		}

		const obj = list[0];

		if (this.name in obj.variables) {

			const result = (parseInt(obj.variables[this.name]) + parseInt(this.value));
			obj.variables[this.name] = result + "";
		} else {
			Output.error(`On VariableAdd response: variable "${this.name}" not found in noun "${this.instance}".`);
		}
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "name")) return ;

		if (node.hasAttr("value"))
			this.value = node.getAttr("value").getValue();

		this.instance = node.getAttr("instance").getValue();
		this.name = node.getAttr("name").getValue();
	}
} responses.VariableAdd = VariableAdd;

export class VariableSub extends ActionResponse {
	constructor() {
		super();
		this.instance = "";
		this.name = "";
		this.value = "1";
	}

	toString() {
		return `Subtract "${this.value}" to variable "${this.name}", instance: "${this.instance}".`;
	}

	async execute(action) {
		const list = action.book.dictionary.getNouns(this.instance);
		if (list.length === 0) {
			Output.error(`On VariableSub response: noun "${this.instance}" not found in dictionary.`);
		}

		const obj = list[0];

		if (this.name in obj.variables) {
			const result = (parseInt(obj.variables[this.name]) - parseInt(this.value));
			obj.variables[this.name] = result + "";
		} else {
			Output.error(`On VariableSub response: variable "${this.name}" not found in noun "${this.instance}".`);
		}
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "name")) return ;

		if (node.hasAttr("value"))
			this.value = node.getAttr("value").getValue();

		this.instance = node.getAttr("instance").getValue();
		this.name = node.getAttr("name").getValue();
	}
} responses.VariableSub = VariableSub;

export class AppendName extends ActionResponse {
	constructor() {
		super();
		this.instance = ""
		this.name = ""
	}

	toString() {
		return `Append name "${this.name}" to "${this.instance}"`;
	}

	async execute(action) {
		const objList = action.book.dictionary.getNouns(this.instance);
		if (objList.length === 0) {
			Output.error(`On AppendName response: noun "${this.instance}" not found in dictionary.`);
		}

		objList[0].appendName(this.name);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "name")) return ;

		this.instance = node.getAttr("instance").getValue();
		this.name = node.getAttr("name").getValue();
	}
} responses.AppendName = AppendName;

export class Move extends ActionResponse {
	constructor() {
		super();
		this.instance = ""
		this.destiny = ""
	}

	toString() {
		return `Move "${this.instance}" to "${this.destiny}"`;
	}

	#getObj(action, name) {
		const objList = action.book.dictionary.getNouns(name);
		if (objList.length === 0) return null;
		return objList[0];
	}

	async execute(action) {
		const obj = this.#getObj(action, this.instance)
		if (!obj) {
			Output.error(`On Move response: noun "${this.instance}" not found in dictionary.`);
		}

		const dest = this.#getObj(action, this.destiny)
		if (!dest) {
			Output.error(`On Move response: destiny "{this.destiny}" not found in dictionary.`);
		}

		obj.container = dest;
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "destiny")) return ;

		this.instance = node.getAttr("instance").getValue();
		this.destiny = node.getAttr("destiny").getValue();
	}
} responses.Move = Move;

export class Root extends ActionResponse {
	constructor() {
		super();
		this.instance = "";
	}

	toString() {
		return `Move "${this.instance}" to root`;
	}

	async execute(action) {
		const objList = action.book.dictionary.getNouns(this.instance);
		if (objList.length === 0) {
			Output.error(`On Root response: noun "${this.instance}" not found in dictionary.`);
		}

		objList[0].container = null;
	}
	
	load(node) {
		if (!Utils.expectedAttributes(node, "instance")) return ;
		this.instance = node.getAttr("instance").getValue();
	}
} responses.Root = Root;

export class Tip extends ActionResponse {
	constructor() {
		super();
		this.message = "";
		this.once = false;
	}

	toString() {
		return `Show tip "${this.message}"${this.once ? " once" : ""}`;
	}

	async execute(action) {
		if (this.once)
			Help.tipOnce(this.message);
		else Help.tip(this.message);
	}

	load(node) {
		this.once = node.hasAttr("once");

		if (node.children.length === 1) {
			if (node.children[0].getElementType() === DFMLElement.DATA) {
				if (node.children[0].getValue().getType() === DFMLValue.STRING) {
					this.message = node.children[0].getValue().getValue();
					return ;
				}
			}
		}

		Output.error(`On Tip Response: Extra element found.`);
	}
} responses.Tip = Tip;

export class Execute extends ActionResponse {
	constructor() {
		super();
		this.sentence = "";
	}

	toString() {
		return `'Execute "${this.sentence}" sentence`;
	}

	async execute(action) {
		await action.book.execute(this.sentence);
	}

	load(node) {
		if (node.children.length === 1) {
			if (node.children[0].getElementType() === DFMLElement.DATA) {
				if (node.children[0].getValue().getType() === DFMLValue.STRING) {
					this.sentence = node.children[0].getValue().getValue();
					return ;
				}
			}
		}
		
		Output.error(`On Execute Response: Extra element found.`);
	}
} responses.Execute = Execute;

export class AddConnection extends ActionResponse {
	constructor() {
		super();
		this.instance = "";
		this.exit = "";
		this.destiny = "";
	}

	toString() {
		return `Add connection to ${this.instance}: ${this.exit} -> ${this.destiny}`;
	}

	async execute(action) {
		const objList = action.book.dictionary.getNouns(this.instance);
		if (objList.length === 0) {
			Output.error(`On AddConnection response: noun "${this.instance}" not found in dictionary.`);
		}

		// If connection already exists: do nothing
		if (objList[0].getConnection(this.exit)) return ;

		const conn = new Connection();
		conn.exit = this.exit;
		conn.destiny = this.destiny;
		objList[0].connections.push(conn);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "exit", "destiny")) return ;

		this.instance = node.getAttr("instance").getValue();
		this.exit = node.getAttr("exit").getValue();
		this.destiny = node.getAttr("destiny").getValue();
	}
} responses.AddConnection = AddConnection;

export class RemoveConnection extends ActionResponse {
	constructor() {
		super();
		this.instance = "";
		this.exit = "";
	}

	toString() {
		return `Remove connection to ${this.instance}: ${this.exit}`;
	}

	async execute(action) {
		const objList = action.book.dictionary.getNouns(this.instance);
		if (objList.length === 0) {
			Output.error(`On RemoveConnection response: noun "${this.instance}" not found in dictionary.`);
		}

		objList[0].removeConnection(this.exit);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "exit")) return ;

		this.instance = node.getAttr("instance").getValue();
		this.exit = node.getAttr("exit").getValue();
	}
} responses.RemoveConnection = RemoveConnection;

export class ShowTitle extends ActionResponse {

	constructor() {
		super();
	}

	toString() {
		return "Show game title";
	}

	async execute(action) {
		action.book.showTitle();
	}

	load(node) {}

} responses.ShowTitle = ShowTitle;
		
export class RunConversation extends ActionResponse {
	constructor() {
		super();
		this.owner = "";
	}
		
	toString() {
		return `Run Conversation with '${this.owner}'`;
	}

	async execute(action) {
		const c = action.book.dictionary.getConversation(this.owner);
		c.start(action);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "owner")) return ;

		this.owner = node.getAttr("owner").getValue();
	}
} responses.RunConversation = RunConversation;

export class Pause extends ActionResponse {

	constructor() {
		super();

		this.key = "Enter";
	}

	toString() {
		return `Pause <${this.key}>`;
	}

	async execute(action) {
		await action.book.input.pause(this.key);
	}

	load(node) {
		if (node.hasAttr("key")) {
			this.key = node.getAttr("key").getValue();
		}
	}
} responses.Pause = Pause;

export class Clear extends ActionResponse {

	constructor() {
		super();
	}

	toString() {
		return "Clear";
	}

	async execute(action) {
		Output.clear();
	}

	load(node) {}
} responses.Clear = Clear;

export class RestartGame extends ActionResponse {
	constructor() {
		super();
	}

	toString() {
		return "Restart game";
	}

	async execute(action) {
		action.book.restart();
	}

	load(node) {}
} responses.RestartGame = RestartGame;

export class Call extends ActionResponse {
	constructor() {
		super();
		this.proc = "";
	}

	toString() {
		return `Call ${this.proc}.`;
	}

	async execute(action) {

		const proc = action.book.dictionary.procedures.get(this.proc);
		if (proc === undefined) {
			Output.error(`Procedure '${this.proc}' not found.`);
			return ;
		}

		await proc.execute(action);
	}

	load(node) {
		if (!Utils.expectedAttributes(node, "procedure")) return ;

		this.proc = node.getAttr("procedure").getValue();
	}

} responses.Call = Call;

export class Sequence extends ActionResponse {
	constructor() {
		super();
		this.responses = [];
		this.index = -1;
		this.chance = 1.0;
	}

	toString() {
		return "Sequence";
	}

	async execute(action) {

		if (action.eventControl.brk) return ;

		if (this.responses.length === 0) return ;

		if (Math.random() > this.chance) return ;

		this.index ++;
		if (this.index >= this.responses.length) this.index = 0;

		await this.responses[this.index].execute(action);
	}

	load(node) {

		// Load shuffle
		let shuffle = false;
		if (node.hasAttr("shuffle")) {
			if (node.getAttr("shuffle").getType() === DFMLValue.BOOLEAN) {
				shuffle = node.getAttr("randomize").getValue() === "true";
			} else {
				Output.error("Warning: Sequence attr shuffle must be a boolean. Assuming false.");
			}
		}

		// Load chance
		let error = false;
		if (node.hasAttr("chance")) {
			if (node.getAttr("chance").getType() === DFMLValue.DOUBLE) {
				try {
					this.chance = parseFloat(node.getAttr("chance").getValue());
				} catch (e) {
					error = true;
				}
			} else {
				error = true;
			}
		}

		if (error)
			Output.error("Warning: Sequence chance must be a double. Assuming 1.0.");

		// Load resoonses
		loadResponses(node, this.responses);

		if (this.responses.length === 0) {
			Output.error("Warning: Sequence must have at least one response.");
		}

		// Randomize responses
		if (shuffle) {
			this.responses.sort(() => Math.random() - 0.5);
		}
	}

} responses.Sequence = Sequence;

/********************************************************************/
/*					CONDITIONS										*/
/********************************************************************/

/**
 * Execute nested responses if the condition is true.
 *
 * @export
 * @class Condition
 */
export class ConditionResponse extends ActionResponse {
	/**
	 * Creates an instance of Condition.
	 * @memberof Condition
	 */
	constructor() {
		super();
		this.responses = [];
	}

	/** 
	 * Checks if the condition is true. (Override this method)
	 * 
	 * @param {Action} action Current action
	 * @return {boolean} true if the condition is true.
	 * 
	 */
	check(action) {
		return true;
	}

	/** 
	 * Executes the condition response.
	 * 
	 * @param {Action} action Current action
	 * 
	 */
	async execute(action) {
		if (action.eventControl.brk) return ;

		if (!this.check(action)) return ;

		for (const r of this.responses) {
			await r.execute(action);

			if (action.eventControl.brk) break;
		}
	}

	load(node) {
		loadResponses(node, this.responses);
	}
};


export class IfIsSet extends ConditionResponse {
	constructor() {
		super();

		this.instance = "";
		this.attr = "";
	}

	toString() {
		return `If is set "${this.attr}" on "${this.instance}"`;
	}

	check(action) {
		// Gets the noun
		const noun = action.book.dictionary.getNouns(this.instance);
		if (noun.length === 0) {
			 
			Output.error(`On IfIsSet condition: instance "${this.instance}" not found in dictionary.`);
		}
	
		return noun[0].isSet(this.attr);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "attr")) return ;

		this.instance = node.getAttr("instance").getValue();
		this.attr = node.getAttr("attr").getValue();

		ConditionResponse.prototype.load.call(this, node);
	}
} responses.IfIsSet = IfIsSet;

export class IfIsNotSet extends ConditionResponse {
	constructor() {
		super();

		this.instance = "";
		this.attr = "";
	}

	toString() {
		return `If is not set "${this.attr}" on "${this.instance}"`;
	}

	check(action) {
		// Gets the noun
		const noun = action.book.dictionary.getNouns(this.instance)
		if (noun.length === 0) {
			 
			Output.error(`On IfIsNotSet condition: instance "${this.instance}" not found in dictionary.`);
		}
		return !noun[0].isSet(this.attr);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "attr")) return ;

		this.instance = node.getAttr("instance").getValue();
		this.attr = node.getAttr("attr").getValue();

		ConditionResponse.prototype.load.call(this, node);
	}
} responses.IfIsNotSet = IfIsNotSet;

export class IfDirectEqualsExit extends ConditionResponse {
	constructor() {
		super();
		this.exit = "";
	}

	toString() {
		return `If direct equals exit: "${this.exit}"`;
	}

	check(action) {
		const e = action.book.dictionary.getExit(this.exit);
		if (!e) {
			 
			Output.error(`On IfDirectEqualsExit condition: exit "${this.exit}" not found in dictionary.`);
		}

		return e.responds(action.book.parser.directObjectString);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "exit")) return ;

		this.exit = node.getAttr("exit").getValue();

		ConditionResponse.prototype.load.call(this, node);
	}
} responses.IfDirectEqualsExit = IfDirectEqualsExit;
		
export class IfContains extends ConditionResponse {
	constructor() {
		super();
		this.container = "";
		this.instance = "";
	}

	toString() {
		return `If "${this.container}" contains "${this.instance}"`;
	}

	check(action) {
		const cont = action.book.dictionary.getNouns(this.container)
		if (cont.length === 0) {
			 
			Output.error(`On If contains condition: container "${this.container}" not found in dictionary.`);
		}

		return cont[0].contains(this.instance);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "container")) return ;

		this.instance = node.getAttr("instance").getValue();
		this.container = node.getAttr("container").getValue();

		ConditionResponse.prototype.load.call(this, node);
	}
} responses.IfContains = IfContains;

export class IfNotContains extends ConditionResponse {
	constructor() {
		super();
		this.container = "";
		this.instance = "";
	}

	toString() {
		return `"If ${this.container}" not contains "${this.instance}"`;
	}

	check(action) {
		const cont = action.book.dictionary.getNouns(this.container)
		if (cont.length === 0) {
			
			Output.error(`On IfNotContains condition: container "${this.container}" not found in dictionary.`);
		}

		return !cont[0].contains(this.instance);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "container")) return ;

		this.instance = node.getAttr("instance").getValue();
		this.container = node.getAttr("container").getValue();

		ConditionResponse.prototype.load.call(this, node);
	}
} responses.IfNotContains = IfNotContains;

export class IfCurrentPlaceContains extends ConditionResponse {
	constructor() {
		super();
		this.instance = "";
	}

	toString() {
		return `If current place contains "${this.instance}"`;
	}

	check(action) {
		const cont = action.book.player.container;
		return cont.contains(this.instance);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance")) return ;

		this.instance = node.getAttr("instance").getValue();

		ConditionResponse.prototype.load.call(this, node);
	}
} responses.IfCurrentPlaceContains = IfCurrentPlaceContains;

export class IfCurrentPlaceNotContains extends ConditionResponse {
	constructor() {
		super();
		this.instance = "";
	}

	toString() {
		return `If current place not contains "${this.instance}"`;
	}

	check(action) {
		const cont = action.book.player.container;
		return !cont.contains(this.instance);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance")) return ;

		this.instance = node.getAttr("instance").getValue();

		ConditionResponse.prototype.load.call(this, node);
	}
} responses.IfCurrentPlaceNotContains = IfCurrentPlaceNotContains;

export class IfDirectEquals extends ConditionResponse {
	constructor() {
		super();
		this.instance = "";
	}

	toString() {
		return `If direct equals "${this.instance}"`;
	}

	check(action) {
		const obj = action.book.parser.directObject;
		if (!obj) return false;

		return obj.responds(this.instance);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance")) return ;

		this.instance = node.getAttr("instance").getValue();

		ConditionResponse.prototype.load.call(this, node);
	}
} responses.IfDirectEquals = IfDirectEquals;

export class IfDirectNotEquals extends ConditionResponse {
	constructor() {
		super();
		this.instance = "";
	}

	toString() {
		return `If direct not equals "${this.instance}"`;
	}

	check(action) {
		const obj = action.book.parser.directObject;
		if (!obj) return true;

		return !obj.responds(this.instance);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance")) return ;

		this.instance = node.getAttr("instance").getValue();

		ConditionResponse.prototype.load.call(this, node);
	}
} responses.IfDirectNotEquals = IfDirectNotEquals;

export class IfIndirectEquals extends ConditionResponse {
	constructor() {
		super();
		this.instance = "";
	}

	toString() {
		return `If indirect equals "${this.instance}"`;
	}

	check(action) {
		const obj = action.book.parser.indirectObject;
		if (!obj) return false;

		return obj.responds(this.instance);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance")) return ;

		this.instance = node.getAttr("instance").getValue();

		ConditionResponse.prototype.load.call(this, node);
	}
} responses.IfIndirectEquals = IfIndirectEquals;

export class IfIndirectNotEquals extends ConditionResponse {
	constructor() {
		super();
		this.instance = "";
	}

	toString() {
		return `If indirect equals "${this.instance}"`;
	}

	check(action) {
		const obj = action.book.parser.indirectObject;
		if (!obj) return true;

		return !obj.responds(this.instance);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance")) return ;

		this.instance = node.getAttr("instance").getValue();

		ConditionResponse.prototype.load.call(this, node);
	}
} responses.IfIndirectNotEquals = IfIndirectNotEquals;

export class IfVariableEquals extends ConditionResponse {
	constructor() {
		super();
		this.instance = "";
		this.variable = "";
		this.value = "";
	}

	toString() {
		return `If variable "${this.variable}" equals to "${this.value}."`;
	}

	check(action) {
		const obj = action.book.dictionary.getNouns(this.instance);

		if (obj.length === 0) {
			
			Output.error(`On condition "IfVariableEquals" instance "${this.instance}" not found in dictionary.`);
		}

		return obj[0].getVariable(this.variable) === this.value;
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "variable", "value")) return ;

		this.instance = node.getAttr("instance").getValue();
		this.variable = node.getAttr("variable").getValue();
		this.value = node.getAttr("value").getValue();

		ConditionResponse.prototype.load.call(this, node);
	}
} responses.IfVariableEquals = IfVariableEquals;

export class IfConnectionExists extends ConditionResponse {
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
			Output.error(`On condition "IfConnectionExists" instance "${this.instance}" not found in dictionary.`);
		}

		return place[0].getConnection(this.exit) != null;
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "exit")) return ;

		this.instance = node.getAttr("instance").getValue();
		this.exit = node.getAttr("exit").getValue();

		ConditionResponse.prototype.load.call(this, node);
	}

} responses.IfConnectionExists = IfConnectionExists;

export class IfConnectionNotExists extends ConditionResponse {
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
			Output.error(`On condition "IfConnectionNotExists" instance "${this.instance}" not found in dictionary.`);
		}

		return place[0].getConnection(this.exit) == null;
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "exit")) return ;

		this.instance = node.getAttr("instance").getValue();
		this.exit = node.getAttr("exit").getValue();

		ConditionResponse.prototype.load.call(this, node);
	}

} responses.IfConnectionNotExists = IfConnectionNotExists;

export class IfActionEquals extends ConditionResponse {
	constructor() {
		super();
		this.actionName = "";
	}

	toString() {
		return `If action equals "${this.actionName}"`;
	}

	check(action) {
		return this.actionName === action.constructor.name;
	}

	load(node) {
		if (!Utils.expectedAttributes(node, "action")) return ;
		this.actionName = node.getAttr("action").getValue();
		
		ConditionResponse.prototype.load.call(this, node);
	}
} responses.IfActionEquals = IfActionEquals;
