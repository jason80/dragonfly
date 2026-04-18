# Conditions Table

English | [Español](../es/conditions_table.md)

Conditions are responses that, if fulfilled, execute the responses inside their block:

```
if-contains(container: "player", instance: "magic stone") {
	"Winner !!"
	end_game()
}
```

They derive from ConditionResponse, which in turn derives from ActionResponse. So their equivalent is:

```
response(class: "IfContains", container: "player", instance: "magic stone") {
	response(class: "Print") { "Winner !!!" }
	response(class: "EndGame")
}
```

---

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
            <td><code>if-is-set</code></td>
            <td>If the attribute is present in the instance.</description>
            <td><code>instance</code>, <code>attr</code></parameters>
        </tr>
        <tr>
            <td><code>if-is-not-set</code></name>
            <td>If the attribute is NOT present in the instance.</description>
            <td><code>instance</code>, <code>attr</code></parameters>
        </tr>
        <tr>
            <td><code>if-direct-equals-exit</code></name>
            <td>If the parser's direct object matches the specified exit.</description>
            <td><code>exit</code></parameters>
        </tr>
        <tr>
            <td><code>if-contains</code></name>
            <td>If the container contains the specified instance.</description>
            <td><code>container</code>, <code>instance</code></parameters>
        </tr>
        <tr>
            <td><code>if-not-contains</code></name>
            <td>If the container does NOT contain the specified instance.</description>
            <td><code>container</code>, <code>instance</code></parameters>
        </tr>
        <tr>
            <td><code>if-current-place-contains</code></name>
            <td>If the current place (player's container) contains the instance.</description>
            <td><code>instance</code></parameters>
        </tr>
        <tr>
            <td><code>if-current-place-not-contains</code></name>
            <td>If the current place does NOT contain the instance.</description>
            <td><code>instance</code></parameters>
        </tr>
        <tr>
            <td><code>if-direct-equals</code></name>
            <td>If the parser's direct object responds to the instance name.</description>
            <td><code>instance</code></parameters>
        </tr>
        <tr>
            <td><code>if-direct-not-equals</code></name>
            <td>If the parser's direct object does NOT respond to the instance name (or there is no direct object).</description>
            <td><code>instance</code></parameters>
        </tr>
        <tr>
            <td><code>if-indirect-equals</code></name>
            <td>If the parser's indirect object responds to the instance name.</description>
            <td><code>instance</code></parameters>
        </tr>
        <tr>
            <td><code>if-indirect-not-equals</code></name>
            <td>If the parser's indirect object does NOT respond to the instance name (or there is no indirect object).</description>
            <td><code>instance</code></parameters>
        </tr>
        <tr>
            <td><code>if-variable-equals</code></name>
            <td>If the instance's variable has the specified value.</description>
            <td><code>instance</code>, <code>variable</code>, <code>value</code></parameters>
        </tr>
        <tr>
            <td><code>if-connection-exists</code></name>
            <td>If the connection (exit) exists in the instance.</description>
            <td><code>instance</code>, <code>exit</code></parameters>
        </tr>
        <tr>
            <td><code>if-connection-not-exists</code></name>
            <td>If the connection (exit) does NOT exist in the instance.</description>
            <td><code>instance</code>, <code>exit</code></parameters>
        </tr>
        <tr>
            <td><code>if-action-equals</code></name>
            <td>If the current action matches the specified name.</description>
            <td><code>action</code></parameters>
        </tr>
    </tbody>
</table>
