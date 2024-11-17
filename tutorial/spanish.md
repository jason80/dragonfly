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

## Añadiendo sustantivos

Vamos a añadir una linterna a la escena, simplemente de la siguiente forma:

```
dictionary {
   noun(names: "En Una Habitación, habitacion") {
      describe-place {
         "En la habitación puedo ver una cama y una mesita de luz."
      }

      noun(names: "jugador") {
         describe-object {
            "¡Hola! Soy el jugador. No soy bueno resolviendo acertijos, por ello me tendrás que ayudar."
            "Dime lo que tengo que hacer y ¡presiona enter!."
         }
      }

      noun(names: "linterna, luz") {
         describe-object {
            "Una antigua linterna de lata con un enorme foco."
         }
      }
   }
}
```

Dragonfly intentará describir todo lo que el jugador tiene alrededor. Por eso verás esto después de la descripción del lugar:

`Puedo ver: un linterna.`

Claramente el motor no tiene forma de identificar el género del sustantivo linterna.

### Attributos:

La forma de corregir esto es añadiendo el atributo `female` a linterna:

```
noun(names: "linterna, luz") {

   set { "female" }

   describe-object {
      "Una antigua linterna de lata con un enorme foco."
   }
}
```

Ahora prueba "recoger linterna", "inventario", "dejar la linterna".

`set` admite varios atributos y se usa de ésta forma: `set { "female" "plural" "scene" }`

Algunos atributos pueden modificar el comportamiento del sustantivo. Aquí hay una lista de los mas usuales:

<table>
<tr style="font-weight: bold;">
   <td>
Attributo(s)
   </td>
   <td>
Descripcion
   </td>
</tr>

<tr>
   <td>
<pre>"female"</pre>
   </td>
   <td>
Se refiere al objeto como "la" o "una"
   </td>
</tr>

<tr>
   <td>
<pre>"plural"</pre>
   </td>
   <td>
Se refiere al objeto como "los" o "unos"
   </td>
</tr>

<tr>
   <td>
<pre>"female" "plural"</pre>
   </td>
   <td>
Se refiere al objeto como "las" o "unas"
   </td>
</tr>

<tr>
   <td>
<pre>"definited"</pre>
   </td>
   <td>
Suele referirse al objeto como "el" en vez de "un".
   </td>
</tr>

<tr>
   <td>
<pre>"countless"</pre>
   </td>
   <td>
El objeto se vuelve incontable: "Puedes ver: agua".
   </td>
</tr>

<tr>
   <td>
<pre>"propper"</pre>
   </td>
   <td>
El sustantivo se vuelve propio. Los sustantivos propios se describen aparte de los comunes: "Dante está aqui" o "Puedes ver a Dante".
   </td>
</tr>

<tr>
   <td>
<pre>"scene"</pre>
   </td>
   <td>
Ocultará el objeto cuando se describa el lugar.
   </td>
</tr>

<tr>
   <td>
<pre>"container"</pre>
   </td>
   <td>
Conceptualmente, el objeto se vuelve contenedor. El jugador podrá "mirar dentro ..." "sacar de ..."
   </td>
</tr>

<tr>
   <td>
<pre>"closable"</pre>
   </td>
   <td>
El objeto se podrá cerrar y abrir. En el caso de que sea "container", el jugador no podrá mirar dentro o sacar cosas dentro de él.
   </td>
</tr>

<tr>
   <td>
<pre>"closed"</pre>
   </td>
   <td>
Se utiliza cuando el objeto es "closable" e indica que está cerrado. La ausencia de "closed" indica que está abierto.
   </td>
</tr>

<tr>
   <td>
<pre>"fixed"</pre>
   </td>
   <td>
El objeto estára fijo en el lugar y el jugador no podrá "recoger el objeto", "empujar" ni "tirar de".
   </td>
</tr>

<tr>
   <td>
<pre>"heavy"</pre>
   </td>
   <td>
El jugador podrá "empujar" y "tirar del" objeto. Pero no podrá llevárselo porque es muy pesado.
   </td>
</tr>

</table>

Agregemos los objetos que faltan:  
 
```
noun(names: "cama, litera, camastro, colchon, muebles, mueble") {
   set { "female" }
   
   describe-object {
      "La cama es de una plaza y ocupa casi toda la habitación."
   }
}

noun(names: "mesita de luz, mesita, muebles, mueble") {
   set { "female" }
   
   describe-object {
      "En el pasado era el lugar de una lámpara de noche."
   }
}
```

Así como Dragonfly intenta describir la linterna, lo hará con la cama y la mesita de luz:  
  
`Puedo ver: una cama, una mesita de luz y una linterna.`

Claro que no está bueno porque en la descripción ya se hace mención de estos dos sustantivos.

Para evitar esto, establece el atributo "scene" a ambos objetos para que "pertenezcan a la escena" y Dragonfly no los describa.

#### Limitando un poco las cosas:

Prueba "recoger la cama" y "recoger la mesita".

Para solucionar esto rápidamente establece el atributo "fixed" a la mesita de luz y "heavy" a la cama. Prueba "recoger", "empujar", "jalar" para ver los resultados.
