import { Book } from "../base/book.js";
import { Output } from "../base/output.js";

window.onload = function() {
	const book = new Book("console");

	book.include("../templates/dict-es.dfml").then(() => {
		book.include("test.dfml").then(() => {
			book.run();
		});
	});
}
