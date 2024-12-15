import { Action } from "./action.js";
import { Output } from "./output.js";

export const debugActions = {};

function debugPrint(msg) {
	Output.print(msg, {
		fontFamily: "'Courier New', Courier, monospace"
	});
}

export class Info extends Action {

	constructor() {
		super();

		this.nounList = [];
	}

	async init() {

		this.nounList = this.book.dictionary.getNouns(this.book.parser.directObjectString)
		if (this.nounList === 0) {
			debugPrint(`Nouns not found in dictionary.`);
			return false;
		}

		return true;
	}

	async check() {
		return true;
	}

	async carryOut() {
		for (const n of this.nounList)
			this.printNounInfo(n);

		debugPrint("--------------------");
	}

	async report() {
	}

	printNounInfo(noun) {
		debugPrint("--------------------");
		debugPrint(`Names: ${Array.from(noun.names).join(", ")}`);
		debugPrint(`Container: ${noun.container ? noun.container.getName() : 'null'}`);
		if (noun.attrs)
			debugPrint(`Attributes: ${Array.from(noun.attrs).join(", ")}`);
		if (noun.variables)
			debugPrint(`Variables: ${Object.entries(noun.variables)
				.map(([key, value]) => `${key}: "${value}"`)
				.join(", ")}`);
		if (noun.connections) {
			debugPrint(`Connections:`);
			for (const c of noun.connections)
				debugPrint(c.toString());
		}
	}

	responses() {
		return [];
	}
} debugActions.Info = Info;

export class Tree extends Action {

	constructor() {
		super();
		this.nounList = [];
	}

	init() {
		for (const n of this.book.dictionary.getNouns("")) {
			if (!n.container) {
				this.nounList.push(n);
			}
		}
		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		debugPrint('Nouns:');
		for (const n of this.nounList) {
			this.printNode(n, "");
		}
	}

	report() {
	}

	printNode(noun, indent) {
		debugPrint(`${indent}${noun.names}`);
		for (const n of noun.children())
			this.printNode(n, indent + "---");
	}

	responses() {
		return [];
	}
} debugActions.Tree = Tree;

export class TreeObject extends Tree {
	init() {
		for (const n of this.book.dictionary.getNouns(this.book.parser.directObjectString)) {
			this.nounList.push(n);
		}

		if (this.nounList.length === 0)
			debugPrint(`Tree: No results.`);
		
		return true;
	}
} debugActions.TreeObject = TreeObject;

export class Attr extends Action {

	constructor() {
		super();
		this.obj = null;
		this.attrs = "";
		this.command = "";
	}

	init() {
		const lst = this.book.dictionary.getNouns(this.book.parser.directObjectString)
		if (lst.length === 0) {
			debugPrint(`Attr: noun not found in dictionary.`);
			return false;
		}

		this.command = this.book.parser.keyword.toLowerCase();

		this.obj = lst[0];
		return true;
	}

	check() {

		if (this.command !== "set" && this.command !== "unset") {
			debugPrint(`Attr: usage: 'attr <obj> set/unset <attr list>'.`);
			return false;
		}
		return true;
	}

	carryOut() {
		const lst = [];
		for (const a of this.book.parser.indirectObjectString.split(" "))
			if (a.trim() !== "")
				lst.push(a);

		if (this.command === "set") {
			this.obj.set(lst);
			debugPrint(`setted "${Array.from(lst).join(', ')}" to "${this.obj.getName()}".`);
		} if (this.command === "unset") {
			this.obj.unset(lst);
			debugPrint(`unsetted "${Array.from(lst).join(', ')}" to "${this.obj.getName()}".`);
		}
	}

	report() {
	}

	responses() {
		return []
	}
} debugActions.Attr = Attr;

export class Move extends Action {
	constructor() {
		super();
		
		this.object = null;
		this.dest = null;
	}

	async init() {

		// Direct object
		let name = this.book.parser.directObjectString;
		let lst = this.book.dictionary.getNouns(name)
		if (lst.length === 0) {
			debugPrint(`Move: "${name}" not found in dictionary.`);
			return false;
		}

		this.object = await this.book.dictionary.objectChooserDialog.execute(lst);
		if (!this.object) return false;

		name = this.book.parser.indirectObjectString;
		lst = this.book.dictionary.getNouns(name);
		if (lst.length === 0) {
			debugPrint(`Move: "${name}" not found in dictionary.`);
			return false;
		}

		this.dest = await this.book.dictionary.objectChooserDialog.execute(lst);
		if (!this.dest) return false;

		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		this.object.container = this.dest;
		debugPrint(`"${this.object.getName()}" moved to "${this.dest.getName()}".`);
	}

	report() {
	}

	responses() {
		return [];
	}
} debugActions.Move = Move;

export class Root extends Action {
	constructor() {
		super();
		this.object = null;
	}

	async init() {

		const name = this.book.parser.directObjectString;
		const lst = this.book.dictionary.getNouns(name);

		if (lst.length === 0) {
			debugPrint(`Root: "${name}" not found in dictionary.`);
			return false;
		}

		this.object = await this.book.dictionary.objectChooserDialog.execute(lst);
		if (!this.object) return false;

		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		this.object.container = null;
		debugPrint(`"${this.object.getName()}" moved to ROOT.`);
	}

	report() {
	}

	responses() {
		return [];
	}
} debugActions.Root = Root;

export class VerbInfo extends Action {
	constructor() {
		super();
		this.verbList = [];
	}

	init() {
		let name = this.book.parser.directObjectString;

		if (name === "all") {
			this.verbList = this.book.dictionary.getVerbs();
		} else {
			this.verbList = this.book.dictionary.getVerbs(name);
		}

		if (this.verbList.length === 0) {
			debugPrint(`Verb: "${name}" not found in dictionary.`);
			debugPrint(`Verb: use: "verb all" to list all verbs.`);
			return false;
		}
		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		Output.print('---------------------------');
		for (const v of this.verbList) {
			this.verbInfo(v);
			Output.print('---------------------------');
		}
	}

	report() {
	}

	responses() {
		return [];
	}

	verbInfo(verb) {
		debugPrint(`Action: "${verb.action.name}" Syntax: "${verb.syntax}":`);
		debugPrint(`${verb.names}`);
	}
} debugActions.VerbInfo = VerbInfo;
