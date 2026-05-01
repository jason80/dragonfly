# Dragonfly Actions Table

English | [Español](../es/actions_table.md)

This table contains all the actions available in Dragonfly to define verbs.

All the actions send events to the player and the place where it is (in that order), both `before` and `after` and to the objects directly and indirectly involved.

---

## Specific Actions:

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
      <th>Responses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>UnknownVerb</strong></td>
      <td>Executed when the engine does not recognize the entered command. Triggers player and room events before emitting the error response.</td>
      <td>unknown-verb</td>
    </tr>
    <tr>
      <td><strong>Clear</strong></td>
      <td>Completely clears the console or text output area using the <code>Output.clear()</code> method.</td>
      <td>(None)</td>
    </tr>
    <tr>
      <td><strong>SaveGame</strong></td>
      <td>Uses the persistence system to save the current state of the dictionary in the browser's <code>localStorage</code>, using the book title as the key.</td>
      <td>game-saved</td>
    </tr>
    <tr>
      <td><strong>LoadGame</strong></td>
      <td>Retrieves saved data from <code>localStorage</code> and restores it into the current dictionary to resume a previous game.</td>
      <td>game-loaded</td>
    </tr>
    <tr>
      <td><strong>Inventory</strong></td>
      <td>Lists the items the player is carrying. If the inventory is empty, it triggers a response; otherwise, it executes the dictionary's visual inventory dialog.</td>
      <td>inventory-is-empty</td>
    </tr>
    <tr>
      <td><strong>ExamineObject</strong></td>
      <td>Searches for the object in the inventory or the room. If found, marks it as "described" so the engine processes its detailed description.</td>
      <td>direct-not-found</td>
    </tr>
    <tr>
      <td><strong>ExamineMe</strong></td>
      <td>Special action that redirects the flow: looks up the verb associated with "ExamineObject" in the dictionary and automatically executes it on the "player" object.</td>
      <td>(Inherited from ExamineObject)</td>
    </tr>
    <tr>
      <td><strong>LookAround</strong></td>
      <td>Prints the name of the current location and marks it as "described". Then, lists all visible objects that are neither the player nor "scenery" elements.</td>
      <td>(None)</td>
    </tr>
    <tr>
      <td><strong>LookInside</strong></td>
      <td>Verifies that the direct object is an open container and not the player. If requirements are met, it displays the object's contents.</td>
      <td>direct-not-found, direct-is-the-player, direct-is-not-container, direct-is-closed, container-is-empty</td>
    </tr>
    <tr>
      <td><strong>TakeObject</strong></td>
      <td>Attempts to move an object from the room to the inventory. Checks that the object is not the player, is not fixed, and is not heavy. Marks it as "taken".</td>
      <td>direct-not-found, direct-is-the-player, direct-is-fixed, direct-is-heavy, direct-taken</td>
    </tr>
    <tr>
      <td><strong>LeaveObject</strong></td>
      <td>Moves an object from the player's inventory to the current room and marks it with the "leaved" status.</td>
      <td>direct-not-found, first-remove, direct-left</td>
    </tr>
    <tr>
      <td><strong>TakeFrom</strong></td>
      <td>Searches for an object (direct) inside another (indirect). Validates that the container is open and, after control events, moves the object to the inventory.</td>
      <td>indirect-not-found, indirect-is-not-container, indirect-is-closed, direct-not-found, direct-taken</td>
    </tr>
    <tr>
      <td><strong>LeaveIn</strong></td>
      <td>Moves an object from the inventory to a specific container. Validates that the destination is a valid container and is not closed.</td>
      <td>direct-not-found, indirect-not-found, indirect-is-the-player, indirect-is-not-container, indirect-is-closed, first-remove, direct-leaved</td>
    </tr>
    <tr>
      <td><strong>PullObject / PushObject</strong></td>
      <td>Physical interaction that verifies the object is in the room and not fixed. By default, it only triggers a neutral response.</td>
      <td>direct-not-found, direct-is-the-player, direct-is-fixed, nothing-happens</td>
    </tr>
    <tr>
      <td><strong>OpenObject / CloseObject</strong></td>
      <td>Manipulate the "closed" state on objects marked as "closable". Validate if the object is already in the desired state before acting.</td>
      <td>direct-not-found, direct-is-the-player, direct-is-not-closable, direct-is-open/closed, direct-was-opened/closed</td>
    </tr>
    <tr>
      <td><strong>OpenWith / CloseWith</strong></td>
      <td>Versions of opening and closing that require a tool (indirect object) present in the player's inventory to execute.</td>
      <td>direct-not-found, direct-is-the-player, indirect-is-the-player, direct-is-not-closable, direct-is-open, nothing-happens</td>
    </tr>
    <tr>
      <td><strong>GoTo</strong></td>
      <td>Manages movement. Searches for the exit, validates the connection in the current room, and moves the player, potentially triggering an automatic "LookAround".</td>
      <td>exit-not-exists, exit-not-found</td>
    </tr>
    <tr>
      <td><strong>Talk</strong></td>
      <td>Generic speech action that triggers a response indicating the player is emitting a message in the current location.</td>
      <td>player-says</td>
    </tr>
    <tr>
      <td><strong>TalkTo</strong></td>
      <td>Attempts to start a conversation with an object. Requires the target to have the "speaker" attribute set.</td>
      <td>direct-not-found, direct-is-the-player, direct-is-not-speaker, nothing-happens</td>
    </tr>
    <tr>
      <td><strong>GiveTo</strong></td>
      <td>Transfers an item from the inventory to a receiver in the room, provided the latter is marked as "interactive" in its attributes.</td>
      <td>direct-not-found, indirect-not-found, indirect-is-the-player, indirect-is-not-interactive, given-to-indirect</td>
    </tr>
    <tr>
      <td><strong>WearObject</strong></td>
      <td>Allows the player to put on a wearable item. The item goes to the inventory and is marked as "worn".</td>
      <td>direct-not-found, direct-is-the-player, direct-is-not-wearable, direct-is-worn, direct-moved-to-inventory, direct-now-worn</td>
    </tr>
    <tr>
      <td><strong>RemoveObject</strong></td>
      <td>Allows the player to take off a wearable item that is currently being worn. Checks that the direct object has the "worn" attribute set.</td>
      <td>direct-not-found
          direct-is-not-worn
          direct-removed
      </td>
    </tr>
    <tr>
      <td><strong>CutWith / TieWith / BreakWith</strong></td>
      <td>Complex actions requiring a direct object and an indirect tool. They send events to both objects for the game logic to react.</td>
      <td>direct-not-found, direct-is-the-player, indirect-is-the-player, nothing-happens</td>
    </tr>
  </tbody>
</table>

---

## Default actions (Direct object)

Here is the translation into English:

These are actions that expect a direct object as a parameter and do not perform any state changes by default. The object must be either in the current location or in the player's inventory.

They are intended to be intercepted (captured) to perform specific logic.

All default actions have three standard responses: `direct-not-found`, `direct-is-the-player`, `and nothing-happens`.

They can all be shown in a list:

* **ReadObject**
* **SmokeObject**
* **TurnOnObject**
* **TurnOffObject**
* **TurnObject**
* **HitObject**
* **TouchObject**
* **PressObject**
* **BlowObject**
* **CutObject**
* **TieObject**
* **FollowObject**
* **BreakObject**
* **ClimbObject**
* **LoadObject**
* **FillObject**
* **ShootObject**
* **EatObject**
* **HangObject**

---

## Simple actions

These are actions that do not expect any objects as parameters.
These actions have a single default response: `nothing-happens`.

* **Jump**
* **Scream**
* **Cry**
* **Listen**
* **Sleep**
* **Smell**
