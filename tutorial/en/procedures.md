# Procedures

A procedure groups responses under a name. These responses can be executed by simply calling the name of the procedure.

It is analogous to a subroutine of the traditional languages and serves to reuse code. There is a special response called `call` that calls the procedure defined.

## Defining a procedure

Procedures are defined only in the `dictionary` and `noun` nodes, and are ALL GLOBAL, that is, you can declare a procedure in a noun and call it from anywhere.

Let's define some procedures that determine the end of a game:

```dfml
dictionary {
   procedure(name: "final-good") {
      print("¡ You won !", style: "color: green; font-weight: bold;")

      "You completed the game with success." pause()

      restart-game() break()
   }

   procedure(name: "final-bad") {
      print("¡ You lost !", style: "color: red; font-weight: bold;")

      "The next time will be better." pause()

      restart-game() break()
   }
}
```

## Calling a procedure

The procedure is called by response `call`. For example:

```dfml
noun(name: "The Final Tunnel, final-tunnel") {
   describe-place {
      "I can see light. The exit is close. I have to go north."
   }

   before(actions: "GoTo") {
      if-direct-equals-exit(exit: "north") {
         call(procedure: "final-good")
      }
   }

   connection(exit: "north", destiny: "outside")
}
```

When a procedure is called, envent information is inherited: the action, the direct object and the indirect object, the flow control, etc. Therefore, you can call responses like `cancel-event`, `resume-event` and `break`.

[<<< The Parser](parser.md)
