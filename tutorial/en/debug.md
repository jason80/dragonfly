# Debug

English | [Español](./es/debug.md "Tutorial de depuración")

Dragonfly offers tools for debugging, that is, they allow you to see the parsing process, query the game elements and set variables and attribute values at runtime.

## Dictionary of debugging

Including the dictionary of debugging dict-debug.dfml, you can include the following special verbs:

* **info**: Shows the information of one or more subjects: names, container, attributes, variables and connections. (Usage: `info <subject>`).

* **tree**: Shows all the subjects in form of a tree. (Usage: `tree`). If you pass a subject, shows the tree of that subject. (Usage: `tree <subject>`).

* **attribute, attr**: Adds or removes an attribute to a subject. (Usage: `attr <subject> set/unset <attribute>`).

* **move, mv**: Moves a subject inside another. (Usage: `mv <subject> to <destination>`).

* **root**: Moves a subject to the root of the objects tree. (Usage: `root <subject>`).

* **verb**: Shows information of one or more verbs: names, actions associated, syntax. (Usage: `verb <verb>`).

* **action**: Returns the responses of an action. Useful to create new verbs. (Usage: `action <action>`).  

* **exitlist**: Shows the list of all possible exits. (Usage: `exitlist`).

## The parser

### **show-parsing-process**

You can enable the parser's parsing process with:

```dfml
property(name: "show-parsing-process", value: true)
```

After each entry, the parser shows:

*> x note*

```dfml
Parser: for x, 4 verb(s) found, checking syntax ...
Parser: executing action: "ExamineObject".
Parser: Params 1=note
```

*An ugly note, with a pale tint only legible.*

This feature is very useful to know which action is executed with each verb.

### **parser-clean**

The parser cleans the player's input of characters indesired. But if the developer needs it, it can be disabled, because there are times when the names of the subjects include characters that cannot be, for example, move with `mv` or show the `info`.

To NOT clean the player's input:

```dfml
property(name: "parser-clean", value: "")
```

It allows to debug in the following way:

````dfml
move snake to -inside-cavern
````