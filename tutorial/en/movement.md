## Movement

English | [Spanish](../es/movement.md "Movement tutorial in Spanish")

Mostly conversational games do not limit themselves to one place. The way to indicate the player to move through them is with cardinal points. Let's say that there is a path to the `east` of our garden. Let's create the place:

```
noun(names: "The Cobblestone Path, path") {
   describe-place() {
      "I find myself walking along a cobblestone path. It continues to the east. To the west, it leads back to the garden."
   }
}
```

By saying 'go east', we would tell the player to head east. But in this case, it won't work.

This is because there is still no `connection` between the garden and the cobblestone path.

Let's add it:

```
noun(names: "The Garden, garden") {
   # Garden definition goes here
   # ...

   # Adding the connection to the east
   connection(exit: "east", destiny: "path")
}
```

And to go back to the garden via the west:

```
noun(names: "The Cobblestone Path, path") {
   # Path definition goes here
   # ...

   # Adding the connection to the west
   connection(exit: "west", destiny: "garden")
}
```

Now the player can `go east` or `west` navigating between the places.

### The exits:

For the connections to work, there must be exits. All the possible exits come from the dictionary "dict-xx.dfml". Here is a complete list:

<ul>

<li>north, n</li>
<li>south, s</li>
<li>east, e</li>
<li>west, w</li>

<li>northeast, ne</li>
<li>northwest, nw</li>
<li>southeast, se</li>
<li>southwest, sw</li>

<li>up, u, climb, ascend</li>
<li>down, d, descend</li>
<li>inside, in, enter</li>
<li>outside, out side, out, leave, exit</li>
<li>otherside, other side, cross</li>

</ul>

The syntax to move can be `"go to <exit>"`. You can also write the exit name, for example `"north"` or `"n"`. Dragonfly will check if it is a possible exit and, if so, it will execute the action "go to" of the case above.

Of course, if we try to 'go south' in our garden, the result will be:

*I can't go that way.*

Since the connection with the 'south' exit does not exist in this location.

[<<< Start](start.md) | [Open and close >>>](open_close.md)

