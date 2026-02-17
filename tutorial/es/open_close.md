## Abrir y Cerrar

[English](../en/open_close.md "Open and Close tutorial in English") | Español

En muchos juegos conversacionales, el jugador se encuentra con objetos que pueden ser abiertos o cerrados. Para eso, Dragonfly tiene un sistema de atributos para los objetos.

Supongamos que en nuestro camino hay una caja de madera. Para crearla, escribimos:

```
noun(names: "caja de madera, caja, madera") {

   set { "female" "container" }

   describe-object() {
      "Es una pequeña caja de madera. Tiene una tapa unida con bisagras."
   }

   # Dentro de la caja hay un anillo
   noun(names: "anillo") {
      describe-object() {
         "Es un anillo de oro con una piedra preciosa incrustada."
      }
   }
}
```

La caja de madera es un contenedor:

```
set { "female" "container" }
```

Por lo tanto, él podrá ver las cosas que hay dentro de ella.

`mirar dentro de la caja` o `mirar en la caja` para luego: `sacar el anillo de la caja` o `coge el anillo de la caja`.

Pero, ¿qué pasa si queremos que el jugador tenga que abrir la caja para ver lo que hay dentro?

Dragonfly permite que los objetos sean "cerrables". Para eso, agregamos el atributo `closable` y de paso `closed` para que la caja comience cerrada:

```
set { "female" "container" "closable" "closed" }
```

Ahora, el jugador no podrá ver lo que hay dentro de la caja a menos que la abra. Para eso, deberá usar el comando `abrir la caja` o `abre la caja`. Y para cerrarla: `cerrar la caja` o `cierra la caja`.

No necesariamente un objeto debe ser un contenedor para ser "cerrable". Por ejemplo, una puerta puede ser cerrada pero no contener nada.

[<<< Movimiento](movement.md) | [Verbos y Acciones >>>](verbs_actions.md)
