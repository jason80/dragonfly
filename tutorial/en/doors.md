# Doors

Doors are objects that can be opened and closed. The mechanism ensures that the player cannot pass through an exit if the door is closed. No external libraries are needed to create doors.

### The Problem

In Dragonfly, a noun cannot be inside two containers at the same time:
How is it possible to create a door? Since a door is an object shared by two rooms.

### The Solution

The solution consists of creating two doors, one in each room. Then, synchronize their opening and closing. The player will think it is a single door, but depending on which room they are in, they will see one door or the other.

First, we define the rooms with the two doors. One door is an exact copy of the other; only different names are added to identify them later:

```dfml
noun(names: "The Dining Room, dining-room") {
   describe-place() {
      "A table surrounded by chairs occupies the whole room. Plates and cutlery are arranged in a balanced way. To the north, there is a door."
   }

   noun(names: "player")

   noun(names: "door, d-diningroom-kitchen") {
      set { "female" "fixed" "scene" "closable" "closed" }

      describe-object() {
         "A wooden door with a metal handle."
      }
   }

   connection(exit: "north", destiny: "kitchen")
}

noun(names: "The Kitchen, kitchen") {
   describe-place() {
      "Countertops and shelves full of preserve jars. Two huge ovens can be seen on one side. To the south, you return to the dining room."
   }

   noun(names: "door, d-kitchen-diningroom") {
      set { "female" "fixed" "scene" "closable" "closed" }

      describe-object() {
         "A wooden door with a metal handle."
      }
   }

   connection(exit: "south", destiny: "dining-room")
}

```

Now all that remains is to:

* **Synchronize the doors**: When one is opened, the other opens, and vice versa.

* **Block the player's path**: When the doors are closed, the player cannot move through the exit.

### Synchronizing the doors

By modifying the open and close events of one door, the other door is opened or closed:

```dfml
noun(names: "door, d-diningroom-kitchen") {
   set { "female" "fixed" "scene" "closable" "closed" }

   describe-object() {
      "A wooden door with a metal handle."
   }

   // Opening this door opens the other one
   after(actions: "OpenObject", cancel: false) {
      attr(instance: "d-kitchen-diningroom", unset: "closed")
   }

   // Closing this door closes the other one
   after(actions: "CloseObject", cancel: false) {
      attr(instance: "d-kitchen-diningroom", set: "closed")
   }
}

```

```dfml
noun(names: "door, d-kitchen-diningroom") {
   set { "female" "fixed" "scene" "closable" "closed" }

   describe-object() {
      "A wooden door with a metal handle."
   }

   // Opening this door opens the other one
   after(actions: "OpenObject", cancel: false) {
      attr(instance: "d-diningroom-kitchen", unset: "closed")
   }

   // Closing this door closes the other one
   after(actions: "CloseObject", cancel: false) {
      attr(instance: "d-diningroom-kitchen", set: "closed")
   }
}
```

### Blocking the player's path

By modifying the GoTo event of the current location, the path is blocked if the doors are closed:

```dfml
noun(names: "The Dining Room, dining-room") {

   // ...

   // If the exit is "north" and the door is closed, the path is blocked.
   before(actions: "GoTo", cancel: true) {
      if-direct-equals-exit(exit: "north")
      if-is-set(instance: "d-diningroom-kitchen", attr: "closed")

      "The door is closed."
   }
}
```

```dfml
noun(names: "The Kitchen, kitchen") {

   // ...

   // If the exit is "south" and the door is closed, the path is blocked.
   before(actions: "GoTo", cancel: true) {
      if-direct-equals-exit(exit: "south")
      if-is-set(instance: "d-kitchen-diningroom", attr: "closed")

      "The door is closed."
   }
}
```
