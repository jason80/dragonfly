import { Book } from "../../../base/book.js";

window.onload  = () => {
	const book = new Book(
		"game-area",
		"puertas.dfml"
	);
	book.run();
};
