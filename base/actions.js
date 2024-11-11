import { Action, DefaultAction } from "./action.js"
import { Output } from "./output.js";

export const actions = {};

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
} actions.UnknownVerb = UnknownVerb;

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
} actions.Clear = Clear;

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
		if (this.book.saveGame()) {
			this.fireResponse("game-saved")
		} else {  this.fireResponse("cancel-error") }
	}

	report() {
		
	}

	responses() {
		return ["game-saved", "cancel-error"]
	}
} actions.SaveGame = SaveGame;

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
		if (this.book.loadGame()) {
			this.fireResponse("game-loaded")
		} else {  this.fireResponse("cancel-error") }
	}

	report() {
		
	}

	responses() {
		return ["game-loaded", "cancel-error"]
	}
} actions.LoadGame = LoadGame;

export class Inventory extends Action {

	constructor() {
		super();
	}

	init() {
		this.sendEventLater(this.book.player)
		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		let lst = this.book.player.children()
		if (lst.length === 0) { this.fireResponse("inventory-is-empty")
		} else { 
			this.book.dictionary.inventoryDialog.execute(lst)
		}

		this.sendEventLater(this.book.player)
	}

	report() {
		
	}

	responses() {
		return ["inventory-is-empty"]
	}
} actions.Inventory = Inventory;


export class ExamineObject extends Action {

	constructor() {
		super();
	}

	init() {

		let lst = this.book.player.children(this.book.parser.directObjectString)
		lst.push(...this.book.player.container.children(this.book.parser.directObjectString))

		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.book.parser.directObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.directObject) return false

		this.sendEventLater(this.book.parser.directObject)

		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		this.sendEventLater(this.book.parser.directObject) }

	report() {
		
	}

	responses() {
		return ["direct-not-found"]
	}
} actions.ExamineObject = ExamineObject;

export class LookAround extends Action {

	constructor() {
		super();
	}

	init() {
		this.place = this.book.player.container
		this.sendEventLater(this.place)

		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		// Print the description of the place
		Output.print(this.place.getName(), this.book.getProperty("place-title-style"));
		this.sendEventLater(this.place);
	}

	report() {
		let nouns = []
		let proppers = []
		this.place.children().forEach(n => {
			if (n === this.book.player) return;
			if (n.isSet("scene")) return;
			if (n.isSet("propper")) proppers.push(n);
			else nouns.push(n);
		});

		if (nouns.length !== 0) {
			Output.print("")
			this.book.dictionary.seeListDialog.execute(nouns);
		}

		if (proppers.length !== 0) {
			Output.print("")
			this.book.dictionary.propperListDialog.execute(proppers)
		}
	}
	
	responses() {
		return []
	}
} actions.LookAround = LookAround;

export class LookInside extends Action {

	constructor() {
		super();
	}

	init() {

		let lst = this.book.player.children(this.book.parser.directObjectString)
		lst.push(...this.book.player.container.children(this.book.parser.directObjectString))

		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.book.parser.directObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.directObject) return false

		this.sendEventLater(this.book.parser.directObject)

		return true;
	}

	check() {
		if (this.book.parser.directObject == this.book.player)
			return this.fireResponse("direct-is-the-player")
		if (!this.book.parser.directObject.isSet("container"))
			return this.fireResponse("direct-is-not-container")
		if (this.book.parser.directObject.isSet("closed"))
			return this.fireResponse("direct-is-closed")

		return true;
	}

	carryOut() {
		const childs = this.book.parser.directObject.children();
		if (childs.length === 0) {
			this.fireResponse("container-is-empty")
		} else { 
			this.book.dictionary.lookInsideDialog.execute(childs)
		}

		this.sendEventLater(this.book.parser.directObject)
	}

	report() {
		
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "direct-is-not-container",
					"direct-is-closed", "container-is-empty"]
	}
} actions.LookInside = LookInside;

export class TakeObject extends Action {

	constructor() {
		super();
	}

	init() {
		// Get the object from the current place
		let lst = this.book.player.container.children(this.book.parser.directObjectString)
		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.book.parser.directObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.directObject) return false

		this.sendEventLater(this.book.parser.directObject)

		return true;
	}

	check() {
		if (this.book.parser.directObject == this.book.player)
			return this.fireResponse("direct-is-the-player")
		if (this.book.parser.directObject.isSet("fixed"))
			return this.fireResponse("direct-is-fixed")
		if (this.book.parser.directObject.isSet("heavy"))
			return this.fireResponse("direct-is-heavy")

		return true;
	}

	carryOut() {
		// Move the DO to player's inventory
		this.book.parser.directObject.container = this.book.player
		this.book.parser.directObject.set(["taken"])
		this.sendEventLater(this.book.parser.directObject)
	}

	report() {
		this.fireResponse("direct-taken")
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "direct-is-fixed",
					"direct-is-heavy", "direct-taken"]
	}
} actions.TakeObject = TakeObject;

export class LeaveObject extends Action {

	constructor() {
		super();
	}

	init() {
		let lst = this.book.player.children(this.book.parser.directObjectString)
		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.book.parser.directObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.directObject) return false

		this.sendEventLater(this.book.parser.directObject)

		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		const noun = this.book.parser.directObject;
		noun.container = this.book.player.container;
		noun.set(["leaved"]);

		this.sendEventLater(noun);
	}

	report() {
		this.fireResponse("direct-left")
	}

	responses() {
		return ["direct-not-found", "direct-left"]
	}
} actions.LeaveObject = LeaveObject;

export class TakeFrom extends Action {

	constructor() {
		super();
	}

	init() {

		let lst = this.book.player.children(this.book.parser.indirectObjectString)
		lst.push(...this.book.player.container.children(this.book.parser.indirectObjectString))

		if (lst.length === 0) return this.fireResponse("indirect-not-found")

		this.book.parser.indirectObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.indirectObject) return false

		this.sendEventLater(this.book.parser.indirectObject)

		return true;
	}

	check() {

		const container = this.book.parser.indirectObject;

		if (!container.isSet("container"))
			return this.fireResponse("indirect-is-not-container")
		if (container.isSet("closed"))
			return this.fireResponse("indirect-is-closed")

		const lst = container.children(this.book.parser.directObjectString)
		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.book.parser.directObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.directObject) return false

		// Send the before event now
		return this.book.parser.directObject.doBefore()
	}

	carryOut() {
		// Move the noun to the player's inventory
		this.book.parser.directObject.container = this.book.player
		this.book.parser.directObject.set(["taken"])
		this.sendEventLater(this.book.parser.indirectObject)
		this.sendEventLater(this.book.parser.directObject)
	}

	report() {
		this.fireResponse("direct-taken")
	}

	responses() {
		return ["indirect-not-found", "indirect-is-not-container", "indirect-is-closed",
					"direct-not-found", "direct-taken"]
	}
} actions.TakeFrom = TakeFrom;

export class LeaveIn extends Action {

	constructor() {
		super();
	}

	init() {
		// The direct object in inventory (object)
		let lst = this.book.player.children(this.book.parser.directObjectString)
		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.book.parser.directObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.directObject) return false

		// The indirect object in the inventory or the current place (container)
		lst = this.book.player.children(this.book.parser.indirectObjectString)
		lst.push(...this.book.player.container.children(this.book.parser.indirectObjectString))
		if (lst.length === 0) return this.fireResponse("indirect-not-found")

		this.book.parser.indirectObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.indirectObject) return false

		this.sendEventLater(this.book.parser.directObject)
		this.sendEventLater(this.book.parser.indirectObject)

		return true;
	}

	check() {

		if (this.book.parser.indirectObject == this.book.player)
			return this.fireResponse("indirect-is-the-player")
		if (!this.book.parser.indirectObject.isSet("container"))
			return this.fireResponse("indirect-is-not-container")
		if (this.book.parser.indirectObject.isSet("closed"))
			return this.fireResponse("indirect-is-closed")

		return true;
	}

	carryOut() {
		// Move the object to the container
		this.book.parser.directObject.container = this.book.parser.indirectObject
		this.book.parser.directObject.set(["leaved"])
		this.sendEventLater(this.book.parser.directObject)
		this.sendEventLater(this.book.parser.indirectObject)
	}

	report() {
		this.fireResponse("direct-leaved")
	}

	responses() {
		return ["direct-not-found", "indirect-not-found", "indirect-is-the-player",
					"indirect-is-not-container", "indirect-is-closed", "direct-leaved"]
	}
} actions.LeaveIn = LeaveIn;

export class PullObject extends Action {

	constructor() {
		super();
	}

	init() {

		let lst = this.book.player.container.children(this.book.parser.directObjectString)
		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.book.parser.directObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.directObject) return false

		this.sendEventLater(this.book.parser.directObject)

		return true;
	}

	check() {
		if (this.book.parser.directObject == this.book.player)
			return this.fireResponse("direct-is-the-player")
		if (this.book.parser.directObject.isSet("fixed"))
			return this.fireResponse("direct-is-fixed")
		return true;
	}

	carryOut() {
		this.sendEventLater(this.book.parser.directObject)
	}

	report() {
		this.fireResponse("nothing-happens")
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "direct-is-fixed", "nothing-happens"]
	}
} actions.PullObject = PullObject;

export class PushObject extends Action {

	constructor() {
		super();
	}

	init() {

		let lst = this.book.player.container.children(this.book.parser.directObjectString)
		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.book.parser.directObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.directObject) return false

		this.sendEventLater(this.book.parser.directObject)

		return true;
	}

	check() {
		if (this.book.parser.directObject == this.book.player)
			return this.fireResponse("direct-is-the-player")
		if (this.book.parser.directObject.isSet("fixed"))
			return this.fireResponse("direct-is-fixed")
		return true;
	}

	carryOut() {
		this.sendEventLater(this.book.parser.directObject)
	}

	report() {
		this.fireResponse("nothing-happens")
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "direct-is-fixed",
						"nothing-happens"]
	}
} actions.PushObject = PushObject;


export class OpenObject extends Action {

	constructor() {
		super();
	}

	init() {
		let lst = this.book.player.children(this.book.parser.directObjectString)
		lst.push(...this.book.player.container.children(this.book.parser.directObjectString))

		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.book.parser.directObject = this.book.dictionary.objectChooserDialog.execute(lst)

		if (!this.book.parser.directObject) return false

		this.sendEventLater(this.book.parser.directObject)

		return true;
	}

	check() {

		if (this.book.parser.directObject == this.book.player)
			return this.fireResponse("direct-is-the-player")
		if (!this.book.parser.directObject.isSet("closable"))
			return this.fireResponse("direct-is-not-closable")
		if (!this.book.parser.directObject.isSet("closed"))
			return this.fireResponse("direct-is-open")

		return true;
	}

	carryOut() {
		this.book.parser.directObject.unset(["closed"])
		this.sendEventLater(this.book.parser.directObject)
	}

	report() {
		this.fireResponse("direct-was-opened")
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "direct-is-not-closable",
					"direct-is-open", "direct-was-opened"]
	}
} actions.OpenObject = OpenObject;

export class CloseObject extends Action {

	constructor() {
		super();
	}

	init() {
		let lst = this.book.player.children(this.book.parser.directObjectString)
		lst.push(...this.book.player.container.children(this.book.parser.directObjectString))

		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.book.parser.directObject = this.book.dictionary.objectChooserDialog.execute(lst)

		if (!this.book.parser.directObject) return false

		this.sendEventLater(this.book.parser.directObject)

		return true;
	}

	check() {

		if (this.book.parser.directObject == this.book.player)
			return this.fireResponse("direct-is-the-player")
		if (!this.book.parser.directObject.isSet("closable"))
			return this.fireResponse("direct-is-not-closable")
		if (this.book.parser.directObject.isSet("closed"))
			return this.fireResponse("direct-is-closed")

		return true;
	}

	carryOut() {
		this.book.parser.directObject.set(["closed"])
		this.sendEventLater(this.book.parser.directObject)
	}

	report() {
		this.fireResponse("direct-was-closed")
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "direct-is-not-closable",
						"direct-is-closed", "direct-was-closed"]
	}
} actions.CloseObject = CloseObject;

export class OpenWith extends Action {

	constructor() {
		super();
	}

	init() {

		// Direct object in inventory or current place
		let lst = this.book.player.children(this.book.parser.directObjectString)
		lst.push(...this.book.player.container.children(this.book.parser.directObjectString))

		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.book.parser.directObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.directObject) return false

		// Indirect object in inventory
		lst = this.book.player.children(this.book.parser.indirectObjectString)

		if (lst.length === 0) return this.fireResponse("indirect-not-found")

		this.book.parser.indirectObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.indirectObject) return false

		this.sendEventLater(this.book.parser.directObject)
		this.sendEventLater(this.book.parser.indirectObject)

		return true;
	}

	check() {

		if (this.book.parser.directObject == this.book.player)
			return this.fireResponse("direct-is-the-player")
		if (this.book.parser.indirectObject == this.book.player)
			return this.fireResponse("indirect-is-the-player")

		if (!this.book.parser.directObject.isSet("closable"))
			return this.fireResponse("direct-is-not-closable")

		if (!this.book.parser.directObject.isSet("closed"))
			return this.fireResponse("direct-is-open")

		return true;
	}

	carryOut() {
		this.sendEventLater(this.book.parser.directObject)
		this.sendEventLater(this.book.parser.indirectObject)
	}

	report() {
		this.fireResponse("nothing-happens")
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "indirect-is-the-player",
					"direct-is-not-closable", "direct-is-open", "nothing-happens"]
	}
} actions.OpenWith = OpenWith;

export class CloseWith extends Action {

	constructor() {
		super();
	}

	init() {

		// Direct object in inventory or current place
		let lst = this.book.player.children(this.book.parser.directObjectString)
		lst.push(...this.book.player.container.children(this.book.parser.directObjectString))

		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.book.parser.directObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.directObject) return false

		// Indirect object in inventory
		lst = this.book.player.children(this.book.parser.indirectObjectString)

		if (lst.length === 0) return this.fireResponse("indirect-not-found")

		this.book.parser.indirectObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.indirectObject) return false

		this.sendEventLater(this.book.parser.directObject)
		this.sendEventLater(this.book.parser.indirectObject)

		return true;
	}

	check() {

		if (this.book.parser.directObject == this.book.player)
			return this.fireResponse("direct-is-the-player")
		if (this.book.parser.indirectObject == this.book.player)
			return this.fireResponse("indirect-is-the-player")

		if (!this.book.parser.directObject.isSet("closable"))
			return this.fireResponse("direct-is-not-closable")

		if (this.book.parser.directObject.isSet("closed"))
			return this.fireResponse("direct-is-closed")

		return true;
	}

	carryOut() {
		this.sendEventLater(this.book.parser.directObject)
		this.sendEventLater(this.book.parser.indirectObject)
	}

	report() {
		this.fireResponse("nothing-happens")
	}

	responses() {
		return ["direct-not-found", "indirect-not-found", "direct-is-the-player",
					"indirect-is-the-player", "direct-is-not-closable",
							"direct-is-closed", "nothing-happens"]
	}
} actions.CloseWith = CloseWith;

export class GoTo extends Action {

	constructor() {
		super();
	}

	init() {

		// Get exit from dictionary
		const exit = this.book.dictionary.getExit(this.book.parser.directObjectString);
		if (!exit) return this.fireResponse("exit-not-exists");

		// Get connection from dictionary
		this.conn = this.book.player.container.getConnection(exit);
		if (!this.conn) return this.fireResponse("exit-not-found");

		this.sendEventLater(this.book.player.container)

		return true;
	}

	check() {
		return true;
	}

	carryOut() {
		// Get the destiny
		let nouns = this.book.dictionary.getNouns(this.conn.destiny)
		if(nouns.length === 0) {
			Output.error(`Called GoTo action from "${this.book.player.container.getName()}": Destiny "${this.conn.destiny}" not found on exit "${this.conn.exit}"`);
		}
		// Move the player
		this.book.player.container = nouns[0];

		// Visibility behavior
		if (this.book.getProperty("look-around") === "always") {
			// Look around verb
			let v = this.book.dictionary.verbByAction("LookAround");
			this.book.execute(v.getName());
		}
		
		this.sendEventLater(this.book.player.container);
	}

	report() {
		
	}
	
	responses() {
		return ["exit-not-exists", "exit-not-found"]
	}
} actions.GoTo = GoTo;

export class Talk extends Action {

	constructor() {
		super();
	}

	init() {
		this.place = this.book.player.container
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
} actions.Talk = Talk;

export class TalkTo extends Action {

	constructor() {
		super();
	}

	init() {
		// Direct object in inventory or current place
		let lst = this.book.player.children(this.book.parser.directObjectString)
		lst.push(...this.book.player.container.children(this.book.parser.directObjectString))

		if (lst.length === 0) return this.fireResponse("direct-not-found")

		this.book.parser.directObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.directObject) return false

		this.sendEventLater(this.book.parser.directObject)

		return true;
	}
	
	check() {
		if (this.book.parser.directObject == this.book.player)
			return this.fireResponse("direct-is-the-player")
		if (!this.book.parser.directObject.isSet("speaker"))
			return this.fireResponse("direct-is-not-speaker")
		return true;
	}

	carryOut() {
		this.sendEventLater(this.book.parser.directObject)
	}

	report() {
		this.fireResponse("nothing-happens")
	}

	responses() {
		return ["direct-not-found", "direct-is-the-player", "direct-is-not-speaker",
					"nothing-happens"]
	}
} actions.TalkTo = TalkTo;

export class GiveTo extends Action {

	constructor() {
		super();
	}

	init() {

		// Direct Object in inventory
		let lst = this.book.player.children(this.book.parser.directObjectString)
		if (lst.length === 0) return this.fireResponse("direct-not-found")
		this.book.parser.directObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.directObject) return false

		// Indirect Object in the place
		lst = this.book.player.container.children(this.book.parser.indirectObjectString)
		if (lst.length === 0) return this.fireResponse("indirect-not-found")
		this.book.parser.indirectObject = this.book.dictionary.objectChooserDialog.execute(lst)
		if (!this.book.parser.indirectObject) return false

		this.sendEventLater(this.book.parser.directObject)
		this.sendEventLater(this.book.parser.indirectObject)

		return true;
	}

	check() {
		if (this.book.player == this.book.parser.indirectObject)
			return this.fireResponse("indirect-is-the-player")
		if (!this.book.parser.indirectObject.isSet("interactive"))
			return this.fireResponse("indirect-is-not-interactive")
		return true;
	}

	carryOut() {
		// Move direct inner indirect
		this.book.parser.directObject.container = this.book.parser.indirectObject

		this.sendEventLater(this.book.parser.directObject)
		this.sendEventLater(this.book.parser.indirectObject)
	}

	report() {
		this.fireResponse("given-to-indirect")
	}

	responses() {
		return ["direct-not-found", "indirect-not-found", "indirect-is-the-player",
				"indirect-is-not-interactive", "given-to-indirect"]
	}
} actions.GiveTo = GiveTo;

export class ReadObject extends DefaultAction {
	constructor() {
		super();
	}
} actions.ReadObject = ReadObject;

export class SmokeObject extends DefaultAction {
	constructor() {
		super();
	}
} actions.SmokeObject = SmokeObject;

export class TurnOnObject extends DefaultAction {
	constructor() {
		super();
	}
} actions.TurnOnObject = TurnOnObject;

export class TurnOffObject extends DefaultAction {
	constructor() {
		super();
	}
} actions.TurnOffObject = TurnOffObject;

export class HitObject extends DefaultAction {
	constructor() {
		super();
	}
} actions.HitObject = HitObject;

export class TouchObject extends DefaultAction {
	constructor() {
		super();
	}
} actions.TouchObject = TouchObject;

export class PressObject extends DefaultAction {
	constructor() {
		super();
	}
} actions.PressObject = PressObject;
