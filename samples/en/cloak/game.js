import { Book } from "https://jason80.github.io/dragonfly/base/book.js";

window.onload = () => {
   const book = new Book("game-area", "game.dfml");
   book.run();
};
