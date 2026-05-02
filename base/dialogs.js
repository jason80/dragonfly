import { Output } from "./output.js";
import { Utils } from "./utils.js";

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

export class ProperListDialog {
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

            result += nouns[i].getName();
            if (nouns[i].isSet("plural")) suffix = this.plural;
        }

        if (nouns.length > 1) suffix = this.plural;

        Output.print(`${result} ${suffix}.`);
    }
}

export class ObjectChooserDialog {
    constructor(book, message, cancel, error) {
        this.book = book;
        this.message = message;
        this.cancel = cancel;
        this.error = error;
    }

    async execute(objects) {
        if (objects.length === 1) return objects[0];

        let success = false;
        let result = null;

        while (!success) {
            Output.print(`${this.message}:`);
            objects.forEach((obj, index) => {
                Output.print(`${index + 1}) ${obj.article()}.`);
            });
            Output.print(`0) ${this.cancel}.`);

            const input = await this.userInput();
            
            const opt = parseInt(input.trim(), 10);
			if (isNaN(opt)) {
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

	async userInput() {
		const inputContainer = document.createElement('div');
		const input = document.createElement('input');
		inputContainer.appendChild(input);
		Output.outputDiv.appendChild(inputContainer);

        Utils.applyStyle(input, this.book.getProperty("input-style"));

		input.focus();

		this.continue_ = false;

		input.addEventListener('keydown', event => {
			if (event.key === "Enter") {
				this.continue_ = true;
			}
		});

		let result = "";

		await new Promise(resolve => {
			const checkInterval = setInterval(() => {
				if (this.continue_ === true) {
					clearInterval(checkInterval);
					result = input.value.trim();
					resolve();
				}
			}, 100);
		});

		return result;
	}

    printError() {
        Output.print("");
        Output.print(this.error);
    }
}

export class InventoryDialog {
    constructor(book, youHave, youWear, separator, andSeparator) {
        this.book = book;
        this.youHave = youHave;
        this.youWear = youWear;
        this.separator = separator;
        this.andSeparator = andSeparator;
    }

    async execute() {

        if (this.book.player.children().length === 0) return;

        const items = [];
        const wear = [];

        this.book.player.children().forEach(n => {
            if (n.isSet("worn")) wear.push(n);
            else items.push(n);
        });

        if (items.length !== 0) {
            const dialog = new ListDialog(this.youHave, this.separator, this.andSeparator);
            dialog.execute(items);
        }

        if (wear.length !== 0) {
            const dialog = new ListDialog(this.youWear, this.separator, this.andSeparator);
            dialog.execute(wear);
        }
    }
};

export function loadListDialog(child) {

	if (!Utils.expectedAttributes(child, "initial-message",
			"separator", "and-separator")) return null;

    return new ListDialog(
        child.getAttr("initial-message").getValue(),
        child.getAttr("separator").getValue(),
        child.getAttr("and-separator").getValue()
    );
}

export function loadProperListDialog(child) {

	if (!Utils.expectedAttributes(child, "singular", "plural",
		"separator", "and-separator")) return null;

    return new ProperListDialog(
        child.getAttr("singular").getValue(),
        child.getAttr("plural").getValue(),
        child.getAttr("separator").getValue(),
        child.getAttr("and-separator").getValue()
    );
}

export function loadObjectChooserDialog(book, child) {

	if (!Utils.expectedAttributes(child, "message", "cancel", "error")) return null;

    return new ObjectChooserDialog(
        book,
        child.getAttr("message").getValue(),
        child.getAttr("cancel").getValue(),
        child.getAttr("error").getValue()
    );
}

export function loadInventoryDialog(book, child) {

    if (!Utils.expectedAttributes(child, "you-have", "you-wear", "separator", "and-separator")) return null;

    return new InventoryDialog(
        book,
        child.getAttr("you-have").getValue(),
        child.getAttr("you-wear").getValue(),
        child.getAttr("separator").getValue(),
        child.getAttr("and-separator").getValue()
    );
}
