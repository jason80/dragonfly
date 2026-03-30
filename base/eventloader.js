import { DFMLNode } from "../dfml/js/main/node.js";
import { DFMLElement } from "../dfml/js/main/element.js";
import { DFMLValue } from "../dfml/js/main/value.js";
import { ActionResponse } from "./actionresponse.js";
import { responses } from "./responses.js";
import { Output } from "./output.js";
import { Utils } from "./utils.js";


/**
 * Load responses from dfml node. can be event or conversation topic.
 *
 * @param {DFMLNode} node The dfml node.
 * @param {Array<ActionResponse>} responseList Response list to add.
 */
export function loadResponses(node, responseList) {
	// Load responses
	node.children.forEach(child => {

		// Simple text found: create a message response:
		if (child.getElementType() === DFMLElement.DATA && child.getValue().getType() == DFMLValue.STRING) {
			const text = child.getValue().getValue();
			const message = new responses["Print"]();
			message.message = text;
			responseList.push(message);
		}

		// Response found:
		if (child.getElementType() === DFMLElement.NODE) {
			if (child.getName() === "response") {
				loadResponse(child, responseList);
			} else { // Response class name

				// Convert to class name style
				let className = child.getName()
						.split('-')
						.map(word => word.charAt(0).toUpperCase() + word.slice(1))
						.join('');

				child.setAttrString("class", className);
				loadResponse(child, responseList);
			}
		}
	});
}

/**
 * Load single response.
 *
 * @param {DFMLNode} node the response node.
 * @param {Array<ActionResponse>} responseList Response list to add.
 */
function loadResponse(node, responseList) {

	if (!Utils.expectedAttributes(node, "class")) return ;

	const responseClassName = node.getAttr("class").getValue();
	const responseClass = responses[responseClassName];
	if (!responseClass) {
		Output.error(`response class "${responseClassName}" not exists.`);
	} else {
		const response = new responseClass();
		response.load(node);
		responseList.push(response);
	}
}
