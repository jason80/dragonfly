# Tabla de Condiciones

[English](../en/conditions_table.md) | Español

Las condiciones son respuestas que, si se cumple, ejecuta las respuestas dentro de su bloque:

```
if-contains(container: "player", instance: "magic stone") {
	"Has ganado !!"
	end_game()
}
```

Derivan de `ConditionResponse` que a su vez, deriva de `ActionResponse`. Entonces su equivalente es:

```
response(class: "IfContains", container: "player", instance: "magic stone") {
	response(class: "Print") { "Has ganado !!!" }
	response(class: "EndGame")
}
```

---

<table>
    <thead>
        <tr>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Parámetros</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>if-is-set</code></td>
            <td>Si el atributo está presente en la instancia.</td>
            <td><code>instance</code>, <code>attr</code></td>
        </tr>
        <tr>
            <td><code>if-is-not-set</code></td>
            <td>Si el atributo NO está presente en la instancia.</td>
            <td><code>instance</code>, <code>attr</code></td>
        </tr>
        <tr>
            <td><code>if-direct-equals-exit</code></td>
            <td>Si el objeto directo del parser coincide con la salida especificada.</td>
            <td><code>exit</code></td>
        </tr>
        <tr>
            <td><code>if-contains</code></td>
            <td>Si el contenedor contiene la instancia especificada.</td>
            <td><code>container</code>, <code>instance</code></td>
        </tr>
        <tr>
            <td><code>if-not-contains</code></td>
            <td>Si el contenedor NO contiene la instancia especificada.</td>
            <td><code>container</code>, <code>instance</code></td>
        </tr>
        <tr>
            <td><code>if-current-place-contains</code></td>
            <td>Si el lugar actual (contenedor del jugador) contiene la instancia.</td>
            <td><code>instance</code></td>
        </tr>
        <tr>
            <td><code>if-current-place-not-contains</code></td>
            <td>Si el lugar actual NO contiene la instancia.</td>
            <td><code>instance</code></td>
        </tr>
        <tr>
            <td><code>if-direct-equals</code></td>
            <td>Si el objeto directo del parser responde al nombre de instancia.</td>
            <td><code>instance</code></td>
        </tr>
        <tr>
            <td><code>if-direct-not-equals</code></td>
            <td>Si el objeto directo NO responde al nombre de instancia (o no hay objeto directo).</td>
            <td><code>instance</code></td>
        </tr>
        <tr>
            <td><code>if-indirect-equals</code></td>
            <td>Si el objeto indirecto del parser responde al nombre de instancia.</td>
            <td><code>instance</code></td>
        </tr>
        <tr>
            <td><code>if-indirect-not-equals</code></td>
            <td>Si el objeto indirecto NO responde al nombre de instancia (o no hay objeto indirecto).</td>
            <td><code>instance</code></td>
        </tr>
        <tr>
            <td><code>if-variable-equals</code></td>
            <td>Si la variable de la instancia tiene el valor especificado.</td>
            <td><code>instance</code>, <code>name</code>, <code>value</code></td>
        </tr>
        <tr>
            <td><code>if-variable-not-equals</code></td>
            <td>Si la variable de la instancia no tiene el valor especificado.</td>
            <td><code>instance</code>, <code>name</code>, <code>value</code></td>
        </tr>
        <tr>
            <td><code>if-variable-lt</code></td>
            <td>Si la variable de la instancia es menor que el valor especificado.</td>
            <td><code>instance</code>, <code>name</code>, <code>value</code></td>
        </tr>
        <tr>
            <td><code>if-variable-gt</code></td>
            <td>Si la variable de la instancia es mayor que el valor especificado.</td>
            <td><code>instance</code>, <code>name</code>, <code>value</code></td>
        </tr>
        <tr>
            <td><code>if-variable-lte</code></td>
            <td>Si la variable de la instancia es menor o igual que el valor especificado.</td>
            <td><code>instance</code>, <code>name</code>, <code>value</code></td>
        </tr>
        <tr>
            <td><code>if-variable-gte</code></td>
            <td>Si la variable de la instancia es mayor o igual que el valor especificado.</td>
            <td><code>instance</code>, <code>name</code>, <code>value</code></td>
        </tr>
        <tr>
            <td><code>if-connection-exists</code></td>
            <td>Si la conexión (salida) existe en la instancia.</td>
            <td><code>instance</code>, <code>exit</code></td>
        </tr>
        <tr>
            <td><code>if-connection-not-exists</code></td>
            <td>Si la conexión (salida) NO existe en la instancia.</td>
            <td><code>instance</code>, <code>exit</code></td>
        </tr>
        <tr>
            <td><code>if-action-equals</code></td>
            <td>Si la acción actual coincide con el nombre especificado.</td>
            <td><code>action</code></td>
        </tr>
    </tbody>
</table>
