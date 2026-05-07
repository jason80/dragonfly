

export function check_inventory(action, player, noun) {
   const capacity = "capacity" in player.variables ?
      parseInt(player.getVariable("capacity")) : 0;

   if (capacity == 0) return true;

   if (capacity <= player.children().length) {
      return action.fireResponse("inventory-full");
   }

   return true;
}
