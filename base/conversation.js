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
	 * Loads the topic from dfml node.
	 *
	 * @param {DFMLNode} node the dfml node
	 * @memberof Topic
	 */
	load(node) {

		if (!Utils.expectedAttributes(node, "match")) return ;

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
	 * Compares the input parameters with the topic match of all topics.
	 * Run the conversation.
	 *
	 * @param {Action} action the action.
	 * @memberof Conversation
	 */
	start(action) {

		let bestTopic = this.defaultTopic;
		let highScore = 0;

		for (const t of this.topics) {
			let score = 0;
			for (const p of action.book.parser.parameters.split(' ')) {
				for (const m of t.match) {
					if (Utils.isEquals(p, m)) {
						score ++;
					}
				}
			}

			if (score > highScore) {
				highScore = score;
				bestTopic = t;
			}
		}

		this.runTopic(action, bestTopic);
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

		if (!Utils.expectedAttributes(node, "owner")) return ;

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
