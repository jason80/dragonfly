import { Output } from "./output.js"

/**
 * Represents an action performed by the player.
 * When the verb is parser, the associated action is executed by execute() method.
 *
 * @export
 * @class Action
 */
export class Action {
	/**
	 * Creates an instance of Action.
	 * @memberof Action
	 */
	constructor() {
		this.book = null;
		this.verb = null;
		this.sendingEvents = [];
	}

	/**
	 * Initialize the action. Behavior depends on the type of action.
	 * Direct and indirect objects are usually looked up in the dictionary and 
	 * if these objects are not found, False is returned for cancel the action.
	 *
	 * @return {boolean} False: causes the action to be cancelled.
	 * @abstract
	 * @memberof Action
	 */
	init() {
		return false;
	}

	/**
	 * The action check consists in verifying if an object
	 *	complies with the norm of the action. Example:
	 *	LookInside checks if the direct object is not "closed".
	 *	"the player will not be able to see inside the chest if it is closed"
	 *
	 * @return {boolean} causes the action to be cancelled.
	 * @abstract
	 * @memberof Action
	 */
	check() {
		return false;
	}

	/**
	 * Perform the action. Example:
	 * If the action is TakeObject, the direct object is moved to player's inventory.
	 * @abstract
	 * @memberof Action
	 */
	carryOut() {

	}

	/**
	 * Report occurs after when action has been performed. Usually show a message.
	 * Example:
	 * "you get a flashlight"
	 *
	 * @abstract
	 * @memberof Action
	 */
	report() {

	}

	/**
	 * The execute() method has the following steps:
	 * 1)	Abstract method init(): initialize the action. If False is
	 * 	returned from init(), action is cancelled.
	 * 1a)	Execute before event on objects handled by the action. If False is returned
	 * 	from doBefore() method, action is cancelled.
	 * 2)	Abstract method check(): check the action. False: action is cancelled.
	 * 3)	Abstract method carryOut(): perform the action.
	 * 3b)	Execute after event on objects handled by the action. If False is returned
	 * 	from doAfter() method, action is cancelled in this point.
	 * 4)	Abstract method report(): report the action after performed.
	 *
	 * @memberof Action
	 */
	execute() {
		this.sendingEvents = []

		// Initialize action
		if (!this.init()) return ;

		// BEFORE EVENT
		this.sendingEvents.array.forEach(n => {
			if (!n.doBefore(this)) return ;
		});

		// Check action
		if (!this.check()) return ;

		this.sendingEvents = [];

		// Action performs the changes
		this.carryOut();

		// AFTER EVENT
		this.sendingEvents.array.forEach(n => {
			if (!n.doAfter(this)) return ;
		});

		// Report the result
		this.report();
	}

	/**
	 * Add the target object to list. This list will be used to send before
	 * and after events.
	 *
	 * @param {Noun} noun Target object
	 * @memberof Action
	 */
	sendEventLater(noun) {
		this.sendingEvents.push(noun);
	}

	/**
	 * Execute a verb's response. The response may exists in the verb and show
	 * the response message. The verb is associated with the current action.
	 *
	 * @param {string} id response id declared in the verb.
	 * @return {boolean} ALWAYS returns false for programming convenience.
	 * @memberof Action
	 */
	fireResponse(id) {
		if (!this.verb.hasResponse(id)) {
			// TODO: ERROR
		}

		Output.print(verd.getResponse(id));

		return false;
	}
	

	/**
	 * Return a list of all responses that may occurs.
	 *
	 * @return {Array.<string>}
	 * @abstract
	 * @memberof Action
	 */
	responses() {
		return [];
	}

	/**
	 * Return action string info.
	 *
	 * @return {string} string of action.
	 * @memberof Action
	 */
	toString() {
		return this.constructor.name;
	}
};

export class UnknownVerb extends Action {
	constructor() {
		super();
	}

	init() { return true; }
	check() { return true; }

	carryOut() { this.fireResponse("unknown-verb"); }
	report() { }
	responses() { return ["unknown-verb"]; }
};
