import { Action } from "./action.js"

/**
 * Single action takes no arguments. Usually represents verb like "jump", "scream".
 *	By default, SingleAction fires response: "nothing-happens"
 *
 *	Responses:
 *	nothing-happens

 * @export
 * @class SingleAction
 * @extends {Action}
 */
export class SingleAction extends Action {

	constructor() {
		super();
	}

	init() {
		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		
	}

	report() {
		this.fireResponse("nothing-happens");
	}

	responses() {
		return ["nothing-happens"];
	}
}

/**
 * DefaultAction takes one argument (direct object).
 * By default, fires response "nothing-happens"
 * Responses:
 * direct-not-found
 * direct-is-the-player
 * nothing-happens
 *
 * @export
 * @class DefaultAction
 * @extends {Action}
 */
export class DefaultAction extends Action {

	constructor() {
		super();
	}

	init() {
		let lst = this.game.player.children(this.parser.directObjectString);
		lst = lst.concat(this.game.player.container.children(this.parser.directObjectString));

		if (lst.length === 0) {
			return this.fireResponse("direct-not-found");
		}

		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst);
		if (!this.parser.directObject) {
			return false;
		}

		this.sendEventLater(this.parser.directObject);

		return true;
	}

	check() {
		if (this.parser.directObject == this.game.player) {
			return this.fireResponse("direct-is-the-player")
		}
		return true;
	}

	carryOut() {
		
	}

	report() {
		this.fireResponse("nothing-happens")
	}

	responses() {
		return ["nothing-happens", "direct-not-found", "direct-is-the-player"]
	}
}

export class UnknownVerb extends Action {

	constructor() {
		super();
	}

	init() {
		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		this.fireResponse("unknown-verb")
	}

	report() {
		
	}

	responses() {
		return ["unknown-verb"]
	}
}

export class Clear extends Action {

	constructor() {
		super();
	}

	init() {
		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		Output.clear()
	}

	report() {
		
	}

	responses() {
		return []
	}
}

export class SaveGame extends Action {

	constructor() {
		super();
	}

	init() {
		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		if (this.game.saveGame()) {
			this.fireResponse("game-saved")
		} else {  this.fireResponse("cancel-error") }
	}

	report() {
		
	}

	responses() {
		return ["game-saved", "cancel-error"]
	}
}

export class LoadGame extends Action {

	constructor() {
		super();
	}

	init() {
		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		if (this.game.loadGame()) {
			this.fireResponse("game-loaded")
		} else {  this.fireResponse("cancel-error") }
	}

	report() {
		
	}

	responses() {
		return ["game-loaded", "cancel-error"]
	}
}

export class Inventory extends Action {

	constructor() {
		super();
	}

	init() {
		this.sendEventLater(this.game.player)
		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		let lst = this.game.player.childs()
		if (lst.length === 0) { this.fireResponse("inventory-is-empty")
		} else { 
			this.dictionary.inventoryDialog.execute(lst)
		}

		this.sendEventLater(this.game.player)
	}

	report() {
		
	}

	responses() {
		return ["inventory-is-empty"]
	}
}


export class ExamineObject extends Action {

	constructor() {
		super();
	}

	init() {

		let lst = this.game.player.childs(this.parser.directObjectString)
		lst.extend(this.game.player.container.childs(this.parser.directObjectString))

		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.directObject) return false

		this.sendEventLater(this.parser.directObject)

		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		this.sendEventLater(this.parser.directObject) }

	report() {
		
	}

	responses() {
		return ["direct-not-found"]
	}
}

export class LookAround extends Action {

	constructor() {
		super();
	}

	init() {
		this.place = this.game.player.container
		this.sendEventLater(this.place)

		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		// Print the description of the place
		Output.print(this.place.name, "bold: true")
		this.sendEventLater(this.place)
	}

	report() {
		nouns = []
		proppers = []
		this.place.children().forEach(n => {
			if (n === this.game.player) return;
			if (n.isSet("scene")) return;
			if (n.isSet("propper")) proppers.push(n);
			else nouns.push(n);
		});

		if (nouns.length !== 0) {
			Output.print("")
			this.dictionary.seeListDialog.execute(nouns);
		}

		if (proppers.length !== 0) {
			Output.print("")
			this.dictionary.propperListDialog.execute(proppers)
		}
	}
	
	responses() {
		return []
	}
}

export class LookInside extends Action {

	constructor() {
		super();
	}

	init() {

		let lst = this.game.player.childs(this.parser.directObjectString)
		lst.extend(this.game.player.container.childs(this.parser.directObjectString))

		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.directObject) return false

		this.sendEventLater(this.parser.directObject)

		return true;
	}

	check() {
		if (this.parser.directObject == this.game.player)
			return this.fireResponse("direct-is-the-player")
		if (!this.parser.directObject.isSet("container"))
			return this.fireResponse("direct-is-not-container")
		if (this.parser.directObject.isSet("closed"))
			return this.fireResponse("direct-is-closed")

		return true;
	}

	carryOut() {
		childs = this.parser.directObject.childs()
		if (childs.length === 0) {
			this.fireResponse("container-is-empty")
		} else { 
			this.dictionary.lookInsideDialog.execute(childs)
		}

		this.sendEventLater(this.parser.directObject)
	}

	report() {
		
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "direct-is-not-container",
					"direct-is-closed", "container-is-empty"]
	}
}

export class TakeObject extends Action {

	constructor() {
		super();
	}

	init() {
		// Get the object from the current place
		let lst = this.game.player.container.childs(this.parser.directObjectString)
		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.directObject) return false

		this.sendEventLater(this.parser.directObject)

		return true;
	}

	check() {
		if (this.parser.directObject == this.game.player)
			return this.fireResponse("direct-is-the-player")
		if (this.parser.directObject.isSet("fixed"))
			return this.fireResponse("direct-is-fixed")
		if (this.parser.directObject.isSet("heavy"))
			return this.fireResponse("direct-is-heavy")

		return true;
	}

	carryOut() {
		// Move the DO to player's inventory
		this.parser.directObject.container = this.game.player
		this.parser.directObject.set(["taken"])
		this.sendEventLater(this.parser.directObject)
	}

	report() {
		this.fireResponse("direct-taken")
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "direct-is-fixed",
					"direct-is-heavy", "direct-taken"]
	}
}

export class LeaveObject extends Action {

	constructor() {
		super();
	}

	init() {
		let lst = this.game.player.childs(this.parser.directObjectString)
		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.directObject) return false

		this.sendEventLater(this.parser.directObject)

		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		noun = this.parser.directObject
		noun.container = this.game.player.container
		noun.set(["leaved"])

		this.sendEventLater(noun)
	}

	report() {
		this.fireResponse("direct-left")
	}

	responses() {
		return ["direct-not-found", "direct-left"]
	}
}

export class TakeFrom extends Action {

	constructor() {
		super();
	}

	init() {

		let lst = this.game.player.childs(this.parser.indirectObjectString)
		lst.extend(this.game.player.container.childs(this.parser.indirectObjectString))

		if (lst.length === 0) return this.fireResponse("indirect-not-found")

		this.parser.indirectObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.indirectObject) return false

		this.sendEventLater(this.parser.indirectObject)

		return true;
	}

	check() {

		container = this.parser.indirectObject;

		if (!container.isSet("container"))
			return this.fireResponse("indirect-is-not-container")
		if (container.isSet("closed"))
			return this.fireResponse("indirect-is-closed")

		let lst = container.childs(this.parser.directObjectString)
		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.directObject) return false

		// Send the before event now
		return this.parser.directObject.doBefore()
	}

	carryOut() {
		// Move the noun to the player's inventory
		this.parser.directObject.container = this.game.player
		this.parser.directObject.set(["taken"])
		this.sendEventLater(this.parser.indirectObject)
		this.sendEventLater(this.parser.directObject)
	}

	report() {
		this.fireResponse("direct-taken")
	}

	responses() {
		return ["indirect-not-found", "indirect-is-not-container", "indirect-is-closed",
					"direct-not-found", "direct-taken"]
	}
}

export class LeaveIn extends Action {

	constructor() {
		super();
	}

	init() {
		// The direct object in inventory (object)
		let lst = this.game.player.childs(this.parser.directObjectString)
		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.directObject) return false

		// The indirect object in the inventory or the current place (container)
		lst = this.game.player.childs(this.parser.indirectObjectString)
		lst.extend(this.game.player.container.childs(this.parser.indirectObjectString))
		if (lst.length === 0) return this.fireResponse("indirect-not-found")

		this.parser.indirectObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.indirectObject) return false

		this.sendEventLater(this.parser.directObject)
		this.sendEventLater(this.parser.indirectObject)

		return true;
	}

	check() {

		if (this.parser.indirectObject == this.game.player)
			return this.fireResponse("indirect-is-the-player")
		if (!this.parser.indirectObject.isSet("container"))
			return this.fireResponse("indirect-is-not-container")
		if (this.parser.indirectObject.isSet("closed"))
			return this.fireResponse("indirect-is-closed")

		return true;
	}

	carryOut() {
		// Move the object to the container
		this.parser.directObject.container = this.parser.indirectObject
		this.parser.directObject.set(["leaved"])
		this.sendEventLater(this.parser.directObject)
		this.sendEventLater(this.parser.indirectObject)
	}

	report() {
		this.fireResponse("direct-leaved")
	}

	responses() {
		return ["direct-not-found", "indirect-not-found", "indirect-is-the-player",
					"indirect-is-not-container", "indirect-is-closed", "direct-leaved"]
	}
}

export class PullObject extends Action {

	constructor() {
		super();
	}

	init() {

		let lst = this.game.player.container.childs(this.parser.directObjectString)
		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.directObject) return false

		this.sendEventLater(this.parser.directObject)

		return true;
	}

	check() {
		if (this.parser.directObject == this.game.player)
			return this.fireResponse("direct-is-the-player")
		if (this.parser.directObject.isSet("fixed"))
			return this.fireResponse("direct-is-fixed")
		return true;
	}

	carryOut() {
		this.sendEventLater(this.parser.directObject)
	}

	report() {
		this.fireResponse("nothing-happens")
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "direct-is-fixed", "nothing-happens"]
	}
}

export class PushObject extends Action {

	constructor() {
		super();
	}

	init() {

		let lst = this.game.player.container.childs(this.parser.directObjectString)
		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.directObject) return false

		this.sendEventLater(this.parser.directObject)

		return true;
	}

	check() {
		if (this.parser.directObject == this.game.player)
			return this.fireResponse("direct-is-the-player")
		if (this.parser.directObject.isSet("fixed"))
			return this.fireResponse("direct-is-fixed")
		return true;
	}

	carryOut() {
		this.sendEventLater(this.parser.directObject)
	}

	report() {
		this.fireResponse("nothing-happens")
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "direct-is-fixed",
						"nothing-happens"]
	}
}


export class OpenObject extends Action {

	constructor() {
		super();
	}

	init() {
		let lst = this.game.player.childs(this.parser.directObjectString)
		lst.extend(this.game.player.container.childs(this.parser.directObjectString))

		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst)

		if (!this.parser.directObject) return false

		this.sendEventLater(this.parser.directObject)

		return true;
	}

	check() {

		if (this.parser.directObject == this.game.player)
			return this.fireResponse("direct-is-the-player")
		if (!this.parser.directObject.isSet("closable"))
			return this.fireResponse("direct-is-not-closable")
		if (!this.parser.directObject.isSet("closed"))
			return this.fireResponse("direct-is-open")

		return true;
	}

	carryOut() {
		this.parser.directObject.unset(["closed"])
		this.sendEventLater(this.parser.directObject)
	}

	report() {
		this.fireResponse("direct-was-opened")
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "direct-is-not-closable",
					"direct-is-open", "direct-was-opened"]
	}
}


export class CloseObject extends Action {

	constructor() {
		super();
	}

	init() {
		let lst = this.game.player.childs(this.parser.directObjectString)
		lst.extend(this.game.player.container.childs(this.parser.directObjectString))

		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst)

		if (!this.parser.directObject) return false

		this.sendEventLater(this.parser.directObject)

		return true;
	}

	check() {

		if (this.parser.directObject == this.game.player)
			return this.fireResponse("direct-is-the-player")
		if (!this.parser.directObject.isSet("closable"))
			return this.fireResponse("direct-is-not-closable")
		if (this.parser.directObject.isSet("closed"))
			return this.fireResponse("direct-is-closed")

		return true;
	}

	carryOut() {
		this.parser.directObject.set(["closed"])
		this.sendEventLater(this.parser.directObject)
	}

	report() {
		this.fireResponse("direct-was-closed")
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "direct-is-not-closable",
						"direct-is-closed", "direct-was-closed"]
	}
}


export class OpenWith extends Action {

	constructor() {
		super();
	}

	init() {

		// Direct object in inventory or current place
		let lst = this.game.player.childs(this.parser.directObjectString)
		lst.extend(this.game.player.container.childs(this.parser.directObjectString))

		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.directObject) return false

		// Indirect object in inventory
		lst = this.game.player.childs(this.parser.indirectObjectString)

		if (lst.length === 0) return this.fireResponse("indirect-not-found")

		this.parser.indirectObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.indirectObject) return false

		this.sendEventLater(this.parser.directObject)
		this.sendEventLater(this.parser.indirectObject)

		return true;
	}

	check() {

		if (this.parser.directObject == this.game.player)
			return this.fireResponse("direct-is-the-player")
		if (this.parser.indirectObject == this.game.player)
			return this.fireResponse("indirect-is-the-player")

		if (!this.parser.directObject.isSet("closable"))
			return this.fireResponse("direct-is-not-closable")

		if (!this.parser.directObject.isSet("closed"))
			return this.fireResponse("direct-is-open")

		return true;
	}

	carryOut() {
		this.sendEventLater(this.parser.directObject)
		this.sendEventLater(this.parser.indirectObject)
	}

	report() {
		this.fireResponse("nothing-happens")
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "indirect-is-the-player",
					"direct-is-not-closable", "direct-is-open", "nothing-happens"]
	}
}


export class CloseWith extends Action {

	constructor() {
		super();
	}

	init() {

		// Direct object in inventory or current place
		let lst = this.game.player.childs(this.parser.directObjectString)
		lst.extend(this.game.player.container.childs(this.parser.directObjectString))

		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.directObject) return false

		// Indirect object in inventory
		lst = this.game.player.childs(this.parser.indirectObjectString)

		if (lst.length === 0) return this.fireResponse("indirect-not-found")

		this.parser.indirectObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.indirectObject) return false

		this.sendEventLater(this.parser.directObject)
		this.sendEventLater(this.parser.indirectObject)

		return true;
	}

	check() {

		if (this.parser.directObject == this.game.player)
			return this.fireResponse("direct-is-the-player")
		if (this.parser.indirectObject == this.game.player)
			return this.fireResponse("indirect-is-the-player")

		if (!this.parser.directObject.isSet("closable"))
			return this.fireResponse("direct-is-not-closable")

		if (this.parser.directObject.isSet("closed"))
			return this.fireResponse("direct-is-closed")

		return true;
	}

	carryOut() {
		this.sendEventLater(this.parser.directObject)
		this.sendEventLater(this.parser.indirectObject)
	}

	report() {
		this.fireResponse("nothing-happens")
	}

	responses() {
		return ["direct-not-found", "indirect-not-found", "direct-is-the-player",
					"indirect-is-the-player", "direct-is-not-closable",
							"direct-is-closed", "nothing-happens"]
	}
}


export class GoTo extends Action {

	constructor() {
		super();
	}

	init() {

		// Get exit from dictionary
		exit = this.dictionary.exit(this.parser.directObjectString)
		if (!exit) return this.fireResponse("exit-not-exists")

		// Get connection from dictionary
		this.conn = this.game.player.container.connection(exit)
		if (!this.conn) return this.fireResponse("exit-not-found")

		this.sendEventLater(this.game.player.container)

		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		// Get the destiny
		let nouns = this.dictionary.nouns(this.conn.destiny)
		if(nouns.length === 0) {
			// TODO error
			//raise DragonflyException(f'Called GoTo action from "{this.game.player.container.name}": Destiny "{this.conn.destiny}" not found on exit "{this.conn.exit}"')
		}
		// Move the player
		this.game.player.container = nouns[0]

		// Visibility behavior
		if (this.game.getProperty("look-around") === "always") {
			// Look around verb
			let v = this.dictionary.verbByAction("LookAround")
			this.game.execute(v.name)
		}
		
		this.sendEventLater(this.game.player.container)
	}

	report() {
		
	}
	
	responses() {
		return ["exit-not-exists", "exit-not-found"]
	}
}


export class Talk extends Action {

	constructor() {
		super();
	}

	init() {
		this.place = this.game.player.container
		this.sendEventLater(this.place)

		return true;
	}
		
	check() {
		return true;
	}

	carryOut() {
		this.fireResponse("player-says")

		this.sendEventLater(this.place)
	}

	report() {
		
	}

	responses() {
		return ["player-says"]
	}
}

export class TalkTo extends Action {

	constructor() {
		super();
	}

	init() {
		// Direct object in inventory or current place
		let lst = this.game.player.childs(this.parser.directObjectString)
		lst.extend(this.game.player.container.childs(this.parser.directObjectString))

		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.directObject) return false

		this.sendEventLater(this.parser.directObject)

		return true;
	}
	
	check() {
		if (this.parser.directObject == this.game.player)
			return this.fireResponse("direct-is-the-player")
		if (!this.parser.directObject.isSet("speaker"))
			return this.fireResponse("direct-is-not-speaker")
		return true;
	}

	carryOut() {
		this.sendEventLater(this.parser.directObject)
	}

	report() {
		this.fireResponse("nothing-happens")
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "direct-is-not-speaker",
					"nothing-happens"]
	}
}


export class GiveTo extends Action {

	constructor() {
		super();
	}

	init() {

		// Direct Object in inventory
		let lst = this.game.player.childs(this.parser.directObjectString)
		if (lst.length === 0) return this.fireResponse("direct-not-found")
		this.parser.directObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.directObject) return false

		// Indirect Object in the place
		lst = this.game.player.container.childs(this.parser.indirectObjectString)
		if (lst.length === 0) return this.fireResponse("indirect-not-found")
		this.parser.indirectObject = this.dictionary.objectChooserDialog.execute(lst)
		if (!this.parser.indirectObject) return false

		this.sendEventLater(this.parser.directObject)
		this.sendEventLater(this.parser.indirectObject)

		return true;
	}

	check() {
		if (this.game.player == this.parser.indirectObject)
			return this.fireResponse("indirect-is-the-player")
		if (!this.parser.indirectObject.isSet("interactive"))
			return this.fireResponse("indirect-is-not-interactive")
		return true;
	}

	carryOut() {
		// Move direct inner indirect
		this.parser.directObject.container = this.parser.indirectObject

		this.sendEventLater(this.parser.directObject)
		this.sendEventLater(this.parser.indirectObject)
	}

	report() {
		this.fireResponse("given-to-indirect")
	}

	responses() {
		return ["direct-not-found", "indirect-not-found", "indirect-is-the-player",
				"indirect-is-not-interactive", "given-to-indirect"]
	}
}

export class ReadObject extends DefaultAction {
	constructor() {
		super();
	}
}

export class SmokeObject extends DefaultAction {
	constructor() {
		super();
	}
}

export class TurnOnObject extends DefaultAction {
	constructor() {
		super();
	}
}

export class TurnOffObject extends DefaultAction {
	constructor() {
		super();
	}
}

export class HitObject extends DefaultAction {
	constructor() {
		super();
	}
}

export class TouchObject extends DefaultAction {
	constructor() {
		super();
	}
}

export class PressObject extends DefaultAction {
	constructor() {
		super();
	}
}
