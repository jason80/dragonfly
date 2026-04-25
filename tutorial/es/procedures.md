# Procedimientos

Un procedimiento agrupa respuestas bajo un nombre. Estas respuestas pueden ser ejecutadas con solo llamar al nombre del procedimiento.

Es análogo a una subrutina de los lenguajes tradicionales y sirve para reaprovechar código. Hay una respuesta especial llamada `call` que llama al procedimiento definido.

## Definiendo un procedimiento

Los procedimientos se definen solo en los nodos `dictionary` y `noun`, y son TODOS GLOBALES, es decir, se puede declarar un procedimiento en un sustantivo y llamarlo desde cualquier otro lejano.

Vamos a definir unos procedimientos que determinan el final del un juego:

```dfml
dictionary {
   procedure(name: "final-bueno") {
      print("¡ Has ganado !", style: "color: green; font-weight: bold;")

      "Completaste el juego con exito." pause()

      restart-game() break()
   }

   procedure(name: "final-malo") {
      print("¡ Has perdido !", style: "color: red; font-weight: bold;")

      "La próxima vez será." pause()

      restart-game() break()
   }
}
```

## Llamando a un procedimiento

Los procedimientos se llaman con la respuesta `call`. Por ejemplo:

```dfml
noun(names: "El Final del Túnel, final-tunel) {
   describe-place {
      "Puedo ver luz. La salida está cerca. Solo debo caminar hacia el norte."
   }

   before(actions: "GoTo") {
      if-direct-equals-exit(exit: "norte") {
         call(procedure: "final-bueno")
      }
   }

   connection(exit: "norte", destiny: "exterior")
}
```

Cuando se llama a un procedimiento, se hereda la información del evento: la acción, el objeto directo y el objeto indirecto, el control de flujo, etc. Por lo tanto se pueden llamar a respuestas como `cancel-event`, `resume-event`y `break`.

[<<< El Parser](parser.md) | [Variables >>>](variables.md)
