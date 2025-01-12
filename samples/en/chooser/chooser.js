import { Book } from "../../../base/book.js"

window.onload = function() {
	const book = new Book("game-area");
	book.include("chooser.dfml");

	book.run();
}
