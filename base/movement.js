export class Connection {
	constructor() {
		this.exit = "";
		this.destiny = "";
	}

	toString() {
		return `${this.exit} --> ${this.destiny}`;
	}
	
	load(node) {
		this.exit = node.getAttr("exit").getValue();
		this.destiny = node.getAttr("destiny").getValue();
	}
};
