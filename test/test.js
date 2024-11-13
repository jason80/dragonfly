import { Book } from "../base/book.js";

window.onload = function() {
	const book = new Book("console");

	book.setProperty("player", "-player");
	book.setProperty("show-parsing-process", true);

	book.include("../templates/dict-es.dfml");
	book.include("../templates/dict-debug.dfml");
	book.include("test.dfml");
	
	book.run();
}
