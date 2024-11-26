import { Output  } from "./output.js";

export class Help {

	static tipSet = new Set();
	static book = null;

	/**
	 * Show tip text.
	 *
	 * @static
	 * @param {string} message tip message string.
	 * @memberof Help
	 */
	static tip(message) {
		Output.print(`[ Tip: ${message} ]`, this.book.getProperty("tip-style"));
	}

	/**
	 * Show tip text once.
	 * Print the tip if it is no longer in the 'seen' set.
	 *
	 * @static
	 * @param {string} message tip message string.
	 * @memberof Help
	 */
	static tipOnce(message) {
		if (!Help.tipSet.has(message)) {
			Help.tip(message);
			Help.tipSet.add(message);
		}
	}
};
