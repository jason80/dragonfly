import { loadResponses } from "./eventloader.js";
import { Utils } from "./utils.js";

export class Procedure {

   constructor() {
      this.name = "";
      this.responses = [];
   }

   async execute(action) {
      for (const response of this.responses) {
         await response.execute(action);
      }
   }

   load(node) {
      Utils.expectedAttributes(node, "name");
      this.name = node.getAttr("name").getValue();

      loadResponses(node, this.responses);
   }
}
