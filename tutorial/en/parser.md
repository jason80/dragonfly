## The Parser

English | [Español](../es/parser.md)

The parser is the component of the game engine that interprets the player's input and translates it into actions within the game.

It decomposes the player's input into its constituent parts, identifies the verb and the objects involved, and then determines what action to take based on the verb and the objects.

---

Next, we will detail in general the steps that the parser follows to process the player's input:

### 1 - Clean characters.

Removes characters:

```
- _ # $ @ & + * ; /
```

These characters do not provide relevant information for the parser and can interfere with the interpretation of the player's input.

*Note: you can configure the parser to ignore specific characters by setting the `book` node:*
*```property(name: "parse-clean", value: "_#$@&+*;/")```*

### 2 - Looks for verbs.
Looks for verbs in the dictionary that match the first word entered by the player. It expects to find one or more verbs that match that word. If it doesn't find any, it goes to step 2A.

#### 2A - Looks for exits.
It searches for exits registered in the dictionary, such as `north`, `south`, `east`, `west`, etc. If it finds an exit that matches the entered word, it implicitly executes the `GoTo` action and sets the found exit as the direct object. The process stops here, and the parser starts again with the input `go to "exit"`. Whether the exit exists or not in the current location will be handled by the `GoTo` action.

If no exit is found that matches the entered word, the parser returns the typical message `"I don't know what you are saying"`. The process stops here.

#### 2B - Verbs found.

If it finds one or more verbs that match the entered word, the parser continues to determine which verb is the most appropriate based on the syntax.

### 3 - Check the syntax.

Each verb declared in the dictionary has an associated syntax, which indicates what type of objects it expects to receive. The parser searches the sentence entered by the player for objects that match that syntax. Sometimes these involve keywords, such as `with`, `to`, `in`, etc. Other times, they simply expect a direct and/or indirect object.

If it fails to match the syntax of any verb found, the parser returns the typical message `"I don't know what you are saying"`. The process stops here.

### 4 - Execute the action.

It executes the action associated with the found verb, passing the identified objects in the syntax as parameters.

*Note: at this point, it is not yet known whether the direct and indirect objects are valid or not; that is handled within the executed action.*

---

## Differences between syntax:

Verbs are declared with the `verb` key node, and each has an associated action and syntax. These are declared in templates/dict-en1.dfml. Since they are `multiname`, there can be several verbs with the same name but different syntaxes. The parser is responsible for identifying the most appropriate verb based on the syntax of the sentence entered by the player. Let's look at four verbs with the same name but different syntaxes:

```
verb(names: "examine, look, see, find, seek, ex, x, l",
      action: "LookInside", syntax: "in/on/inner, 1") {
   response(id: "direct-not-found", string: "I can't find that.")
   response(id: "direct-is-the-player", string: "You can try: inventory or i.")
   response(id: "direct-is-not-container", string: "I can't see inside #1.")
   response(id: "direct-is-closed", string: "#^1 @1(is,is,are,are) closed.")
   response(id: "container-is-empty", string: "There is nothing in #1.")
}

verb(names: "examine, look, see, find, seek, ex, x, l",
      action: "ExamineObject", syntax: "to, 1") {
   response(id: "direct-not-found", string: "There is none of that.")
}

verb(names: "examine, look, see, find, seek, ex, x, l",
      action: "ExamineObject", syntax: "1") {
   response(id: "direct-not-found", string: "There is none of that.")
}

verb(names: "examine, look, see, find, seek, ex, x, l",
      action: "LookAround")
```

### Special cases:

**Multi-parameter verbs:** Cases such as TalkTo involve a sentence after the direct object, which is interpreted as a message to be sent to the character being spoken to. In this case, the parser identifies the verb, looks for a direct object that matches the syntax, and then takes the rest of the sentence as the message to be sent.

[<<< Conditions](conditions.md) | [Procedures >>>](procedures.md)
