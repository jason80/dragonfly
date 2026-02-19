## Sustantivos

[English](../en/nouns.md "Nouns tutorial in English") | Español

Como se ha dicho antes, los sustantivos son los objetos del juego. Es un tipo de deriva de `Entity` y tiene la propiedad de ser `multiname`, es decir, puede tener varios nombres.

Es recomendable que el desarrollador agregue un nombre interno para determinados sustantivos, pueden incluir guión medio, por ejemplo (el parser quita los guiones medios al analizar la entrada del jugador):

```dfml
noun(names: "Entrada Principal, -entrada-castillo") {
   describe-place() {
      "Es la entrada principal del castillo. Tiene una gran puerta de madera con herrajes de hierro."
   }
}
```

---

Dragonfly se da cuenta cuando dos objetos o mas tienen el mismo nombre, y en ese caso, preguntará al jugador a cuál de ellos se refiere. Por ejemplo:

```dfml
noun(names: "bola roja, bola") {
   set { "female" }
   describe-object() {
      "Es una bola roja brillante."
   }
}

noun(names: "bola azúl, bola") {
   set { "female" }
   describe-object() {
      "Es una bola azúl brillante."
   }
}

```

Las bolas están en el mismo lugar. Cuando el jugador intente `recoger la bola` o `mirar la bola`, el parser le preguntará a cuál de las bolas se refiere.

---

Otra característica de `multiname` lo poco estricto que es a la hora de referirnos a un objeto.

Si tenemos un objeto que se llama `ñandú`, el jugador puede referirse a él como `ñandu`, `ñandú`, `nandu`, `nándu`, etc. La entidad en sí se da cuenta de que todas esas formas se refieren a sí mismo.

Esto hace que el jugador no tenga que preocuparse por escribir exactamente el nombre del objeto, lo que mejora la experiencia de juego.

## Contenedores

En Dragonfly, *todos los sustantivos son contenedores*. Existe una jerarquia en forma de árbol que representa a hijos con un solo padre. *Un objeto no puede estar en dos lugares al mismo tiempo*. Hasta ahora, el ejemplo del jardín viene a estar representado de la siguiente forma:

Dentro de `jardin` hay cuatro sustantivos y uno de ellos es el `jugador`. No existen límites para el autor de aventuras al organizar la estructura de los sustantivos: *podemos meter un camión dentro de un alfiler*. Conceptualmete está mal, pero Dragonfly lo permite. Es por eso que el jugador está limitado.

El jugador no podrá `"meter/insertar cosas dentro del objeto"` si el objeto no tiene establecido el atributo `"container"`. Tampoco podrá `"mirar dentro del objeto"`.

Podemos crear una fuente de agua dentro del jardín. Y dentro de la fuente, una llave. Para esto, agregamos el siguiente código:

```
noun(names: "fuente de agua, fuente, agua") {
   set { "female" "fixed" "scene" "container" }

   describe-object {
      "Una fuente de agua proyecta chorros de agua produciendo un sonido relajante."
   }

   noun(names: "llave, llave antigua") {
      describe-object {
         "Una antigua llave de bronce."
      }
   }

}
```

Prueba ahora `"mirar en la fuente"`, `"sacar la llave de la fuente"` y `"dejar la llave en la fuente"`. Cuando sacas algo de adentro de algo, el objeto va a parar al inventario.

## Vida de Los Sustantivos

Los sustantivos se crean al arrancar el juego y permanecen hasta que termina. *No se crean ni se destruyen sustantivos mientras el juego transcurre*.

Para hacer aparecer un nuevo sustantivo, el desarrollador debe mover el objeto desde un lugar especial, un lugar del que el jugador ni sospeche. Lo mismo para destruirlo, se lo mueve a ese lugar.

Una práctica recomendada es crear un lugar especial inaccesible para el jugador y metemos y sacamos los objetos de allí.

## Persistencia

Escribe `save`, `salvar` o `guardar` para guardar la partida. Dragonfly se encarga de guardar la partida sin que el desarrollador tenga que preocuparse.

Escribe `load`, `cargar` o `recuperar` para recuperar la partida.

#### ¿Dónde se guarda?

Dragonfly guarda la partida en el navegador. No se pierde si se cierra el navegador, se reinicia o se refresca.

La única forma de perder la partida es limpiar los datos de navegador.

#### ¿Cómo se guarda?

Se guarda en el Local Storage del navegador y solo se guarda información de los sustantivos *que puede variar durante la partida*:

* El `identificador` (id): es un valor numérico único para cada sustantivo. *Solo sirve para el sistema de guardado*.
* Los nombres.
* El `id` del contenedor padre: si el objeto está en la `raíz`, el id es 0 (cero).
* Los atributos.
* Las variables.
* Las conexiones.

*Nota: Las partidas guardadas desactualizadas pueden traer problemas. A medida que el desarrollador crea nuevos objetos en el juego, es una buena práctica renovar las partidas guardadas con `save`.*

#### El Estado Inicial En Memoria

El estado inicial de la partida se guarda en la memoria cuando arranca el juego. Esto se utiliza para `reiniciar` la partida cuando se finaliza el juego (game over). Se hace llamando a la respuesta `restart-game()`, se restaura el estado inicial de la partida.

[<<< Abrir y Cerrar](open_close.md) | [Verbos y Acciones >>>](verbs_actions.md)
