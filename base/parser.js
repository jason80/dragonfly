import { Output } from "./output.js";

/**
 *
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
				this.game.execute("?");
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
			if (this.checkKeyword(tokens[1], syntax[0])) {
				this.keyword = tokens[1];
				this.directObjectString = tokens.slice(2).join(" ");
				return action;
			} else {
				return null;
			}
		}

		// Case 4: Object, keyword, object
		if (syntax.length === 3) {
			if (syntax[1] !== "1" && syntax[1] !== "2") {
				let ti = 1;
				while (ti < tokens.length && !this.checkKeyword(tokens[ti], syntax[1])) {
					if (syntax[0] === "1") {
						this.directObjectString += tokens[ti] + " ";
					} else {
						this.indirectObjectString += tokens[ti] + " ";
					}
					ti++;
				}

				if (ti >= tokens.length) return null;
				this.keyword = tokens[ti];

				ti++;
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

	checkKeyword(keyword, kwList) {
		return kwList.toLowerCase().split("/").includes(keyword.toLowerCase());
	}

	cleanArticles(obj) {
		return obj.toLowerCase().split(" ").filter(w => !this.book.dictionary.getArticle(w)).join(" ").trim();
	}

	debug(msg) {
		if (this.showParsingProcess) {
			Output.print(`Parser: ${msg}`, {
				fontFamily: "'Courier New', Courier, monospace"
			});
		}
	}

	checkMultiparameterVerb(action, tokens) {
		const verb = action.verb;
		const syntax = verb.syntax;

		const joined = tokens.join(" ");
		const pair = joined.split(":");

		if (pair.length !== 2) {
			this.debug("Separator ':' not found.");
			return false;
		}

		if (syntax.length === 1) {
			if (!verb.responds(pair[0])) {
				this.debug(`verb: '${verb.getName()}' is not '${pair[0]}.'`);
				return false;
			}
			this.parameters = pair[1].trim();
			this.debug(`Parameters: '${this.parameters}'.`);
			return action;
		}

		if (syntax.length === 3) {
			const leftTokens = pair[0].split(" ");

			if (syntax[1] !== "1") throw new Error(`Syntax error on verb: ${verb.name}.`);

			if (leftTokens.length < 3) return null;

			if (!this.checkKeyword(leftTokens[1], syntax[0])) return null;

			this.keyword = leftTokens[1];
			this.directObjectString = leftTokens.slice(2).join(" ");
			this.parameters = pair[1].trim();

			this.debug(`Keyword: '${this.keyword}'.`);
			this.debug(`Parameters: '${this.parameters}'.`);

			return action;
		}

		return null;
	}
}
