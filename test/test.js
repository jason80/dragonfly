import { Book } from "../base/book.js";
import { Output } from "../base/output.js";

window.onload = function() {
	const book = new Book("console");

	book.setProperty("player", "-player");

	book.include("../templates/dict-es.dfml");
	book.include("../templates/dict-debug.dfml");
	book.include("test.dfml");
	
	book.run();
}
