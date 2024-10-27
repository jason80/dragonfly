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
    parse(line) {
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
        const verbs = this.dictionary.verbs(strVerb);

        // Verb not found
        if (!verbs.length) {
            this.debug("verbs not found.");
            
            // Check if the token is an exit
            const exit = this.dictionary.exit(line.trim());
            if (exit) {
                this.debug(`exit: "${exit.name}" found.`);
                const gotoVerb = this.dictionary.verbByAction("GoTo");
                this._dObjStr = line.trim();
                this._iObjStr = "";

                const action = new gotoVerb.action();
                action.verb = gotoVerb;
                action.game = this.game;

                this.debug(`calling GoTo action on exit: "${this._dObjStr}".`);
                action.execute();
            } else {
                this.debug("exit not found.");
                this.parse("?");
            }
            return;
        }

        this.debug(`for ${tokens[0]}, ${verbs.length} verb(s) found, checking syntax ...`);

        let action = null;

        for (const v of verbs) {
            this._dObjStr = "";
            this._iObjStr = "";
            this._keyword = "";
            this._parameters = "";

            action = this.checkSyntax(v, tokens);
            if (action) break; // Syntax match found
        }

        if (!action) {
            this.debug(`syntax check fails: "${tokens[0]}".`);

            const response = verbs[0].getResponse("syntax-fail").trim();
            if (response) {
                Console.println(response);
            } else {
                this.game.execute("?");
            }
            return;
        }

        this._dObjStr = this.cleanArticles(this._dObjStr);
        this._iObjStr = this.cleanArticles(this._iObjStr);

        this.debug(`executing action: "${action.constructor.name}".`);

        if (this._showParsingProcess) {
            if (this._dObjStr) {
                let msg = `Params 1=${this._dObjStr}`;
                if (this._iObjStr) {
                    msg += `, 2=${this._iObjStr}.`;
                }
                this.debug(msg);
            }
        }

        action.execute();
    }

    checkSyntax(verb, tokens) {
        const action = new verb.action();
        action.game = this._game;
        action.verb = verb;

        const syntax = verb.syntax;

        // Case 0: Multiparameter verb
        if (syntax && syntax[syntax.length - 1] === "...") {
            this.debug("Multiparameter verb:");
            return this.checkMultiparameterVerb(action, tokens);
        }

        // Case 1: Verb without parameters
        if (!syntax) {
            if (tokens.length > 1) return null;
            return action;
        }

        // Case 2: Wait for direct object
        if (syntax.length === 1 && syntax[0] === "1") {
            if (tokens.length === 1) return null;
            this._dObjStr = tokens.slice(1).join(" ");
            return action;
        }

        // Case 3: Keyword and direct object
        if (syntax.length === 2 && syntax[1] === "1") {
            if (tokens.length <= 1) return null;
            if (this.checkKeyword(tokens[1], syntax[0])) {
                this._keyword = tokens[1];
                this._dObjStr = tokens.slice(2).join(" ");
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
                        this._dObjStr += tokens[ti] + " ";
                    } else {
                        this._iObjStr += tokens[ti] + " ";
                    }
                    ti++;
                }

                if (ti >= tokens.length) return null;
                this._keyword = tokens[ti];

                ti++;
                while (ti < tokens.length) {
                    if (syntax[2] === "1") {
                        this._dObjStr += tokens[ti] + " ";
                    } else {
                        this._iObjStr += tokens[ti] + " ";
                    }
                    ti++;
                }

                if (!this._dObjStr && syntax[2] === "1") return null;
                if (!this._iObjStr && syntax[2] !== "1") return null;

                return action;
            }
        }

        throw new Error(`Syntax error on verb: ${verb.name}.`);
    }

    checkKeyword(keyword, kwList) {
        return kwList.split("/").includes(keyword);
    }

    cleanArticles(obj) {
        return obj.split(" ").filter(w => !this.game.dictionary.article(w)).join(" ");
    }

    debug(msg) {
        if (this._showParsingProcess) {
            Console.println(`Parser: ${msg}`, "family: 'Courier'");
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
                this.debug(`verb: '${verb.name}' is not '${pair[0]}.'`);
                return false;
            }
            this._parameters = pair[1].trim();
            this.debug(`Parameters: '${this._parameters}'.`);
            return action;
        }

        if (syntax.length === 3) {
            const leftTokens = pair[0].split(" ");

            if (syntax[1] !== "1") throw new Error(`Syntax error on verb: ${verb.name}.`);

            if (leftTokens.length < 3) return null;

            if (!this.checkKeyword(leftTokens[1], syntax[0])) return null;

            this._keyword = leftTokens[1];
            this._dObjStr = leftTokens.slice(2).join(" ");
            this._parameters = pair[1].trim();

            this.debug(`Keyword: '${this._keyword}'.`);
            this.debug(`Parameters: '${this._parameters}'.`);

            return action;
        }

        return null;
    }
}