import { Book } from "https://jason80.github.io/dragonfly/base/book.js"

window.onload = function() {
	const book = new Book(
		"game-area",
		"bosque.dfml"
	);

	book.run();
}
