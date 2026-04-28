import { Book } from "../../../base/book.js";

window.onload = () => {
   const book = new Book("game-area", "game.dfml");
   book.run();
};
