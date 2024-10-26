import { Book } from "../base/book.js";

window.onload = function() {
	const book = new Book("console");

	book.include("../templates/dict-es.dfml").then(() => {
		book.include("test.dfml").then(() => {
			book.run();
		});
	});
}
