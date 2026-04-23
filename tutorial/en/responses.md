## Responses

English | [Español](../es/responses.md)

When handling an event, such as **before**, we observed that we can display a custom message whether the action is canceled or not:

```dfml
noun(names: "snake, viper") {
   describe-object() {
      "It looks like a venomous snake; I'd better not get too close."
   }

   before(actions: "TakeObject, TouchObject", cancel: true) {
      "No way am I getting near that!"
   }
}
```

That message `"No way am I getting near that!"` is an action response.

Another way to represent the same response is:

```dfml
print {
   "No way am I getting near that!"
}
```

In both cases, the result is the same, and Dragonfly will replace it with the native `response` node:

```dfml
response(class: "Print") {
   "No way am I getting near that!"
}
```

There are different types of responses, each with its own function. Let's make the snake move away from the player if they try to touch it:

```dfml
noun(names: "snake, viper") {
   describe-object() {
      "It looks like a venomous snake; I'd better not get too close."
   }

   before(actions: "TakeObject, TouchObject", cancel: true) {
      "The snake slithers away quickly."
      move(instance: "snake", destiny: "another-room")
   }
}
```

As you can see, the `move` function is an action response that moves an object to another location. In this case, we move the snake to another room. And yes, there can be multiple responses within the same event.

In this instance, Dragonfly will also transform the `move` response into `response(class: "Move", instance: "snake", destiny: "another-room")`.

If we don't want to move the snake to another room but instead want to take it to the root of the object tree, we can use:

```dfml
root(instance: "snake")
```

Internally, root will change the parent of "snake" to `null` and take it to the root of the object tree.

Some responses are described in the following table:

Response | Description
--- | ---
print | Displays a custom message.
append | As `print`, but the message is added to the end of the last message shown.
attr | Adds or removes an attribute to an object.
variable-set | Sets the value of a variable to an object.
move | Moves an object to another location.
root | Moves an object to the root of the object tree.
tip | Displays a message of help to the player.
execute | Executes a sentence as if the player did it: eg: `throw the knife`.
add-connection | Adds a connection between two rooms.
remove-connection | Removes a connection between two rooms.
show-title | Displays a title of the game.
run-conversation | Starts a conversation with a character.
pause | Waits for the player to press `Enter`.
clear | Clears the screen.
restart-game | Restarts the game.

[<<< Verbs and Actions](verbs_actions.md) | [Conditions >>>](conditions.md)
