## Conditions

English | [Español](../es/conditions.md)

Attending an event becomes more dynamic when you can add conditions to the side of the responses. This allows the event to only execute if the conditions are met.

Let's suppose we want to describe a place showing a text when the same place is visited for the first time, and another text when it is visited again. To do this, we can use a condition that reviews if the place was visited or not.

```dfml
noun(names: "The Swamp, swamp") {

   describe-place() {
      if-is-not-set(instance: "swamp", attr: "described") {
         "Once I get to the swamp, I realize it is a very humid and lush place. The air is dense and the smell of wet earth is strong. It is a mysterious and a little unsettling place."
      }

      if-is-set(instance: "swamp", attr: "described") {
         "Between the dense air and the smell of wet earth, I return to this unsettling place."
      }

      append { "A sort of path between the mud seeps to the west, by the south I return to the forest." }
   }
}
```

In this way, the first time the `LookAround` event is executed in the `The Swamp` location, the first text will be displayed and the `described` attribute will be set. In subsequent executions of the same event, the second text will be shown. The third event, `LookAround`, will always execute regardless of whether the location has been visited before, and that text will be appended after the last line displayed.

### Nested conditions

There can be more than one condition in a single event. The way to present them in the event is the following:

```dfml
noun(names: "letter, paper, envelope, mail") {

   after(actions: "ReadObject", cancel: false) {
      if-contains(instance: "candle", container: "office") {
         if-is-set(instance: "candle", attr: "lit") {
            if-contains(instance: "glasses", container: "player") {
               "It is another letter from the magistrate."
               cancel-event()
            }
         }
      }
   }
}
```

In this case, the `"It is another letter from the magistrate."` text will only shown if the candle is in the office, the candle is lit, and the player has the glasses. If any of these conditions are not met, the event will not cancel and will show the default message: `"Cannot read the letter"`.

Just like with the responses, Dragonfly will replace the conditions with their equivalents using the native `response` node. Conditions are also Javascript classes that extend from `Response`.

The equivalent of `if-is-set(instance: "candle", attr: "lit")` is the following:

```dfml
response(class: "IfIsSet", instance: "candle", attr: "lit") {
	// inner responses
}
```

There are some conditions available:

Condition | Description
--- | ---
if-is-set | Checks if a noun has an attribute set.
if-is-not-set | Checks if a noun has an attribute not set.
if-direct-equals-exit | Checks if the `direct object` equals a `exit` registered in the dictionary.
if-contains | Checks if a noun contains another noun.
if-not-contains | Checks if a noun does not contain another noun.
if-direct-equals | Checks if the `direct object` equals another noun.
if-direct-not-equals | Checks if the `direct object` does not equal another noun.
if-indirect-equals | Checks if the `indirect object` equals another noun.
if-indirect-not-equals | Checks if the `indirect object` does not equal another noun.
if-variable-equals | Checks if the value of a variable equals a value.
if-connection-exists | Checks if there is a connection in a place indicating its exit.
if-connection-not-exists | Checks if there is no connection in a place indicating its exit.

[<<< Responses](responses.md) | [The Parser >>>](parser.md)
