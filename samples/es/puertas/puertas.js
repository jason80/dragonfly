import { Book } from "../../../base/book.js";

window.onload  = () => {
	const book = new Book("game-area");

	book.include("puertas.dfml");
	book.run();
};
