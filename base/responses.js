import { DFMLElement } from "../dfml/js/main/element.js";
import { DFMLValue } from "../dfml/js/main/value.js";
import { ActionResponse } from "./actionresponse.js";
import { Output } from "./output.js";
import { Help } from "./help.js";
import { Connection } from "./movement.js";
import { ResultType } from "./gameover.js";
import { loadConditionsAndResponses } from "./eventloader.js";
import { Utils } from "./utils.js";

export const responses = {};

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

export class Variable extends ActionResponse {
	constructor() {
		super();
		this.instance = "";
		this.variable = "";
		this.set = "";
	}

	toString() {
		return `Set "${this.set}" to variable "${this.variable}", instance: "${this.instance}".`;
	}

	async execute(action) {
		list = action.book.dictionary.getNouns(this.instance);
		if (list.length === 0) {
			Output.error(`On Variable response: noun "${this.instance}" not found in dictionary.`);
		}

		const obj = list[0];

		obj.setVariable(this.variable, this.set);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "instance", "variable", "set")) return ;

		this.instance = node.getAttr("instance").getValue();
		this.variable = node.getAttr("variable").getValue();
		this.set = node.getAttr("set").getValue();
	}
} responses.Variable = Variable;

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

export class EndGame extends ActionResponse {
	constructor() {
		super();
		this.result = "";
		//this.message = "";
		this.responses = [];
		this.conditions = [];
	}

	toString() {
		return "End game";
	}

	async execute(action) {
		let victory = true;
		if (this.result === "victory") victory = true;
		else if (this.result === "defeat") victory = false;
		else {
			Output.error(`On EndGame: expected "victory" or "defeat" value on result attr.`);
		}

		await action.book.dictionary.gameover.run(
			victory ? ResultType.VICTORY : ResultType.DEFEAT,
			action, this.conditions, this.responses
		);
	}

	load(node) {

		if (!Utils.expectedAttributes(node, "result")) return ;

		this.result = node.getAttr("result").getValue();

		loadConditionsAndResponses(node, this.conditions, this.responses);
	}
} responses.EndGame = EndGame;

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
