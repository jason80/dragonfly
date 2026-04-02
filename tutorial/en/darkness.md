# Darkness

In Dragonfly, the concepts of "darkness" and "light" do not exist natively. We might say that a place is dark, but if the player checks their inventory or examines an object in it, they shouldn't be able to do so.

Stopping every action that requires "light" in a dark place would be very tedious. That is why the concept of "capturing all actions" exists.

```dfml
before(actions: "*", except: "LookAround, GoTo", cancel: true) {
  // ...
} 
```

This is translated as: `Before 'all actions', except 'LookAround' and 'GoTo', cancel the action.`

## Example

```dfml
dictionary {
   // The entrance of the grotto
   noun(names: "Mountain Path, path") {
      describe-place {
         "Reaching the base of the mountain, I can see the entrance to the grotto."
      }

     noun(names: "-player")

      connection(exit: "inside", destiny: "grotto")
   }

   // The grotto
   noun(names: "The Grotto, grotto, cave") {

      describe-place {
         "Darkness covers me. I should 'get out' of here."
      }

      // BEFORE ALL actions, EXCEPT examining the place and moving towards...
      before(actions: "*", except: "LookAround, GoTo", cancel: true) {
         "It's pitch black. I can't see anything..."
      }

      // We handle the excepted GoTo action
      before(actions: "GoTo", cancel: true) {

         // Only allows the "outside" exit
         if-direct-equals-exit(exit: "outside") {
            resume-event() break()
         }

         // Cancels any direction other than "outside"
         "I don't think I can go that way."
      }

      connection(exit: "outside", destiny: "path")
      connection(exit: "north", destiny: "cliff")
   }
}

```

Excepting the GoTo and LookAround actions gives the player the opportunity to leave the grotto and describe the place itself, respectively.

## Let there be light ...

In the following example, the place is described only if the player has a lamp. The lamp is located at the entrance of the grotto:

```dfml

// The entrance of the grotto
noun(names: "Mountain Path, path") {
   describe-place {
      "Reaching the base of the mountain, I can see the entrance to the grotto."
   }

   noun(names: "lamp, light") {
      describe-object {
         "An oil lamp, miraculously lit..."
      }
   }

   noun(names: "-player")

   connection(exit: "inside", destiny: "grotto")
}

// The grotto
noun(names: "The Grotto, grotto, cave") {

   describe-place {
      if-not-contains(container: "-player", instance: "lamp") {
         "Darkness covers me. I should 'get out' of here."
         break()
      }
      
      "The oil lamp reveals the room. There is a passage to the north."
   }

   // BEFORE ALL actions, EXCEPT examining the place and moving towards...
   before(actions: "*", except: "LookAround, GoTo", cancel: true) {
      if-contains(container: "-player", instance: "lamp") {
         resume-event() break()
      }

      if-contains(container: "grotto", instance: "lamp") {
         resume-event() break()
      }

      "It's pitch black. I can't see anything..."
   }

   // We handle the excepted GoTo action
   before(actions: "GoTo", cancel: true) {

      // Only allows the "outside" exit
      if-direct-equals-exit(exit: "outside") {
         resume-event() break()
      }

      // Only allows the "north" exit if the player has the lamp
      if-direct-equals-exit(exit: "north") {
         if-contains(container: "-player", instance: "lamp") {
            resume-event() break()
         }
      }

      // Cancels any direction other than "outside"
      "I don't think I can go that way."
   }

   connection(exit: "outside", destiny: "path")
   connection(exit: "north", destiny: "cliff")
}
```
