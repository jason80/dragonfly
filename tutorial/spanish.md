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
      "Una enorme cama ocupa casi todo el lugar, hay una mesita de luz a un lado."
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
         "Una enorme cama ocupa casi todo el lugar, hay una mesita de luz a un lado."
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

Para solucionar esto rápidamente estableciendo el atributo "fixed" a la mesita de luz y "heavy" a la cama. Prueba "recoger", "empujar", "jalar" para ver los resultados.

### Contenedores

En Dragonfly, *todos los sustantivos son contenedores*. Existe una jerarquia en forma de árbol que representa a hijos con un solo padre. *Un objeto no puede estar en dos lugares al mismo tiempo*. Hasta ahora, el ejemplo de éste tutorial viene a estar representado de la siguiente forma:

<ul>
   <li>En Una Habitación,habitacion
      <ul>
         <li>jugador</li>
         <li>cama,litera,camastro,colchon,muebles,mueble</li>
         <li>mesita de luz,mesita,muebles,mueble</li>
         <li>linterna,luz</li>
      </ul>
   </li>
</ul>

Dentro de `habitacion` hay cuatro sustantivos y uno de ellos es el `jugador`. No existen límites para el autor de aventuras al organizar la estructura de los sustantivos: *podemos meter un camión dentro de un alfiler*. Conceptualmete está mal, pero Dragonfly lo permite. Es por eso que el jugador está limitado.

El jugador no podrá "meter/insertar cosas dentro del objeto" si el objeto no tiene establecido el atributo "container". Tampoco podrá "mirar dentro del objeto".

Ahora vamos a hacer que la linterna aparezca dentro de la mesita de lúz. Nuestro modelo quedará:

<ul>
   <li>En Una Habitación,habitacion
      <ul>
         <li>jugador</li>
         <li>cama,litera,camastro,colchon,muebles,mueble</li>
         <li>mesita de luz,mesita,muebles,mueble
            <ul>
               <li>linterna,luz</li>
            </ul>
         </li>
      </ul>
   </li>
</ul>

```
noun(names: "mesita de luz, mesita, muebles, mueble") {
   set { "female" "scene" "fixed" "container" }

   describe-object {
      "En el pasado era el lugar de una lámpara de noche."
   }

   noun(names: "linterna, luz") {
      describe-object {
         "Una antigua linterna de lata con un enorme foco."
      }
   }
}
```

Pruba ahora "mirar en la mesita", "sacar la linterna de la mesita" y "dejar la linterna en la mesita". Cuando sacas algo de adentro de algo, el objeto va a parar al inventario.

### Inventario

En Dragonfly, todos los sustantivos que estén dentro del jugador se consideran parte del inventario. Puedes consultar tu inventario con: "inventario", "inv" o "i".

Ahora la mesita de luz es contenedora. Quedaría mejor dar un indicio al jugador de ésto:

```
noun(names: "mesita de luz, mesita, muebles, mueble") {
   set { "female" "scene" "fixed" "container" }

   describe-object {
      "En el pasado era el lugar de una lámpara de noche."
     "Tiene una puertita debajo." # <-- Agregamos un indicio
   }

   noun(names: "linterna, luz") {
      describe-object {
         "Una antigua linterna de lata con un enorme foco."
      }
   }
}
```
*Nota: en DFML, todo lo que empieza con `#` ó `//` se considera un comentario de una sola línea. Y si empieza con `/*` y termina con `*/` será un comentario de varias líneas.

### Abre y cierra

Podemos hacer que el jugador no pueda manipular lo que esté adentro de la mesita de luz. Agrega "closable" y "closed" a sus atributos y observa que pasa. Prueba "abrir la mesita" y "cerrar la mesita".

Cuando el sustantivo se trata de un "container", los atributos "closable" y "closed" bloquean al usuario cuando intenta manipular el contenido del objeto.

"closable" debe estar para que el jugador pueda "abrir el objeto" y "cerrar el objeto". La ausencia de "closed" se considera como abierto.

*Nota: se pueden utilizar "closable" y "closed" en sustantivos que no son "container". Por ejemplo: puertas y ventanas.*

Cuando abrimos la mesita de luz se nos informa:

*"Abro la mesita de luz"*

Estaría mejor:

*"Abro la puerta de la mesita de luz"*

Nuestro código quedaría asi:

```
noun(names: "mesita de luz, mesita, muebles, mueble") {
   set { "female" "scene" "fixed" "container" "closable" "closed" }

   describe-object {
      "En el pasado era el lugar de una lámpara de noche."
      "Tiene una puertita debajo."
   }

   after(actions: "OpenObject", cancel: true) { "Abro la puerta de la mesita de luz." }

   after(actions: "CloseObject", cancel: true) { "Cierro la puerta de la mesita de luz." }

   noun(names: "linterna, luz") {
      describe-object {
         "Una antigua linterna de lata con un enorme foco."
      }
   }
}
```

La explicación sería: `después` de `Abrir el objeto` cancelar la acción y mostrar el mensaje ...

Consulta la documentación de [Eventos](tutorial/eventos.md) para mas detalles.

## Movimiento

La mayoria de juegos conversacionales no se limitan a una sola estancia. La forma de indicar al jugador que se mueva a través de ellas es con puntos cardinales. Supongamos que al `este` de nuestra habitación se encuentra un pasillo. El pasillo sería otro lugar que tendremos que declarar:

```
   noun(names: "En Un Oscuro Pasillo, pasillo") {
      describe-place() {
         "La oscuridad lo invade todo. No se puede ver nada."
      }
   }
```

Con "ir hacia el este" le diríamos al jugador que se dirija hacia el este. Pero en éste caso no funcionará.

Esto se debe a que, todavía no existe `conexión` entre la habitación y el pasillo.

Agreguemos (dentro de la habitación) la conexión "de la habitación hacia el pasillo":

```
noun(names: "En Una Habitación, habitacion") {
   describe-place {
      "Una enorme cama ocupa casi todo el lugar, hay una mesita de luz a un lado."
   }
   noun(names: "jugador") {
      describe-object {
         "¡Hola! Soy el jugador. No soy bueno resolviendo acertijos, por ello me tendrás que ayudar."
         "Dime lo que tengo que hacer y ¡presiona enter!."
      }
   }

   noun(names: "cama, litera, camastro, colchon, muebles, mueble") {
      set { "female" "scene" "heavy"}

      describe-object {
         "La cama es de una plaza y ocupa casi toda la habitación."
      }
   }

   noun(names: "mesita de luz, mesita, muebles, mueble") {
      set { "female" "scene" "fixed" "container" "closable" "closed" }

      describe-object {
         "En el pasado era el lugar de una lámpara de noche."
         "Tiene una puertita debajo."
      }

      after(actions: "OpenObject", cancel: true) { "Abro la puerta de la mesita de luz." }

      after(actions: "CloseObject", cancel: true) { "Cierro la puerta de la mesita de luz." }

      noun(names: "linterna, luz") {
         describe-object {
               "Una antigua linterna de lata con un enorme foco."
         }
      }
   }

   connection(exit: "este", destiny: "pasillo")
}
```

Y para ir del pasillo a la habitación por el `oeste`:

```
noun(names: "En Un Oscuro Pasillo, pasillo") {
   describe-place() {
      "La oscuridad lo invade todo. No se puede ver nada."
   }

   connection(exit: "oeste", destiny: "habitacion")
}
```

### Las salidas:

Para que las conexiones entre lugares funcionen, deben existir salidas. Todas las salidas posibles vienen en el diccionario "dict-es.dfml". Aquí hay una lista completa:

<ul>

<li>norte, n</li>
<li>sur, s</li>
<li>este, e</li>
<li>oeste, o, w</li>

<li>noreste, ne</li>
<li>noroeste, no, nw</li>
<li>sudeste, sureste, se</li>
<li>sudoeste, suroeste, so, sw</li>

<li>arriba, arr, sube, subir, subi</li>
<li>abajo, aba, baja, bajar</li>
<li>adentro, ad, entra, entrar</li>
<li>afuera, af, sal, salir, sali</li>

</ul>

La sintaxis para moverse suele ser "ir/ve hacia/al `<salida>`". También puedes escribir el nobre de la salida unicamente, por ejemplo "norte" ó "n". Dragonfly comprobará si es una salida posible y, en el caso de que lo sea, ejecutará la acción "ir hacia" del caso anterior.

Claro que si en nuestra habitación intentamos "ir hacia el sur". El resultado será:

*No puedo ir por ahí.*

Ya que en la habitación no existe la conexión cuya salida es "sur".
