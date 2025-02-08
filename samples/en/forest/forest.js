import { Book } from "../../../base/book.js"

window.onload = function() {
	const book = new Book(
		"game-area",
		"forest.dfml"
	);

	book.run();
}
