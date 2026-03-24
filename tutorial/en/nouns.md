## Nouns

English | [Español](../es/nouns.md)

As mentioned before, nouns are the objects within the game. It is a type derived from `Entity` and has the `multiname` property, meaning it can have several names.

It is recommended that the developer adds an internal name for certain nouns; these can include hyphens, for example (the parser removes hyphens when analyzing player input):

```dfml
noun(names: "Main Entrance, -castle-entrance") {
   describe-place() {
      "It is the main entrance to the castle. It has a large wooden door with iron fittings."
   }
}
```

---

Dragonfly knows when two objects or more have the same name, and in that case, it will ask the player which of them you mean. For example:

```dfml
noun(names: "red ball, ball") {
   describe-object() {
	  "It is a bright red ball."
   }
}

noun(names: "blue ball, ball") {
   describe-object() {
	  "It is a bright blue ball."
   }
}
```

The balls are in the same location. When the player tries to get the ball or look at the ball, the parser will ask which of the balls they mean.

Another feature of multiname is how lenient it is when referring to an object.

If we have an object named ñandú, the player can refer to it as ñandu, ñandú, nandu, nándu, etc. The entity itself recognizes that all these forms refer to it.

This ensures the player doesn't have to worry about typing the exact name of the object, which improves the gameplay experience.

---

## Containers

In Dragonfly, *all nouns are containers*. There is a tree-like hierarchy representing children with a single parent. *An object cannot be in two places at the same time*. So far, the garden example is represented as follows:

Inside `garden` there are four nouns, and one of them is the `player`. There are no limits for the adventure author when organizing the structure of nouns: *we can put a truck inside a pin*. Conceptually it is wrong, but Dragonfly allows it. This is why the player is limited.

The player will not be able to `"put/insert things inside the object"` if the object does not have the `"container"` attribute set. Nor will they be able to `"look inside the object"`.

We can create a water fountain inside the garden. And inside the fountain, a key. To do this, we add the following code:

```dfml
noun(names: "water fountain, fountain, water") {
   set { "fixed" "scene" "container" }

   describe-object {
      "A water fountain sprays jets of water, producing a relaxing sound."
   }

   noun(names: "key, ancient key") {
      describe-object {
         "An ancient bronze key."
      }
   }
}
```

Try now `"look in the fountain"`, `"take the key from the fountain"`, and `"leave the key in the fountain"`. When you take something out of something else, the object goes into the inventory.

---

## Life of Nouns

Nouns are created when the game starts and remain until it ends. *No nouns are created or destroyed while the game is running*.

To make a new noun appear, the developer must move the object from a special place, a place the player doesn't even suspect exists. The same goes for destroying it: it is moved to that place.

A recommended practice is to create a special location inaccessible to the player and move objects in and out of there.

## Persistence

Type `save` to save the game. Dragonfly handles saving the game without the developer having to worry about it.

Type `load` to recover the game.

#### Where is it saved?

Dragonfly saves the game in the browser. It is not lost if the browser is closed, restarted, or refreshed.

The only way to lose the game is to clear the browser data.

#### How is it saved?

It is saved in the browser's Local Storage, and only information about the nouns that *can change during the game is stored*:

* The `identifier` (id): a unique numerical value for each noun. *Only used for the save system*.
* The names.
* The `id` of the parent container: if the object is at the `root`, the id is 0 (zero).
* The attributes.
* The variables.
* The connections.

*Note: Outdated saved games can cause issues. As the developer creates new objects in the game, it is good practice to update saved games with `save`.*

#### Initial State in Memory

The initial state of the game is saved in memory when the game starts. This is used to `restart` the game when it's game over. By calling the `restart-game()` response, the initial state of the match is restored.

[<<< Open and Close](open_close.md) | [Verbs and Actions >>>](verbs_actions.md)
