import { Output } from "./output.js";

export class ListDialog {
    constructor(initialMessage, separator, andSeparator) {
        this.initialMessage = initialMessage;
        this.separator = separator;
        this.andSeparator = andSeparator;
    }

    execute(nouns) {
        let result = `${this.initialMessage} `;

        for (let i = 0; i < nouns.length; i++) {
            if (i !== 0) {
                if (i === nouns.length - 1) {
                    result += this.andSeparator;
                } else {
                    result += this.separator;
                }
            }

            result += nouns[i].article();
        }

        Output.print(`${result}.`);
    }
}

export class PropperListDialog {
    constructor(singular, plural, separator, andSeparator) {
        this.singular = singular;
        this.plural = plural;
        this.separator = separator;
        this.andSeparator = andSeparator;
    }

    execute(nouns) {
        let suffix = this.singular;
        let result = "";

        for (let i = 0; i < nouns.length; i++) {
            if (i !== 0) {
                if (i === nouns.length - 1) {
                    result += this.andSeparator;
                } else {
                    result += this.separator;
                }
            }

            result += nouns[i].name;
            if (nouns[i].isSet("plural")) suffix = this.plural;
        }

        if (nouns.length > 1) suffix = this.plural;

        Output.print(`${result} ${suffix}.`);
    }
}

export class ObjectChooserDialog {
    constructor(game, message, cancel, error) {
        this.game = game;
        this.message = message;
        this.cancel = cancel;
        this.error = error;
    }

    execute(objects) {
        if (objects.length === 1) return objects[0];

        let success = false;
        let opt = 0;
        let result = null;

        while (!success) {
            Output.print(`${this.message}:`);
            objects.forEach((obj, index) => {
                Output.print(`${index + 1}) ${obj.article()}.`);
            });
            Output.print(`0) ${this.cancel}.`);

            const input = this.game.pause();

            try {
                opt = parseInt(input.trim(), 10);
            } catch (e) {
                this.printError();
                continue;
            }

            if (opt < 0 || opt > objects.length) {
                this.printError();
                continue;
            }

            if (opt) {
                result = objects[opt - 1];
            } else {
                Output.print("");
                Output.print(this.cancel);
            }

            success = true;
        }

        return result;
    }

    printError() {
        Output.print("");
        Output.print(this.error);
    }
}

export function loadListDialog(child) {
    return new ListDialog(
        child.getAttr("initial-message").getValue(),
        child.getAttr("separator").getValue(),
        child.getAttr("and-separator").getValue()
    );
}

export function loadPropperListDialog(child) {
    return new PropperListDialog(
        child.getAttr("singular").getValue(),
        child.getAttr("plural").getValue(),
        child.getAttr("separator").getValue(),
        child.getAttr("and-separator").getValue()
    );
}

export function loadObjectChooserDialog(game, child) {
    return new ObjectChooserDialog(
        game,
        child.getAttr("message").getValue(),
        child.getAttr("cancel").getValue(),
        child.getAttr("error").getValue()
    );
}
