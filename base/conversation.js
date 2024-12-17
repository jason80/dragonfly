import { DFMLNode } from "../dfml/js/main/node.js";
import { Action } from "./action.js";

/**
 * Represents a conversation between player and speaker noun.
 * Conversations are stored in dictionary in special list.
 *
 * @export
 * @class Conversation
 */
export class Conversation {
	/**
	 * Creates an instance of Conversation.
	 * @memberof Conversation
	 */
	constructor() {
		this.owner = "";
	}

	/**
	 * Run the conversation.
	 *
	 * @param {Action} action the action
	 * @memberof Conversation
	 */
	start(action) {

	}

	/**
	 * Loads a conversation from dfml node.
	 *
	 * @param {DFMLNode} node the dfml node.
	 * @memberof Conversation
	 */
	load(node) {
		this.owner = node.getAttr("owner").getValue();

		// TODO: rest
	}
};
