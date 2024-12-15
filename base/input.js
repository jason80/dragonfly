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
		this.continue_ = false;

		this.history = new Set();
		this.historyIndex = -1;
	}

	/**
	 * Wait for the user to press a key.
	 *
	 * @param {string} key key to continue.
	 * @memberof Input
	 */
	async pause(key) {
		const inputContainer = document.createElement('div');
		const input = document.createElement('input');
		inputContainer.appendChild(input);
		Output.outputDiv.appendChild(inputContainer);

		Object.assign(input.style, this.book.getProperty("input-style"));

		input.readOnly = true;
		input.focus();

		this.continue_ = false;

		input.addEventListener('keydown', event => {
			if (event.key === key) {
				this.continue_ = true;
				inputContainer.remove();
			}
		});

		await new Promise(resolve => {
			const checkInterval = setInterval(() => {
				if (this.continue_ === true) {
					clearInterval(checkInterval);
					resolve();
				}
			}, 100); // Revisión cada 100 ms
		});
	}

	/**
	 * Add an html input to output game and waits for the player sentence.
	 *
	 * @memberof Input
	 */
	async createInput() {
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
		input.addEventListener('keydown', async event => {
			if (event.key === 'Enter') {
				input.disabled = true;
				
				const value = input.value.trim();

				await this.book.execute(value);

				this.history.add(value);
				this.historyIndex = -1;

				await this.createInput();
			} else if (event.key === 'ArrowUp') {

				if (this.history.size === 0) return ;

				if (this.historyIndex === -1) {
					this.historyIndex = 0;
				} else {
					this.historyIndex ++;
					if (this.historyIndex >= this.history.size) this.historyIndex = 0;
				}

				input.value = Array.from(this.history)[this.historyIndex];
				input.select();
				event.preventDefault();
				
			} else if (event.key === 'ArrowDown') {
				if (this.history.size === 0) return ;

				if (this.historyIndex === -1) {
					this.historyIndex = this.history.size - 1;
				} else {
					this.historyIndex --;
					if (this.historyIndex < 0) this.historyIndex = this.history.size - 1;
				}

				input.value = Array.from(this.history)[this.historyIndex];
				input.select();
				event.preventDefault();
			}

		});
	}

}
