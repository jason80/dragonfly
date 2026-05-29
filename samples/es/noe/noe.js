import { Book } from "https://jason80.github.io/dragonfly/base/book.js";
import { actions } from "https://jason80.github.io/dragonfly/base/actions.js";
import { SingleAction } from "https://jason80.github.io/dragonfly/base/action.js";

import { Utils } from "https://jason80.github.io/dragonfly/base/utils.js";

window.onload = function() {
   const book = new Book(
      "game-area",
      "noe.dfml"
   );

   book.run();
}

class MHelp extends SingleAction {
   constructor() {
      super();
   }
} actions.MHelp = MHelp;

window.switchStyle = function() {
   const style = document.getElementById('dragonfly-style');
   
   if (style.href.endsWith("dragonfly-dark.css")) {
      Utils.switchStyle("https://jason80.github.io/dragonfly/style/dragonfly-light.css");
   } else {
      Utils.switchStyle("https://jason80.github.io/dragonfly/style/dragonfly-dark.css");
   }
}
