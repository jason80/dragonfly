import { Output } from "./output.js";

/**
 * Input system of the game.
 *
 * @export
 * @class Input
 */
export class Input {

	/**
	 * Creates an instance of Input.
	 * @param {Book} book
	 * @memberof Input
	 */
	constructor(book) {
		this.book = book;
	}

	pause() {
			
	}

	/**
	 * Add an html input to output game and waits for the player sentence.
	 *
	 * @memberof Input
	 */
	createInput() {
		const inputContainer = document.createElement('div');
		Object.assign(inputContainer.style, {
			display: "inline-flex",
			width: "100%",
			alignItems: "center"
		});

		const promptSpan = document.createElement('span');
		Object.assign(promptSpan.style, this.book.getProperty("prompt-style"));
		promptSpan.textContent = this.book.getProperty("prompt");
		
		const input = document.createElement('input');
		input.type = 'text';
		Object.assign(input.style, this.book.getProperty("input-style"));
		
		inputContainer.appendChild(promptSpan);
		inputContainer.appendChild(input);
		Output.outputDiv.appendChild(inputContainer);

		input.focus();
		
		// Handle user input
		input.addEventListener('keydown', (event) => {
		if (event.key === 'Enter') {
			input.disabled = true;
			
			this.book.execute(input.value.trim());
			this.createInput();
		}
		});
	}

}
