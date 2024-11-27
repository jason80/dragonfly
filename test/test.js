import { Book } from "../base/book.js";

window.onload = function() {
	const book = new Book("console");

	book.setProperty("player", "-player");
	book.setProperty("show-parsing-process", false);
	book.setProperty("hide-title", false);

	book.include("../templates/dict-es.dfml");
	book.include("../templates/dict-debug.dfml");
	book.include("book.dfml");
	
	book.run();
}
