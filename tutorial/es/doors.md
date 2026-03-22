# Puertas

Las puertas son objetos que se pueden abrir y cerrar. El mecanismo consiste en que el jugador no pueda pasar por una salida si la puerta está cerrada. No hace falta incluir ninguna librería para poder crear puertas.

### El Problema

En Dragonfly no puede haber un sustantivo dentro de dos contenedores a la vez:
¿Cómo es posible crear una puerta? Ya que una puerta es un objeto que es compartido
por dos habitaciones.

### La Solución

La solución consiste en crear dos puertas, una en cada habitación. Luego, sincronizar las aperturas de las mismas. El jugador pensará que es una sola pero depende en qué habitación se encuentra verá una puerta o la otra.

Primero definimos las habitaciones con las dos puertas. Una puerta es la copia exacta de otra, solo se agregan nombres distintos para poder identificarlas más adelante:

```dfml
noun(names: "El Comedor, comedor") {
   describe-place() {
      "Una mesa rodeada de sillas ocupa toda la habitación. Platos y cubiertos están dispuestos de forma equilibrada. Al norte hay una puerta."
   }

   noun(names: "player")

   noun(names: "puerta, p-comedor-cocina") {
      set { "female" "fixed" "scene" "closable" "closed" }

      describe-object() {
         "Una puerta de madera y picaporte de metal."
      }
   }

   connection(exit: "norte", destiny: "cocina")
}

noun(names: "La Cocina, cocina") {
   describe-place() {
      "Mesadas y estantes llenos de frascos de conservas. Se pueden ver dos hornos enormes a un costado. Por el sur se vuelve al comedor."
   }

   noun(names: "puerta, p-cocina-comedor") {
      set { "female" "fixed" "scene" "closable" "closed" }

      describe-object() {
         "Una puerta de madera y picaporte de metal."
      }
   }

   connection(exit: "sur", destiny: "comedor")
}
```

Ahora solo queda:

* **Sincronizar las puertas**: Cuando se abra una se cierre la otra y viceversa.

* **Bloquear el paso del jugador**: Cuando las puertas estén cerradas, el jugador no puede avanzar dependiendo de la salida.

### Sincronizar las puertas

Modificando el evento abrir y cerrar de una puerta se abre o cierra la otra:

```dfml
noun(names: "puerta, p-comedor-cocina") {
   set { "female" "fixed" "scene" "closable" "closed" }

   describe-object() {
      "Una puerta de madera y picaporte de metal."
   }

   // Al abrir esta puerta se abre la otra
   after(actions: "OpenObject", cancel: false) {
      attr(instance: "p-cocina-comedor", unset: "closed")
   }

   // Al cerrar esta puerta se cierra la otra
   after(actions: "CloseObject", cancel: false) {
      attr(instance: "p-cocina-comedor", set: "closed")
   }
}
```

```dfml
noun(names: "puerta, p-cocina-comedor") {
   set { "female" "fixed" "scene" "closable" "closed" }

   describe-object() {
      "Una puerta de madera y picaporte de metal."
   }

   // Al abrir esta puerta se abre la otra
   after(actions: "OpenObject", cancel: false) {
      attr(instance: "p-comedor-cocina", unset: "closed")
   }

   // Al cerrar esta puerta se cierra la otra
   after(actions: "CloseObject", cancel: false) {
      attr(instance: "p-comedor-cocina", set: "closed")
   }
}
```

### Bloquear el paso del jugador

Modificando el evento `GoTo` del lugar actual se bloquea el paso si las puertas están cerradas:

```dfml
noun(names: "El Comedor, comedor") {

   // ...

   // Si la salida es "norte" y la puerta está cerrada se bloquea el paso.
   before(actions: "GoTo", cancel: true) {
      if-direct-equals-exit(exit: "norte")
      if-is-set(instance: "p-comedor-cocina", attr: "closed")

      "La puerta está cerrada."
   }
}
```

```dfml
noun(names: "La Cocina, cocina") {

   // ...

   // Si la salida es "sur" y la puerta está cerrada se bloquea el paso.
   before(actions: "GoTo", cancel: true) {
      if-direct-equals-exit(exit: "sur")
      if-is-set(instance: "p-cocina-comedor", attr: "closed")

      "La puerta está cerrada."
   }
}
```
