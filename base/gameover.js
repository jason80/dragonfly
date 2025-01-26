import { DFMLElement } from "../dfml/js/main/element.js";
import { DFMLValue } from "../dfml/js/main/value.js";
import { Output } from "./output.js";
import { DFMLPersistenceSystem } from "./persistence.js";

export class ResultType {
  static VICTORY = 0;
  static DEFEAT = 1;
}

export class GameOver {
	constructor(dictionary) {
		this.dictionary = dictionary;
		this.gameOverMessage = "Game over";
		this.gameOverStyle = "";
		this.victoryMessage = "with VICTORY !";
		this.victoryStyle = "";
		this.defeatMessage = "with defeat";
		this.defeatStyle = "";
	}

	async run(result, message) {
		Output.print(this.gameOverMessage, this.gameOverStyle);
		if (result === ResultType.VICTORY) {
			Output.print(this.victoryMessage, this.victoryStyle);
		} else {
			Output.print(this.defeatMessage, this.defeatStyle);
		}
		Output.print(message);

		await this.dictionary.book.input.pause("Enter");

		// TODO: improve restart game
		const p = new DFMLPersistenceSystem(this.dictionary);
		p.load(this.dictionary.book.initialState);

		const clearVerb = this.dictionary.verbByAction("Clear");
		if (clearVerb)
			await this.dictionary.book.execute(clearVerb.getName());

		this.dictionary.book.showTitle();

		const lookVerb = this.dictionary.verbByAction("LookAround");
		if (lookVerb)
			await this.dictionary.book.execute(lookVerb.getName());
	}

	load(node) {
		node.children.forEach((e) => {
			if (e.getElementType() === DFMLElement.NODE) {
				if (e.getName() === "game-over-message") {
					[this.gameOverMessage, this.gameOverStyle] = this.loadMessage(e);
				}
				if (e.getName() === "victory-message") {
					[this.victoryMessage, this.victoryStyle] = this.loadMessage(e);
				}
				if (e.getName() === "defeat-message") {
					[this.defeatMessage, this.defeatStyle] = this.loadMessage(e);
				}
			}
		});
	}

	loadMessage(node) {
		let style = "";
		if (node.hasAttr("style")) {
			style = node.getAttr("style").getValue();
		}

		node.children.forEach((e)=> {
			if (e.getElementType() === DFMLElement.DATA) {
				if (e.getValue().getType() === DFMLValue.STRING) {
					return [style, e.getValue().getValue()];
				}
			}
		});

		return [style, ""];
	}
}

