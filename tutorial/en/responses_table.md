# Responses Table

English | [Español](../es/responses_table.md)

Responses go inside blocks such as events (before/after), conditions, and sequences. It's simpler to use the following nomenclature:

```
append-name(name: "new name")
```

Internally, responses are JavaScript classes that derive from ActionResponse, and Dragonfly will replace the previous example with the native response node:"

```
response(class: "AppendName", name: "new name")
```

In the following table, response names will be shown using the first nomenclature:

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Parameters</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>cancel-event</code></td>
            <td>Cancels the execution of the current event.</td>
            <td>None</td>
        </tr>
        <tr>
            <td><code>resume-event</code></td>
            <td>Resumes the execution of the current event.</td>
            <td>None</td>
        </tr>
        <tr>
            <td><code>break</code></td>
            <td>Breaks the execution of a block.</td>
            <td>None</td>
        </tr>
        <tr>
            <td><code>print</code></td>
            <td>Prints text to the output. The style uses CSS.</td>
            <td><code>message</code> (string), <code>style</code> (optional)</td>
        </tr>
        <tr>
            <td><code>append</code></td>
            <td>Appends text to the current output.</td>
            <td><code>message</code> (string), <code>style</code> (optional)</td>
        </tr>
        <tr>
            <td><code>attr</code></td>
            <td>Adds or removes attributes from an object.</td>
            <td><code>instance</code>, <code>set</code> (optional), <code>unset</code> (optional)</td>
        </tr>
        <tr>
            <td><code>variable</code></td>
            <td>Assigns a value to a variable of an object.</td>
            <td><code>instance</code>, <code>variable</code>, <code>set</code></td>
        </tr>
        <tr>
            <td><code>append-name</code></td>
            <td>Adds a name to an object at the front (makes it primary). If the name already exists, it does nothing.</td>
            <td><code>instance</code>, <code>name</code></td>
        </tr>
        <tr>
            <td><code>move</code></td>
            <td>Moves an object inside another (changes its container).</td>
            <td><code>instance</code>, <code>destiny</code></td>
        </tr>
        <tr>
            <td><code>root</code></td>
            <td>Moves an object to the root (without a container).</td>
            <td><code>instance</code></td>
        </tr>
        <tr>
            <td><code>tip</code></td>
            <td>Shows a help message or hint.</td>
            <td><code>message</code> (string), <code>once</code> (boolean, optional)</td>
        </tr>
        <tr>
            <td><code>execute</code></td>
            <td>Executes a game sentence just like the player would.</td>
            <td><code>sentence</code> (string)</td>
        </tr>
        <tr>
            <td><code>add-connection</code></td>
            <td>Adds a connection (exit) to an object.</td>
            <td><code>instance</code>, <code>exit</code>, <code>destiny</code></td>
        </tr>
        <tr>
            <td><code>remove-connection</code></td>
            <td>Removes a connection from an object.</td>
            <td><code>instance</code>, <code>exit</code></td>
        </tr>
        <tr>
            <td><code>show-title</code></td>
            <td>Shows the game title.</td>
            <td>None</td>
        </tr>
        <tr>
            <td><code>run-conversation</code></td>
            <td>Runs a conversation associated with a speaking object.</td>
            <td><code>owner</code></td>
        </tr>
        <tr>
            <td><code>pause</code></td>
            <td>Pauses execution until a key is pressed.</td>
            <td><code>key</code> (optional, defaults to "Enter")</td>
        </tr>
        <tr>
            <td><code>clear</code></td>
            <td>Clears the output (screen).</td>
            <td>None</td>
        </tr>
        <tr>
            <td><code>restart-game</code></td>
            <td>Restarts the game completely.</td>
            <td>None</td>
        </tr>
        <tr>
            <td><code>call</code></td>
            <td>Calls a procedure defined in the dictionary.</td>
            <td><code>procedure</code></td>
        </tr>
        <tr>
            <td><code>sequence</code></td>
            <td>Executes a sequence of responses cyclically, optionally randomized and with probability.</td>
            <td><code>shuffle</code> (boolean, optional), <code>chance</code> (double, optional)</td>
        </tr>
    </tbody>
</table>
