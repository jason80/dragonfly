# Variables

English | [Español](./es/variables.md)

Nouns can have variables. Variables allow you to store information that can change during the game. The type of data they store are character strings, always.

Just like attributes, you can declare variables in the body of the noun:

```dfml
noun(names: "matches, matches, match, match") {
   variable(name: "quantity", value: "3")

   describe-object() {
      "These matches are used to light. There are $(matches.quantity) matches."
   }
}
```

---

### Responses

There are several responses to manipulate variables:

Response | Description | Usage
--- | --- | ---
variable-set | Sets the value of a variable to an object. | `variable-set(instance: "matches", name: "quantity", value: "5")`
variable-add | Adds a value to a variable. The value must be a number and if not specified, the value will be "1" | `variable-add(instance: "matches", name: "quantity", value: "2")`.
variable-sub | Subtracts a value to a variable. The result is the same as `variable-add` | `variable-sub(instance: "matches", name: "quantity", value: "2")`.

All these responses have the same parameters and they can be interpolated.

```dfml
variable-set(instance: "player", name: "steps", value: "$(counter.steps)") {
   
}
```

---

### Conditions

Condition | Description
--- | ---
if-variable-equals | It is fulfilled if the value of a variable is equal to a value given.
if-variable-not-equals | It is fulfilled if the value of a variable is not equal to a value given.
if-variable-lt | It is fulfilled if the value of a variable is less than a value given.
if-variable-lte | It is fulfilled if the value of a variable is less than or equal to a value given.
if-variable-gt | It is fulfilled if the value of a variable is greater than a value given.
if-variable-gte | It is fulfilled if the value of a variable is greater than or equal to a value given.

All these conditions have the same parameters and they can be interpolated.

---

### Global variables (Not implemented)

Global variables are not contained by nouns. The way to declare a global variable is inside the `dictionary` node.

The way to modify or access a global variable is by omitting the `instance` attribute in responses and conditions.

And the way to interpolate a global variable is simply `$(variable)` (also omitting the noun).

[<<< Procedures](procedures.md)

