import { Book } from "../../../base/book.js";

window.onload  = () => {
	const book = new Book(
		"game-area",
		"doors.dfml"
	);
	book.run();
};
