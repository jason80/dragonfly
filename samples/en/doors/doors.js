import { Book } from "../../../base/book.js";

window.onload  = () => {
	const book = new Book("game-area");

	book.include("doors.dfml");
	book.run();
};
