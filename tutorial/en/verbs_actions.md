## Verb and Actions

English | [Español](../es/verbs_actions.md)

When the player types a sentence, Dragonfly parses it syntactically to identify the verb and the parameters. For example, if the player types look `examine box`, Dragonfly identifies the verb `examine` and the parameter `box`.

However, identifying the verb is only the first step. Next, the parser must determine which action corresponds to that verb. To handle this, Dragonfly uses an action system.

Each verb can have one or more associated actions. For instance, the verb look can have an action for `look` an object, another `look` a location, another for `look` inside a container, and so on.

Let's see the difference in the following table:

| Sentence | Action | Detail | Parameters |
| --- | --- | --- | --- |
| look | LookAround | Shows the player's surroundings | N/A
| look inside the box | LookInside | Lists the objects inside the container | box
| look at the ring | ExamineObject | Description of a specific object | ring

The first one takes no parameters, while the second and third ones do. These are direct objects.

When an action is executed, a series of events are sent to specific objects.

In the case of LookAround, events are sent to the current location (where the player is). In the case of LookInside, events are sent to the direct object, just like in ExamineObject.

## Events

There are two events sent to objects when an action is executed:

* **before**
* **after**

For the following sentence:

```leave the bracelet in the chest```

The following steps will be executed:

1) The parser analyzes and identifies the `LeaveIn` action with two parameters: bracelet and chest (direct and indirect object).

2) It verifies that the objects (direct and indirect) exist. If they do, the objects must be within the player's reach. *Otherwise, THE ACTION IS CANCELED, and an error message is displayed*.

3) **Before Event**: The `before` event is sent to each of the objects involved (bracelet and chest).
It is possible for one of the objects to cancel the action, as the developer can capture the event with the option to cancel it. *If this happens, THE ACTION IS CANCELED without displaying any message*.

4) It executes action-specific checks. In this case, it verifies that the objects are not the 'player' themselves, that the chest is a 'container' and that it is open if it is a 'closable' object. *If these conditions are not met, THE ACTION IS CANCELED, and an error message is displayed*.

5) **After Event**: It proceeds by sending the `after` event to each of the involved objects (bracelet and chest). It is possible for one of the objects to cancel the action. *If this happens, THE ACTION IS CANCELED without displaying any message*.

6) At this point, the action is fully executed. The bracelet is moved to the chest, and a confirmation message is displayed: `I leave the bracelet in the chest`.

### Capture Events

#### before

Let’s assume I have the following object inside any given location:

```
noun(names: "log, trunk, wood") {
   describe-object() {
      "It is a dry, charred log, recently used for a campfire."
   }
}
```

By using `take log` or `pick up the log`, the player can collect the log and carry it with them.

We are going to cancel this action so the player cannot pick up the log. To do this, we capture the `before` event of the `TakeObject` action and cancel it:

```dfml
noun(names: "log, trunk, wood") {
   describe-object() {
      "It is a dry, charred log, recently used for a campfire."
   }

   before(actions: "TakeObject", cancel: true) {
      "The log is hot! I'd better wait for it to cool down a bit before picking it up."
   }
}
```

Note: You can capture several actions at once, for example: `before(actions: "TakeObject, TouchObject, PushObject", cancel: true)`. In this case, the player will not be able to pick up, touch, or push the log.

If the event is not canceled `cancel: false`, the action will execute normally, and we would get the following result:

```> take the log```
```The log is hot! I'd better wait for it to cool down a bit before picking it up.```
```I take the log.```

The action executes normally, and the log moves to the player's inventory.

#### after

The after event can be captured in the same way as the before event, but it executes after the action has been fully completed. For example, if we want to show a message after the player has picked up the log (and hide the default message), we can do the following:

```dfml
noun(names: "log, trunk, wood") {
   describe-object() {
      "It is a dry, charred log, recently used for a campfire."
   }

   after(actions: "TakeObject", cancel: true) {
      "I pick up the log; it’s hot, but I take it with me anyway."
   }
}
```

In the same way, if we do not cancel the event, the default message will be displayed along with the custom message:

```> pick up the log```
```I pick up the log; it’s hot, but I take it with me anyway.```
```I take the log.```

[<< Nouns](nouns.md) | [Responses >>>](responses.md)
