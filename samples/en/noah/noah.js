import { Book } from "https://jason80.github.io/dragonfly/base/book.js";
import { actions } from "https://jason80.github.io/dragonfly/base/actions.js";
import { SingleAction } from "https://jason80.github.io/dragonfly/base/action.js";

window.onload = function() {
   const book = new Book(
      "game-area",
      "noah.dfml"
   );

   book.run();
}

class MHelp extends SingleAction {
   constructor() {
      super();
   }
} actions.MHelp = MHelp;
