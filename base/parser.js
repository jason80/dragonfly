import { Action } from "./action.js";
import { Output } from "./output.js";
import { Verb } from "./verb.js";
import { Book } from "./book.js";
import { Utils } from "./utils.js";

/**
 * Main parser module
 *
 * @export
 * @class Parser
 */
export class Parser {
	/**
	 * Creates an instance of Parser.
	 * @param {Book} book main book instance.
	 * @memberof Parser
	 */
	constructor(book) {
		this.book = book;
		this.showParsingProcess = false;

		this.directObjectString = "";
		this.indirectObjectString = "";
		this.parameters = "";
		this.directObject = null;
		this.indirectObject = null;
		this.keyword = "";
	}

	/**
	 * Main parse method.
	 *
	 * @param {string} line string line to parse.
	 * @memberof Parser
	 */
	async parse(line) {

		// Dragonfly version
		if (line.trim().toLowerCase() === "--version") {
			Utils.showBookInfo(this.book);
			return;
		}

		// Clean unexpected chars
		const regex = new RegExp(`[${this.book.getProperty("parser-clean")}]`, 'g');
		line = line.replace(regex, '');

		const tokens = line.trim().split(" ").filter(t => t.trim());

		// Empty line
		if (!tokens.length) {
			this.debug("token list is empty.");
			return;
		}

		let strVerb = tokens[0];

		if (strVerb.endsWith(":")) {
			strVerb = strVerb.slice(0, -1); // Remove ":"
		}

		// Filter the verbs
		const verbs = this.book.dictionary.getVerbs(strVerb);

		// Verb not found
		if (!verbs.length) {
			this.debug("verbs not found.");
			
			// Check if the token is an exit
			const exit = this.book.dictionary.getExit(line.trim());
			if (exit) {
				this.debug(`exit: "${exit.getName()}" found.`);
				const gotoVerb = this.book.dictionary.verbByAction("GoTo");
				this.directObjectString = line.trim();
				this.indirectObjectString = "";

				const action = new gotoVerb.action();
				action.verb = gotoVerb;
				action.book = this.book;

				this.debug(`calling GoTo action on exit: "${this.directObjectString}".`);
				await action.execute();
			} else {
				this.debug("exit not found.");
				this.parse("?");
			}
			return;
		}

		this.debug(`for ${tokens[0]}, ${verbs.length} verb(s) found, checking syntax ...`);

		let action = null;

		for (const v of verbs) {
			this.directObjectString = "";
			this.indirectObjectString = "";
			this.keyword = "";
			this.parameters = "";

			action = this.checkSyntax(v, tokens);
			if (action) break; // Syntax match found
		}

		if (!action) {
			this.debug(`syntax check fails: "${tokens[0]}".`);

			const response = verbs[0].getResponse("syntax-fail").trim();
			if (response === "") {
				Output.print(response);
			} else {
				this.book.execute("?");
			}
			return;
		}

		this.directObjectString = this.cleanArticles(this.directObjectString);
		this.indirectObjectString = this.cleanArticles(this.indirectObjectString);

		this.debug(`executing action: "${action.constructor.name}".`);

		if (this.showParsingProcess) {
			if (this.directObjectString) {
				let msg = `Params 1=${this.directObjectString}`;
				if (this.indirectObjectString) {
					msg += `, 2=${this.indirectObjectString}.`;
				}
				this.debug(msg);
			}
		}

		await action.execute();
	}

	/**
	 * Compare syntax verb and try detect direct and indirect objects. Then, returns
	 * the action associated to verb and syntax.
	 *
	 * @param {Verb} verb target verb.
	 * @param {Array<string>} tokens parsed token list.
	 * @return {Action} the action detected.
	 * @memberof Parser
	 */
	checkSyntax(verb, tokens) {
		const action = new verb.action();
		action.book = this.book;
		action.verb = verb;

		const syntax = verb.syntax;

		// Case 0: Multiparameter verb
		if (syntax.length !== 0 && syntax[syntax.length - 1] === "...") {
			this.debug("Multiparameter verb:");
			return this.checkMultiparameterVerb(action, tokens);
		}

		// Case 1: Verb without parameters
		if (syntax.length === 0) {
			if (tokens.length > 1) return null;
			return action;
		}

		// Case 2: Wait for direct object
		if (syntax.length === 1 && syntax[0] === "1") {
			if (tokens.length === 1) return null;
			this.directObjectString = tokens.slice(1).join(" ");
			return action;
		}

		// Case 3: Keyword and direct object
		if (syntax.length === 2 && syntax[1] === "1") {
			if (tokens.length <= 1) return null;
			let result = this.checkKeyword(1, tokens, syntax[0]);
			if (result) {
				this.keyword = result.keyword;
				this.directObjectString = tokens.slice(result.end).join(" ");
				return action;
			} else {
				return null;
			}
		}

		// Case 4: Object, keyword, object
		if (syntax.length === 3) {
			if (syntax[1] !== "1" && syntax[1] !== "2") {
				let ti = 1;
				let result = null;
				while (ti < tokens.length && (result = this.checkKeyword(ti, tokens, syntax[1])) === null) {
					if (syntax[0] === "1") {
						this.directObjectString += tokens[ti] + " ";
					} else {
						this.indirectObjectString += tokens[ti] + " ";
					}
					ti++;
				}

				if (ti >= tokens.length) return null;
				this.keyword = result.keyword;

				ti = result.end;

				while (ti < tokens.length) {
					if (syntax[2] === "1") {
						this.directObjectString += tokens[ti] + " ";
					} else {
						this.indirectObjectString += tokens[ti] + " ";
					}
					ti++;
				}

				if (!this.directObjectString && syntax[2] === "1") return null;
				if (!this.indirectObjectString && syntax[2] !== "1") return null;

				return action;
			}
		}

		throw new Error(`Syntax error on verb: ${verb.name}.`);
	}

	/**
	 * Check if the keyword is in keyword list.
	 *
	 * @param {number} start the start index.
	 * @param {Array<string>} the token list.
	 * @param {string} keywords the keyword list.
	 * @return {dictionary} null if not found. For otherwise, the keyword and the end index.
	 * @memberof Parser
	 */

	checkKeyword(start, tokens, keywords) {

		// Separate keywords
		for (const kw of keywords.toLowerCase().split("/")) {

			let index = start;
			let match = true;

			// Check word by word
			for (const w of kw.split(" ")) {
				if (tokens[index].toLowerCase() !== w) {
					match = false; break;
				}
				index ++;
			}

			if (match) {
				return {
					// Join the keyword
					keyword: tokens.slice(start, index).join(" "),
					end: index // End index
				};
			}
		}

		return null;
	}

	/**
	 * Removes the dictionary registered articles from given object.
	 *
	 * @param {string} obj the string name of the object.
	 * @return {string} the result without the articles.
	 * @memberof Parser
	 */
	cleanArticles(obj) {
		return obj.split(" ").filter(w => {
			const wordLower = w.toLowerCase();
			return !this.book.dictionary.getArticle(wordLower);
		}).join(" ").trim();
	}

	/**
	 * Check the multiparameter special verb and returns the associated action.
	 *
	 * @param {*} action
	 * @param {*} tokens
	 * @return {*} 
	 * @memberof Parser
	 */
	checkMultiparameterVerb(action, completeTokens) {
		const verb = action.verb;
		const syntax = verb.syntax;

		const pair = completeTokens.join(" ").split(":");

		let tokens = "";
		let parameters = "";

		if (pair.length === 1) {
			this.debug("Separator ':' not found. No parameters.");
			tokens = pair[0];

		} else if (pair.length > 2) {
			this.debug("Error: Multiple separators ':' found.");
			return null;
		} else {
			tokens = pair[0].trim();
			parameters = pair[1].trim();
		}

		if (syntax.length === 1) {
			if (!verb.responds(tokens)) {
				this.debug(`verb: '${verb.getName()}' is not '${tokens}.'`);
				return null;
			}
			this.parameters = parameters;
			this.debug(`Parameters: '${parameters}'.`);
			return action;
		}

		if (syntax.length === 3) {
			const leftTokens = tokens.split(" ");

			if (syntax[1] !== "1") throw new Error(`Syntax error on verb: ${verb.name}.`);

			if (leftTokens.length < 3) return null;

			//if (!this.checkKeyword(leftTokens[1], syntax[0])) return null;
			const result = this.checkKeyword(1, leftTokens, syntax[0]);
			if (!result) return null;

			this.keyword = result.keyword;
			this.directObjectString = leftTokens.slice(result.end).join(" ");
			this.parameters = parameters;

			this.debug(`Keyword: '${this.keyword}'.`);
			this.debug(`Parameters: '${parameters}'.`);

			return action;
		}

		return null;
	}

	/**
	 * Print a debug message if 'showParsingProcess' is activated.
	 * 
	 * @param {string} msg debug message.
	 */
	debug(msg) {
		if (this.showParsingProcess) {
			Output.print(`Parser: ${msg}`, {
				fontFamily: "'Courier New', Courier, monospace",
				color: "#888"
			});
		}
	}
}
