# Tutorial de Dragonfly en español

## Comenzando

Dragonfly es un motor para el desarrollo de juegos de texto interactivo o, conocidos también como Aventuras Conversacionales. Son juegos que se componen en su totalidad de texto (a veces imágenes y sonidos) y en ellos, el jugador podrá interactuar con la historia modificando su entorno.

## El libro

### Corriendo el juego:

Teniendo preparados los archivos necesarios como se explica en el README principal, podrás correr el index.html en un navegador mediante un Live Server. Existen múltiples maneras, aqui van dos:

* Utilizando Visual Studio Code: luego de instalar el pluggin Live Server, le haces click secundario a index.html y eliges: "Open with Live Server". Se abrirá tu navegador predeterminado con tu juego corriendo.
* Con el servidor de Python 3: Teniendo instalado Python 3, navega con un terminal (o shell) hasta el directorio de tu juego y ejecuta: `python3 -m http.server`

Si todo va bién, habrás obtenido el mesaje de error:

*[Dragonfly Error] the book title has not been defined*

Eso se debe a que falta "añadir" partes al libro. Como el título y el autor.

### Primer archivo DFML (El jugador, su lugar y algunas cosas mas):

Crea el archivo "book.dfml" y escribe lo siguiente:
```
book(
   title: "Tutorial de Dragonfly",
   author: "Juan Pérez"
)

dictionary {
   noun(names: "En Una Habitación, habitacion") {
      noun(names: "jugador")
   }
}
```

Luego, modifica "mygame.js" con lo siguiente:
```
import { Book } from "../base/book.js"

window.onload = function() {
   const book = new Book("game-area");

   book.setProperty("player", "jugador");

   book.include("../templates/dict-es.dfml");
   book.include("book.dfml");

   book.run();
}
```

*Nota: puedes elegir los nombres que quieras para todos los archivos: "index.html", "mygame.js" y "book.dfml" siempre y cuando mantengas las referencias dentro de los mismos.*

### Explicación "book.dfml":

* En el nodo `book` se establecen los atributos de título y autor.
* Dentro del nodo `dictionary` se declaran todos los elmentos del libro. En éste caso, un `noun` (sustantivo u objeto) que será el lugar inicial: Una habitación. Y dentro de la habitación estará el sustantivo jugador.

*Nota: En Dragonfly todos los objetos del juego son sustantivos (nouns). Todos se consideran sustantivos (linterna, caldero, ...) incluso los lugares y hasta el jugador.*

### Explicación "mygame.js":

* Se crea el objeto book con `new Book()`. El parámetro "game-area" será el `<div>`  de nuestro html donde se mostrará el contenido del juego (Consulta el README.md)
* Con `setProperty` se le dirá a Dragonfly que el jugador será el sustantivo "jugador" declarado en book.dfml.

*Nota: El funcionamiento de Dragonfly siempre se centrará en el jugador. "habitacion" contiene a "jugador" por lo tanto dicha "habitacion" será el lugar inicial del juego.*

* Se incluye contenido al diccionario (en éste caso en español) del archivo "dict-es.dfml". De esa manera no tenemos que definir el resto de los elementos del juego (como verbos, artículos, conexiones, etc.).
* Obviamente se incluye nuestro archivo "book.dfml".
* Por último se corre el libro con `run()`.

El resutado de todo esto sería el siguiente (si todo va bien):

---
<h2 style="text-align: center; font-size: 3em;">
Tutorial de Dragonfly
</h2>

<center>
*Juan Pérez*
</center>

**En Una Habitación**

`>`

---

Donde aparece el cursor podrás darle órdenes al jugador como `mirar` o `examinar`, `salta`, `inventario`, etc.

## Modificando Sustantivos

### Descripción:
Ya sabemos que el jugador está adentro de un habitación. Pero quedaría mejor agregar una pequeña descripción cada vez que el jugador `mire` o venga de otro lugar.

```
noun(names: "En Una Habitación, habitacion") {
   describe-place {
      "En la habitación puedo ver una cama y una mesita de luz."
   }
   noun(names: "jugador")
}
```

Actualiza la página del navegador y verás el resultado.

* `describe-place` es un evento que ocurre "después" de "mirar al rededor".

* El texto solitario entre comillas que ejecuta describe-place significa `imprime esto en la pantalla`. Siempre debe estar entre comillas (simples o dobles).

Vamos a describir al jugador:

A diferencia de describir un lugar, describiremos un objeto (Esto se aclara porque "en Dragonfly, lugares y objetos son sustantivos").

```
noun(names: "jugador") {
   describe-object {
      "¡Hola! Soy el jugador. No soy bueno resolviendo acertijos, por ello me tendrás que ayudar."
      "Dime lo que tengo que hacer y ¡presiona enter!."
   }
}
```

Ahora prueba "examinar al jugador", "x jugador", "mirarme" o "mírate".

### Internamente es mas complejo:

`describe-place` y `describe-object` son formas simplificadas del evento nativo `after` se pueden escribir como quieras, las opciones están.

Las siguentes expresiones en dragonfly son equivalentes:

<table>

<tr>
   <td>
      Expresión
   </td>
   <td>
      Equivalente
   </td>
   <td>
      Explicación
   </td>
</tr>

<tr>
   <td>
<pre>
describe-place {
   "Texto de la descripción"
}
</pre>
   </td>
   <td>
<pre>
after(actions: "LookAround") {
   "Texto de la descripción"
}
</pre>
   </td>
   <td>
Dragonfly reemplazará describe-place por el evento "después" de "mirar alrededor".
   </td>
</tr>

<tr>
   <td>
<pre>
describe-object {
   "Texto de la descripción"
}
</pre>
   </td>
   <td>
<pre>
after(actions: "ExamineObject") {
   "Texto de la descripción"
}
</pre>
   </td>
   <td>
describe-object será reemplazado por el evento "después" de "examinar objeto".
   </td>
</tr>

<tr>
   <td>
<pre>
describe-place {
   "Texto de la descripción"
}
</pre>
   </td>
   <td>
<pre>
describe-place {
   response(class: "Print") {
      "Texto de la descripción"
   }
}
</pre>
   </td>
   <td>
El texto solitario dentro de los eventos, Dragonfly los reemplazará por una respuesta de acción "Print".
   </td>
</tr>
</table>
