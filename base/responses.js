import { DFMLElement } from "../dfml/js/main/element.js";
import { DFMLValue } from "../dfml/js/main/value.js";
import { Action } from "./action.js";
import { ActionResponse } from "./actionresponse.js";
import { Output } from "./output.js";

export const responses = {};

export class Print extends ActionResponse {

	constructor() {
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

		this.style = node.getAttr("style").getValue().getValue();

		if (node.children.length === 1) {
			if (node.children[0].getElementType() === DFMLElement.DATA) {
				if (node.children[0].getValue().getType() === DFMLValue.STRING) {
					this.message = node.children[0].getValue().getValue();
					return ;
				}
			}
		}
		// TODO: Error
	}
} responses.Print = Print;

export class Append extends ActionResponse {
	constructor() {
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

		this.style = node.getAttr("style").getValue().getValue();

		if (node.children.length === 1) {
			if (node.children[0].getElementType() === DFMLElement.DATA) {
				if (node.children[0].getValue().getType() === DFMLValue.STRING) {
					this.message = node.children[0].getValue().getValue();
					return ;
				}
			}
		}
		// TODO: Error
	}
} responses.Append = Append;

export class Attr extends ActionResponse {
	constructor() {
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
		objList = action.dictionary.getNouns(this.instance);
		if (objList.length === 0) {
			//TODO: error 'On Set response: noun "{this.instance}" not found in dictionary.'
		}

		obj = objList[0];

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
		this.instance = node.getAttr("instance").getValue().getValue();
		this.set = node.getAttr("set").getValue().getValue();
		this.unset = node.getAttr("unset").getValue().getValue();
	}
} responses.Attr = Attr;

export class Variable extends ActionResponse {
	constructor() {
		this.instance = "";
		this.variable = "";
		this.set = "";
	}

	toString() {
		return `Set "${this.set}" to variable "${this.variable}", instance: "${this.instance}".`;
	}

	execute(action) {
		list = action.dictionary.getNouns(this.instance);
		if (list.length === 0) {
			// TODO: 'On Variable response: noun "{this.instance}" not found in dictionary.'
		}

		const obj = list[0];

		obj.setVariable(this.variable, this.set);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue().getValue();
		this.variable = node.getAttr("variable").getValue().getValue();
		this.set = node.getAttr("set").getValue().getValue();
	}
} responses.Variable = Variable;

export class AppendName extends ActionResponse {
	constructor() {
		this.instance = ""
		this.name = ""
	}

	toString() {
		return `Append name "${this.name}" to "${this.instance}"`;
	}

	execute(action) {
		let objList = action.dictionary.getNouns(this.instance);
		if (objList.length === 0) {
			// TODO: 'On AppendName response: noun "{this.instance}" not found in dictionary.'
		}

		obj = objList[0];
		obj.appendName(this.name);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue().getValue();
		this.name = node.getAttr("name").getValue().getValue();
	}
} responses.AppendName = AppendName;

export class Move extends ActionResponse {
	constructor() {
		this.instance = ""
		this.destiny = ""
	}

	toString() {
		return `Move "${this.instance}" to "${this.destiny}"`;
	}

	#getObj(action, name) {
		objList = action.dictionary.getNouns(name);
		if (objList.length === 0) return null;
		return objList[0];
	}

	execute(action) {
		obj = this.getObj(action, this.instance)
		if (!obj) {
			// TODO: 'On Move response: noun "{this.instance}" not found in dictionary.'
		}

		dest = this.getObj(action, this.destiny)
		if (!dest) {
			// TODO: 'On Move response: destiny "{this.destiny}" not found in dictionary.'
		}

		obj.container = dest;
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue().getValue();
		this.destiny = node.getAttr("destiny").getValue().getValue();
	}
} responses.Move = Move;

export class Tip extends ActionResponse {
	constructor() {
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
					this.message = node.children[0].getValue().getValue();
					return ;
				}
			}
		}
		// TODO: Error
	}
} responses.Tip = Tip;

export class TipOnce extends ActionResponse {
	constructor() {
		this.message = "";
		this.instance = "";
	}

	toString() {
		return `Show tip "${this.message} once"`;
	}

	execute(action) {
		let objList = action.dictionary.getNouns(this.instance);
		if (objList.length === 0) return null;
		Help.tipOnce(objList[0], this.message);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue().getValue();

		if (node.children.length === 1) {
			if (node.children[0].getElementType() === DFMLElement.DATA) {
				if (node.children[0].getValue().getType() === DFMLValue.STRING) {
					this.message = node.children[0].getValue().getValue();
					return ;
				}
			}
		}
		// TODO: Error
	}
} responses.TipOnce = TipOnce;

export class Execute extends ActionResponse {
	constructor() {
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
		// TODO: Error
	}
} responses.Execute = Execute;

export class AddConnection extends ActionResponse {
	constructor() {
		this.instance = ""
		this.exit = ""
		this.destiny = ""
	}

	toString() {
		return `Add connection to ${this.instance}: ${this.exit} -> ${this.destiny}`;
	}

	execute(action) {
		let objList = action.dictionary.getNouns(this.instance)
		if (objList.length === 0) {
			// TODO: 'On AddConnection response: noun "{this.instance}" not found in dictionary.')
		}

		const conn = Connection();
		conn.exit = this.exit;
		conn.destiny = this.destiny;
		objList[0].addConnection(conn);
	}

	load(node) {
		this.instance = node.getAttr("instance").getValue().getValue();
		this.exit = node.getAttr("exit").getValue().getValue();
		this.destiny = node.getAttr("destiny").getValue().getValue();
	}
} responses.AddConnection = AddConnection;

export class ShowTitle extends ActionResponse {
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
		this.owner = "";
	}
		
	toString() {
		return `Run Conversation with '${this.owner}'`;
	}

	execute(action) {
		c = action.dictionary.conversation(this.owner);
		c.start(action);
	}

	load(node) {
		this.owner = node.getAttr("owner");
	}
} responses.RunConversation = RunConversation;

export class Pause extends ActionResponse {

	toString() {
		return "Pause";
	}

	execute(action) {
		action.book.pause();
	}

	load(node) {}
} responses.Pause = Pause;

export class Clear extends ActionResponse {
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
			// TODO: 'On EndGame: expected "victory" or "defeat" value on result attr.')
		}

		//action.dictionary.gameOver.run(ResultType.VICTORY if victory else ResultType.DEFEAT, this.message)
	}

	load(node) {
		this.result = node.getAttr("result");

		if (node.children.length === 1) {
			if (node.children[0].getElementType() === DFMLElement.DATA) {
				if (node.children[0].getValue().getType() === DFMLValue.STRING) {
					this.message = node.children[0].getValue().getValue();
					return ;
				}
			}
		}
	}
} responses.EndGame = EndGame;
