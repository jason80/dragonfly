## Inventory limit

English | [Español](../es/inventory.md)

The inventory can be limited using different magnitudes that Dragonfly recognizes, and they can be combined with each other.

* **Capacity:**

The simplest to manage. Set a `capacity` variable with the maximum number of objects the player can carry:

```
noun(names: "player") {
   // Can carry up to 5 objects.
   variable(name: "capacity", value: "5")
}
```

When the player exceeds the maximum while trying to obtain an object, the `inventory-full` response will be triggered. The same will happen with the following magnitudes.

* **Weight:**

Maximum weight the player can lift.
First, set the maximum:

```
noun(names: "player") {
   // Can carry up to a weight of 100.
   variable(name: "weight", value: "100")
}
```

You must remember to set the weight of the objects the player will carry:

```
noun(names: "keys") {
   variable(name: "weight", value: "2")
}

noun(names: "flashlight") {
   variable(name: "weight", value: "10")
}

noun(names: "wallet") {
   variable(name: "weight", value: "5")
}

```
* **Valume:**

Volume works the same way as weight. Just replace the variable name with `volume`.
