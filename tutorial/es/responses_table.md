# Tabla de Respuestas

[English](../en/responses_table.md) | Español

Las respuestas van dentro de bloques como eventos (before/after), condiciones y secuencias. Es mas sencillo utilizar la nomenclatura:

```
append-name(name: "nuevo nombre")
```

Internamente las respuestas son clases de javascript que derivan de `ActionResponse` y Dragonfly reemplazará el ejemplo anterior con el nodo nativo `response`:

```
response(class: "AppendName", name: "nuevo nombre")
```

En la siguiente tabla, se mostrarán los nombres de las respuestas con la primer nomenclatura:

<table>
    <thead>
        <tr>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Parámetros</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><code>cancel-event</code></td><td>Cancela la ejecución del evento actual.</td><td>Ninguno</td></tr>
        <tr><td><code>resume-event</code></td><td>Reanuda la ejecución del evento actual.</td><td>Ninguno</td></tr>
        <tr><td><code>break</code></td><td>Rompe la ejecución de un bloque.</td><td>Ninguno</td></tr>
        <tr><td><code>print</code></td><td>Imprime texto en la salida. El estilo es en css.</td><td><code>message</code> (string), <code>style</code> (opcional)</td></tr>
        <tr><td><code>append</code></td><td>Agrega texto al final de la salida actual.</td><td><code>message</code> (string), <code>style</code> (opcional)</td></tr>
        <tr><td><code>attr</code></td><td>Agrega o elimina atributos de un objeto.</td><td><code>instance</code>, <code>set</code> (opcional), <code>unset</code> (opcional)</td></tr>
        <tr>
            <td><code>variable-set</code></td>
            <td>Asigna un valor a una variable de un objeto.</td>
            <td><code>instance</code>, <code>name</code>, <code>value</code></td>
        </tr>
        <tr>
            <td><code>variable-add</code></td>
            <td>Suma un valor a una variable de un objeto.</td>
            <td><code>instance</code>, <code>name</code>, <code>value</code>(opcional: valor por defecto: "1")</td>
        </tr>
        <tr>
            <td><code>variable-sub</code></td>
            <td>Resta un valor a una variable de un objeto.</td>
            <td><code>instance</code>, <code>name</code>, <code>value</code>(opcional: valor por defecto: "1")</td>
        </tr>
        <tr><td><code>append-name</code></td><td>Agrega un nombre a un objeto adelante (lo vuelve principal). Si el nombre ya existe, no hace nada.</td><td><code>instance</code>, <code>name</code></td></tr>
        <tr><td><code>move</code></td><td>Mueve un objeto dentro de otra (cambia su contenedor).</td><td><code>instance</code>, <code>destiny</code></td></tr>
        <tr><td><code>root</code></td><td>Mueve un objeto a la raíz (sin contenedor).</td><td><code>instance</code></td></tr>
        <tr><td><code>tip</code></td><td>Muestra un mensaje de ayuda o sugerencia.</td><td><code>message</code> (string), <code>once</code> (booleano, opcional)</td></tr>
        <tr><td><code>execute</code></td><td>Ejecuta una oración de juego como lo hace el jugador.</td><td><code>sentence</code> (string)</td></tr>
        <tr><td><code>add-connection</code></td><td>Agrega una conexión (salida) a un objeto.</td><td><code>instance</code>, <code>exit</code>, <code>destiny</code></td></tr>
        <tr><td><code>remove-connection</code></td><td>Elimina una conexión de un objeto.</td><td><code>instance</code>, <code>exit</code></td></tr>
        <tr><td><code>show-title</code></td><td>Muestra el título del juego.</td><td>Ninguno</td></tr>
        <tr><td><code>run-conversation</code></td><td>Ejecuta una conversación asociada a un objeto parlante.</td><td><code>owner</code></td></tr>
        <tr><td><code>pause</code></td><td>Pausa la ejecución hasta que se presione una tecla.</td><td><code>key</code> (opcional, por defecto "Enter")</td></tr>
        <tr><td><code>clear</code></td><td>Limpia la salida (pantalla).</td><td>Ninguno</td></tr>
        <tr><td><code>restart-game</code></td><td>Reinicia el juego por completo.</td><td>Ninguno</td></tr>
        <tr><td><code>call</code></td><td>Llama a un procedimiento definido en el diccionario.</td><td><code>procedure</code></td></tr>
        <tr><td><code>sequence</code></td><td>Ejecuta una secuencia de respuestas de forma cíclica, opcionalmente aleatorizada y con probabilidad.</td><td><code>shuffle</code> (booleano, opcional), <code>chance</code> (double, opcional)</td></tr>
    </tbody>
</table>
