import { Book } from "../base/book.js";
import { Output } from "../base/output.js";

const button = document.getElementById("list");

window.onload = function() {
	const book = new Book("console");

	button.onclick = function() {
		book.dictionary.articles.forEach(v => {
			Output.print(v);
		});
	}

	book.include("../templates/dict-es.dfml").then(() => {
		book.include("test.dfml").then(() => {
			book.run();
		});
	});
}
