import { DFMLElement } from "../dfml/js/main/element.js";
import { DFMLValue } from "../dfml/js/main/value.js";
import { ActionResponse } from "./actionresponse.js";
import { Output } from "./output.js";

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

	execute(action) {
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

	execute(action) {
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

	execute(action) {
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

	execute(action) {
		list = action.book.dictionary.getNouns(this.instance);
		if (list.length === 0) {
			Output.error(`On Variable response: noun "${this.instance}" not found in dictionary.`);
		}

		const obj = list[0];

		obj.setVariable(this.variable, this.set);
	}

	load(node) {
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

	execute(action) {
		const objList = action.book.dictionary.getNouns(this.instance);
		if (objList.length === 0) {
			Output.error(`On AppendName response: noun "${this.instance}" not found in dictionary.`);
		}

		objList[0].appendName(this.name);
	}

	load(node) {
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

	execute(action) {
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
		this.instance = node.getAttr("instance").getValue();
		this.destiny = node.getAttr("destiny").getValue();
	}
} responses.Move = Move;

export class Tip extends ActionResponse {
	constructor() {
		super();
		this.message = "";
	}

	toString() {
		return `Show tip "${this.message}"`;
	}

	execute(action) {
		Help.tip(this.message);
	}

	load(node) {
		if (node.children.length === 1) {
			if (node.children[0].getElementType() === DFMLElement.DATA) {
				if (node.children[0].getValue().getType() === DFMLValue.STRING) {
					this.message = node.children[0].getValue();
					return ;
				}
			}
		}

		Output.error(`On Tip Response: Extra element found.`);
	}
} responses.Tip = Tip;

export class TipOnce extends ActionResponse {
	constructor() {
		super();
		this.message = "";
		this.instance = "";
	}

	toString() {
		return `Show tip "${this.message} once"`;
	}

	execute(action) {
		let objList = action.book.dictionary.getNouns(this.instance);
		if (objList.length === 0) return null;
		Help.tipOnce(objList[0], this.message);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue();

		if (node.children.length === 1) {
			if (node.children[0].getElementType() === DFMLElement.DATA) {
				if (node.children[0].getValue().getType() === DFMLValue.STRING) {
					this.message = node.children[0].getValue();
					return ;
				}
			}
		}
		
		Output.error(`On TipOnce Response: Extra element found.`);
	}
} responses.TipOnce = TipOnce;

export class Execute extends ActionResponse {
	constructor() {
		super();
		this.sentence = "";
	}

	toString() {
		return `'Execute "${this.sentence}" sentence`;
	}

	execute(action) {
		action.book.execute(this.sentence);
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
		this.instance = ""
		this.exit = ""
		this.destiny = ""
	}

	toString() {
		return `Add connection to ${this.instance}: ${this.exit} -> ${this.destiny}`;
	}

	execute(action) {
		let objList = action.book.dictionary.getNouns(this.instance)
		if (objList.length === 0) {
			Output.error(`On AddConnection response: noun "${this.instance}" not found in dictionary.`);
		}

		const conn = Connection();
		conn.exit = this.exit;
		conn.destiny = this.destiny;
		objList[0].addConnection(conn);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue();
		this.exit = node.getAttr("exit").getValue();
		this.destiny = node.getAttr("destiny").getValue();
	}
} responses.AddConnection = AddConnection;

export class ShowTitle extends ActionResponse {

	constructor() {
		super();
	}

	toString() {
		return "Show game title";
	}

	execute(action) {
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

	execute(action) {
		c = action.book.dictionary.conversation(this.owner);
		c.start(action);
	}

	load(node) {
		this.owner = node.getAttr("owner");
	}
} responses.RunConversation = RunConversation;

export class Pause extends ActionResponse {

	constructor() {
		super();
	}

	toString() {
		return "Pause";
	}

	execute(action) {
		action.book.input.pause();
	}

	load(node) {}
} responses.Pause = Pause;

export class Clear extends ActionResponse {

	constructor() {
		super();
	}

	toString() {
		return "Clear";
	}

	execute(action) {
		Output.clear();
	}

	load(node) {}
} responses.Clear = Clear;

export class EndGame extends ActionResponse {
	constructor() {
		super();
		this.result = ""
		this.message = ""
	}

	toString() {
		return "End game";
	}

	execute(action) {
		let victory = true
		if (this.result === "victory") victory = true;
		else if (this.result === "defeat") victory = false;
		else {
			Output.error(`On EndGame: expected "victory" or "defeat" value on result attr.`);
		}

		//action.book.dictionary.gameOver.run(ResultType.VICTORY if victory else ResultType.DEFEAT, this.message)
	}

	load(node) {
		this.result = node.getAttr("result");

		if (node.children.length === 1) {
			if (node.children[0].getElementType() === DFMLElement.DATA) {
				if (node.children[0].getValue().getType() === DFMLValue.STRING) {
					this.message = node.children[0].getValue();
					return ;
				}
			}
		}
	}
} responses.EndGame = EndGame;
