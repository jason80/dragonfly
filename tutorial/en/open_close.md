## Open and Close

English | [Español](../es/open_close.md)

In many interactive fiction games, the player encounters objects that can be opened or closed. To handle this, Dragonfly features an attribute system for objects.

Suppose there is a wooden box on our path. To create it, we write:

```
noun(names: "wooden box, box, wood") {

   set { "container" }

   describe-object() {
      "It is a small wooden box. It has a hinged lid."
   }

   # Inside the box there is a ring
   noun(names: "ring") {
      describe-object() {
         "It is a gold ring with an embedded gemstone."
      }
   }
}
```

The wooden box is a container:

```
set { "container" }
```

Therefore, the player will be able to see the things inside it.

`look inside the box` or `look in the box` and then: `take the ring from the box` or `get the ring from the box`.

But, what if we want the player to have to open the box to see what is inside?

Dragonfly allows objects to be `closable`. To do this, we add the closable attribute and also `closed` so that the box starts out closed:

```
set { "container" "closable" "closed" }
```

Now, the player won't be able to see what is inside the box unless they open it. To do so, they must use the command `open the box` or `open box`. And to close it: `close the box` or `close box`.

An object does not necessarily have to be a container to be closable. For example, a door can be closed but not contain anything.

If you want to know more, check the [Doors](doors.md) section to learn how to create them.

[<<< Movement](movement.md) | [Nouns >>>](nouns.md)
