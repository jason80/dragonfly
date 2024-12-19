import { DFMLElement } from "../dfml/js/main/element.js";
import { DFMLNode } from "../dfml/js/main/node.js";
import { Action } from "./action.js";
import { loadConditionsAndResponses } from "./eventloader.js";
import { Utils } from "./utils.js";

/**
 * Represents a subject or topic in a conversation.
 * When the player types a phrase, the conversation topic is
 * searched and executed as if it were an event with
 * responses and conditions.
 *
 * @export
 * @class Topic
 */
export class Topic {
	/**
	 * Creates an instance of Topic.
	 * @memberof Topic
	 */
	constructor() {
		this.match = [];
		this.conditions = [];
		this.responses = [];
	}

	/**
	 * Compares the input parameters with the topic match.
	 *
	 * @param {string} params the input parameters on single line.
	 * @return {boolean} true if the current topic match.
	 * @memberof Topic
	 */
	check(params) {
		// TODO: Improve topic check
		params = params.toLowerCase().split(" ");

		for (const t of this.match) {
			for (const p of params) {
				if (Utils.isEquals(t, p)) return true;
			}
		}

		return false;
	}


	/**
	 * Loads the topic from dfml node.
	 *
	 * @param {DFMLNode} node the dfml node
	 * @memberof Topic
	 */
	load(node) {
		if (node.hasAttr("match"))
			this.match = node.getAttr("match").getValue().split(",");
		loadConditionsAndResponses(node, this.conditions, this.responses);
	}
};

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
		this.topics = [];
		this.defaultTopic = null;
	}

	/**
	 * Run the conversation.
	 *
	 * @param {Action} action the action.
	 * @memberof Conversation
	 */
	start(action) {
		for (const t of this.topics) {
			if (t.check(action.book.parser.parameters)) {
				if (this.runTopic(action, t)) return;
			}
		}

		if (this.defaultTopic) this.runTopic(action, this.defaultTopic);
	}

	/**
	 * Run topic as event. Check conditions and runs responses.
	 *
	 * @param {Action} action the action.
	 * @param {Topic} topic the topic.
	 * @return {boolean} true if it meets the conditions.
	 * @memberof Conversation
	 */
	runTopic(action, topic) {
		for (const c of topic.conditions) {
			if (!c.check(action)) return false;
		}

		for (const r of topic.responses) {
			r.execute(action);
		}

		return true;
	}

	/**
	 * Loads a conversation from dfml node.
	 *
	 * @param {DFMLNode} node the dfml node.
	 * @memberof Conversation
	 */
	load(node) {
		this.owner = node.getAttr("owner").getValue();

		for (const child of node.children) {
			if (child.getElementType() === DFMLElement.NODE) {
				if (child.getName() === "topic") {
					const topic = new Topic();
					topic.load(child);
					this.topics.push(topic);
				} else if (child.getName() === "default") {
					this.defaultTopic = new Topic();
					this.defaultTopic.load(child);
				}
			}
		}
	}
};
