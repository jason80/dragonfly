import { DFMLElement } from "../dfml/js/main/element.js";
import { DFMLValue } from "../dfml/js/main/value.js";
import { Output } from "./output.js";
import { Utils } from "./utils.js";

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

	async run(result, action, conditions, responses) {

		for (const c of conditions) {
			if (!c.check(action)) return false;
		}

		Output.print(this.gameOverMessage, this.gameOverStyle);
		if (result === ResultType.VICTORY) {
			Output.print(this.victoryMessage, this.victoryStyle);
		} else {
			Output.print(this.defeatMessage, this.defeatStyle);
		}

		for (const r of responses) {
			await r.execute(action);
		}
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

		if (!Utils.expectedAttributes(node, "style")) return ;

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

