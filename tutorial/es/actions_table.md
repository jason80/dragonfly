# Tabla de Acciones de Dragonfly

[English](../en/actions_table.md) | Español

Tabla con todas las acciones disponibles en Dragonfly para definir verbos.

Hay que tener en cuenta que, todas las acciones envian eventos al jugador y al lugar donde se encuentra (en ese orden), tanto `before` como `after` y a los objetos directos e indirectos si entran en juego.

---

## Acciones específicas:

<table>
  <thead>
    <tr>
      <th>Nombre</th>
      <th>Descripción</th>
      <th>Respuestas</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>UnknownVerb</strong></td>
      <td>Se ejecuta cuando el motor no reconoce el comando ingresado. Dispara los eventos del jugador y la habitación antes de emitir la respuesta de error.</td>
      <td>unknown-verb</td>
    </tr>
    <tr>
      <td><strong>Clear</strong></td>
      <td>Limpia por completo la consola o área de salida de texto mediante el método <code>Output.clear()</code>.</td>
      <td>(Ninguna)</td>
    </tr>
    <tr>
      <td><strong>SaveGame</strong></td>
      <td>Utiliza el sistema de persistencia para guardar el estado actual del diccionario en el <code>localStorage</code> del navegador, usando el título del libro como clave.</td>
      <td>game-saved</td>
    </tr>
    <tr>
      <td><strong>LoadGame</strong></td>
      <td>Recupera los datos guardados desde el <code>localStorage</code> y los restaura en el diccionario actual para retomar una partida previa.</td>
      <td>game-loaded</td>
    </tr>
    <tr>
      <td><strong>Inventory</strong></td>
      <td>Lista los objetos que el jugador lleva consigo. Si el inventario está vacío, dispara una respuesta; de lo contrario, ejecuta el diálogo visual de inventario del diccionario.</td>
      <td>inventory-is-empty</td>
    </tr>
    <tr>
      <td><strong>ExamineObject</strong></td>
      <td>Busca el objeto en el inventario o la habitación. Si lo encuentra, lo marca como "described" para que el motor procese su descripción detallada.</td>
      <td>direct-not-found</td>
    </tr>
    <tr>
      <td><strong>ExamineMe</strong></td>
      <td>Acción especial que redirige el flujo: busca el verbo asociado a "ExamineObject" en el diccionario y lo ejecuta automáticamente sobre el objeto "player".</td>
      <td>(Heredadas de ExamineObject)</td>
    </tr>
    <tr>
      <td><strong>LookAround</strong></td>
      <td>Imprime el nombre del lugar actual y lo marca como "descrito". Luego, lista todos los objetos visibles que no sean el jugador ni elementos de "escenario".</td>
      <td>(Ninguna)</td>
    </tr>
    <tr>
      <td><strong>LookInside</strong></td>
      <td>Verifica que el objeto directo sea un contenedor abierto y no sea el propio jugador. Si se cumplen los requisitos, muestra el contenido del objeto.</td>
      <td>direct-not-found, direct-is-the-player, direct-is-not-container, direct-is-closed, container-is-empty</td>
    </tr>
    <tr>
      <td><strong>TakeObject</strong></td>
      <td>Intenta mover un objeto de la habitación al inventario. Comprueba que el objeto no sea el jugador, que no esté fijo y que no sea pesado. Lo marca como "taken".</td>
      <td>direct-not-found, direct-is-the-player, direct-is-fixed, direct-is-heavy, direct-taken</td>
    </tr>
    <tr>
      <td><strong>LeaveObject</strong></td>
      <td>Mueve un objeto del inventario del jugador a la habitación actual y lo marca con el estado "leaved".</td>
      <td>direct-not-found, direct-left</td>
    </tr>
    <tr>
      <td><strong>TakeFrom</strong></td>
      <td>Busca un objeto (directo) dentro de otro (indirecto). Valida que el contenedor esté abierto y, tras los eventos de control, mueve el objeto al inventario.</td>
      <td>indirect-not-found, indirect-is-not-container, indirect-is-closed, direct-not-found, direct-taken</td>
    </tr>
    <tr>
      <td><strong>LeaveIn</strong></td>
      <td>Mueve un objeto del inventario a un contenedor específico. Valida que el destino sea un contenedor válido y que no esté cerrado.</td>
      <td>direct-not-found, indirect-not-found, indirect-is-the-player, indirect-is-not-container, indirect-is-closed, direct-leaved</td>
    </tr>
    <tr>
      <td><strong>PullObject / PushObject</strong></td>
      <td>Interacción física que verifica que el objeto esté en la habitación y no esté fijo. Por defecto, solo dispara una respuesta neutra.</td>
      <td>direct-not-found, direct-is-the-player, direct-is-fixed, nothing-happens</td>
    </tr>
    <tr>
      <td><strong>OpenObject / CloseObject</strong></td>
      <td>Manipulan el estado "closed" en objetos marcados como "closable". Validan si el objeto ya está en el estado deseado antes de actuar.</td>
      <td>direct-not-found, direct-is-the-player, direct-is-not-closable, direct-is-open/closed, direct-was-opened/closed</td>
    </tr>
    <tr>
      <td><strong>OpenWith / CloseWith</strong></td>
      <td>Versiones de apertura y cierre que requieren una herramienta (objeto indirecto) presente en el inventario del jugador para ejecutarse.</td>
      <td>direct-not-found, direct-is-the-player, indirect-is-the-player, direct-is-not-closable, direct-is-open, nothing-happens</td>
    </tr>
    <tr>
      <td><strong>GoTo</strong></td>
      <td>Gestiona el movimiento. Busca la salida, valida la conexión en la habitación actual y traslada al jugador, pudiendo disparar un "LookAround" automático.</td>
      <td>exit-not-exists, exit-not-found</td>
    </tr>
    <tr>
      <td><strong>Talk</strong></td>
      <td>Acción de habla genérica que dispara una respuesta indicando que el jugador emite un mensaje en el lugar actual.</td>
      <td>player-says</td>
    </tr>
    <tr>
      <td><strong>TalkTo</strong></td>
      <td>Intenta iniciar una conversación con un objeto. Requiere que el objetivo tenga el atributo "speaker" establecido.</td>
      <td>direct-not-found, direct-is-the-player, direct-is-not-speaker, nothing-happens</td>
    </tr>
    <tr>
      <td><strong>GiveTo</strong></td>
      <td>Transfiere un objeto del inventario a un receptor en la habitación, siempre que este último esté marcado como "interactive" en sus atributos.</td>
      <td>direct-not-found, indirect-not-found, indirect-is-the-player, indirect-is-not-interactive, given-to-indirect</td>
    </tr>
    <tr>
      <td><strong>CutWith / TieWith / BreakWith</strong></td>
      <td>Acciones complejas que requieren un objeto directo y una herramienta indirecta. Envían eventos a ambos objetos para que la lógica del juego reaccione.</td>
      <td>direct-not-found, direct-is-the-player, indirect-is-the-player, nothing-happens</td>
    </tr>
  </tbody>
</table>

---

## Acciones por defecto (Objeto directo)

Son acciones esperan un objeto directo como parámetro y no realizan cambio alguno. El objeto debe estar en el lugar o en el inventario del jugador.

Sirven para ser capturadas y hacer algo con ellas.

Todas las acciones por defecto tienen tres respuestas: `direct-not-found`, `direct-is-the-player` y `nothing-happens`.

Se pueden mostrar todas en una lista:

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

## Aciones simples

Son acciones que no esperan objetos como parámetros.
Estas acciones tienen una respuesta por defecto: `nothing-happens`:

* **Jump**
* **Scream**
* **Cry**
* **Listen**
* **Sleep**
* **Smell**
