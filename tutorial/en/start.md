# Dragonfly Tutorial in English

English | [Español](../es/start.md)

## Getting started

Dragonfly is an engine for developing interactive text games, also known as Interactive Fiction or Text Adventures. These are games composed entirely of text (sometimes including images and sounds) where the player interacts with the story by modifying their environment.

## The book

### Running the game:

Once you have the necessary files prepared as explained in the main README, you can run index.html in a browser using a local server. There are several ways to get your game up and running; here are two of the most popular:

* Using Visual Studio Code: After installing the Live Server extension, right-click on index.html and select "Open with Live Server". Your default browser will automatically launch with your game active.

* Using the Python 3 Server: If you have Python 3 installed, navigate to your game's directory in your terminal and execute: `python3 -m http.server`

If all goes well, you will have the following result:

![Game sample 1](../../media/sample2.png)

### The first DFML file (The player, his place and some things more):

After changing the title and the author of the book, the next step is to tell Dragonfly who the player is and where they are located. In the process, we can include the English dictionary so we don't have to manually define the verbs, articles, and other elements for our game.

```
book(title: "Dragonfly Tutorial", author: "Jhon Doe") {

   # The player:
   property(name: "player", value: "-player")

   # English dictionary (first person):
   include(src: "https://jason80.github.io/dragonfly/templates/dict-en1.dfml")
}

# The objects (nouns) are defined in the dictionary node:
dictionary {
   # Define the garden (place):
   noun(names: "The Garden, garden") {
      describe-place {
         "I am standing in the middle of a colorful garden. While its flowers soak the air with fragrance, the water of a fountain produces a pleasant sound. There is a stone bench in the middle of the path."
      }

      # Define the player inside the garden:
      noun(names: "Vincent, player, -player")
   }
}
```

*Note: You can choose the names you want for all the files: "index.html", "mygame.js" and "mygame.dfml" always keeping the references inside the same files.*

### Explanation "mygame.dfml":

* In the `book` node we set the title and author. Inside the `book` node you can set properties, include dictionaries and other DFML files.
* In this case we set the `player` property with the value "-player".
* We include the english dictionary so we don't have to manually define the verbs, articles, and other elements for our game.

*Note: The dictionary is available at https://jason80.github.io/dragonfly/templates/dict-en1.dfml, but you can download it and use it locally, and make modifications to it. The number 1 indicates that the dictionary is in the first person. If you want the dictionary in the second person, change the 1 to a 2.*

* Inside of the `dictionary` node we define all the elements of the book. In this case, a `noun` (noun or object) as a place: The Garden. And inside the place there will be the noun player.

*Note 1: In Dragonfly all the game objects are nouns (nouns): torch, candle, ... Even the places and even the player.*

*Note 2: The game logic is always focused on the player. "room" contains "player" so this "room" will be the initial place of the game.*

### Explanation "mygame.js":

* We import the Book object from the Dragonfly library.

* We create the book with `new Book()`. The parameter "game-area" will be the `<div>` of our html where the game content will be shown. See the README.md.
The second parameter is the name of the DFML file that contains the game code. In this case "mygame.dfml".

* Run the book with `run()`.

## Mechanics

While the player is in the garden, you can try different actions such as "look", "examine player", "x player", "look at me", or "look at yourself".

These are predefined verbs in the Spanish dictionary. There are many verbs that do not have a specific functional effect but serve to enhance the game's flavor and experience. For example: "jump", "shout", etc.

## Modifying nouns

### Description:

We known that the player is in a place. Every time the player looks, the place description will be shown. To describe the place, the event `describe-place` is used inside the noun that represents the garden.

In Dragonfly `describe-place` will be replaced by the event. It is a way to simplify the writing of events. The native writing of the event would be:

```dfml
after(actions: "LookAround") {
   "Description text"
}
```

Equivalently, `describe-object` will be replaced by the event:

```dfml
after(actions: "ExamineObject") {
   "Description text"
}
```

`"Description text"` is also a shorthand. When Dragonfly finds a standalone piece of text inside an event, it will replace it with a "Print" action response. In other words, the text will be printed on the screen. It must always be enclosed in quotes (single or double):

```dfml
after(actions: "ExamineObject") {
   print("Description text")
}
```

## Adding nouns

We add an apple next to the player, so the structure looks like:

* garden
   * player
   * apple

```
noun(names: "apple, fruit") {
   describe-object {
	  "An red apple. It looks delicious."
   }
}
```

Dragonfly will show everything that the player has around. So you will see this after the place description:

`You can see: a apple.`

Clearly, the engine has no way of knowing that the noun "apple" starts with a vowel sound, so it incorrectly uses the article "a".

### Attributes:

The way to fix this is by adding the `an` attribute to the apple:

```
noun(names: "apple, fruit") {

   set { "an" }	

   describe-object {
	  "An red apple. It looks delicious."
   }
}
```

Now try "take apple", "inventory", or "drop the fruit".

The set key node establishes attributes. Dragonfly has an attribute system that can be applied to nouns to modify their behavior, such as correcting grammar or defining physical properties.

Custom attributes can also be established as flags. Through conditions, the author can make the game behave in one way or another depending on whether or not the noun has a specific custom attribute. For example: 'loose', 'turned-on', 'broken', etc.

Here is a list of the most common ones:

<table>
<tr style="font-weight: bold;">
<td>
Attribute(s)
</td>
<td>
Description
</td>
</tr>

<tr>
<td>
<pre>"an"</pre>
</td>
<td>
Refers to the object using the article "an" instead of "a" (e.g., "an apple").
</td>
</tr>

<tr>
<td>
<pre>"plural"</pre>
</td>
<td>
Identifies the object as plural. (In spanish: "los" or "unas")
</td>
</tr>

<tr>
<td>
<pre>"defined"</pre>
</td>
<td>
Refers to the object as "the" instead of "a/an".
</td>
</tr>

<tr>
<td>
<pre>"countless"</pre>
</td>
<td>
The object becomes uncountable: "You can see: water".
</td>
</tr>

<tr>
<td>
<pre>"proper"</pre>
</td>
<td>
The noun becomes a proper noun. Proper nouns are described differently than common ones: "Dante is here" or "You can see Dante".
</td>
</tr>

<tr>
<td>
<pre>"scene"</pre>
</td>
<td>
Hides the object when the location is described.
</td>
</tr>

<tr>
<td>
<pre>"container"</pre>
</td>
<td>
Conceptually, the object becomes a container. The player can "look inside...", "take from...", etc.
</td>
</tr>

<tr>
<td>
<pre>"closable"</pre>
</td>
<td>
The object can be opened and closed. If it is also a "container", the player cannot look inside or take things from it if it has the "closed" attribute.
</td>
</tr>

<tr>
<td>
<pre>"closed"</pre>
</td>
<td>
Used when the object is "closable" to indicate it is currently closed. The absence of "closed" implies it is open.
</td>
</tr>

<tr>
<td>
<pre>"fixed"</pre>
</td>
<td>
The object is fixed in place; the player cannot "take", "push", or "pull" it.
</td>
</tr>

<tr>
<td>
<pre>"heavy"</pre>
</td>
<td>
The player can "push" and "pull" the object, but cannot carry it because it is too heavy.
</td>
</tr>

</table>

Adding more nouns:
 
```
noun(names: "flowers, flower, perfume, scent") {
   set { "plural" }

   describe-object() {
      "The flowers have vivid colors, and their scent is intoxicating."
   }
}

noun(names: "stone bench, bench, seat, armchair, stone") {
   set { "scene" }

   describe-object() {
      "A stone bench with an ancient design."
   }
}
```

... resulting in the following structure:

* garden
   * player
   * apple
   * flawers
   * stone bench

Just as Dragonfly tries to describe the apple, it will do the same with the flowers and the stone bench. This is why you will see the following after the location description:

`I can see: some flowers, a stone bench, and an apple.`

Of course, this isn't ideal because these two nouns are already mentioned in the description itself.

To avoid this, set the `scene` attribute to both objects so that they "belong to the scene," and Dragonfly will not describe them.

#### Limiting things a bit:

Try `"take the bench"` or `"get the bench"`.

To fix this quickly, set the "fixed" attribute to the bench. We could also have done it with "heavy". The difference is that with "fixed", the player will not be able to push or pull the bench. On the other hand, with "heavy", the player will be able to push and pull the bench but won't be able to take it.

#### Some of events:

In this case, the player is not intended to be able to `"take the flowers"`, so we are going to `cancel` the action as follows:

```dfml
noun(names: "flowers, flower, perfume, scent, garden") {
   set { "plural" }

   describe-object() {
      "The flowers have vivid colors, and their scent is intoxicating."
   }

   before(actions: "TakeObject", cancel: true) {
       "I must confess that I am allergic to flowers."
   }
}
```

When you try to `"eat the apple"`, you will see that nothing happens. This is because the verb "eat" doesn't have a specific built-in effect in the game. To fix this, we are going to write an event for the "eat" verb by capturing the "EatObject" action:

```dfml
before(actions: "EatObject", cancel: true) {
   "The apple tastes very good."
}
```

### Inventory

In Dragonfly, all nouns that are inside the player are considered part of the inventory. You can check your inventory with: `"inventory"`, `"inv"`, or `"i"`.

The **Nouns** section will further explain the topic of containers.

---

[Movement >>>](movement.md)
