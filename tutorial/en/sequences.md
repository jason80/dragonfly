# Sequences

English | [Español](../es/sequences.md)

Sequences are responses that group other responses together. Internally, they hold a counter: when the sequence "executes," it triggers the response pointed to by the counter index and then increments it. Once all responses have been executed, the sequence starts over from the first one.

```dfml
sequence {
   "The vendor says: 'Hello, welcome to my store!'"
   "The vendor says: 'Don't forget to check my prices.'"
   "The vendor says: 'I'm here to help you with your purchases.'"
   "The vendor says: 'Potions are on sale!'"
   "The vendor says: 'I should open on Saturdays ...'"
}
```

As a sequence is a response, it can be nested inside an event or a procedure. Let's see an example of a procedure to activate the vendor's chatter:

```dfml
procedure(name: "vendor-talks") {

   "The vendor says:"

   sequence {
      append { "'Hello, welcome to my store!'" }
      append { "'Don't forget to check my prices.'" }
      append { "'I'm here to help you with your purchases.'" }
      append { "'Potions are on sale!'" }
      append { "'I should open on Saturdays ...'" } 
   }
}
```

```dfml
noun(names: "The Store, store") {
   describe-place() {
      // ....
   }

   // Define the vendor inside the store, among others
   // ....

   // Call the procedure every time the player does something in the store.
   after(actions: "*", except: "GoTo") {
      call(procedure: "vendor-talks")
   } 
}
```

---

## Chances

It is quite annoying that the vendor talks every time the player does something in the store. To make it talk less, we can add a chance to the sequence:

```dfml

sequence(chance: 0.2) {
   append { "'Hello, welcome to my store!'" }
   append { "'Don't forget to check my prices.'" }
   ...
}
```

Now, the vendor will talk with a 20% chance for each action the player does in the store. By default, the chance is 100% (1.0).

---

## Shuffling

If we want the vendor to talk in a random order, we can do the following:

```dfml
sequence(shuffle: true) {
   append { "'Hello, welcome to my store!'" }
   append { "'Don't forget to check my prices.'" }
   append { "'I'm here to help you with your purchases.'" }
   append { "'Potions are on sale!'" }
   append { "'I should open on Saturdays ...'" }
}
```

Dragonfly *shuffles the responses only at the start of the game*, when the dictionary is loaded. Responses are NOT picked at random during runtime.

---

## Ambient Sounds

In a similar way, we can simulate ambient sounds by adding an event and taking advantage of the random features and appearance chances of sequences.

Phrases like:

```dfml
sequence(shuffle: true, chance: 0.2) {
   print(style: "class: df-ambient") { "A distant scream is heard..." }
   print(style: "class: df-ambient") { "Noises are heard within the walls..." }
   print(style: "class: df-ambient") { "Crickets are chirping everywhere..." }
   ...
}
```
