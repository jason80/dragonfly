# Oscuridad

[English](../en/darkness.md) | Español

En Dragonfly no existe el concepto de "oscuridad" ni "luz". Nosotros podríamos decir que un lugar está oscuro, pero si el jugador consulta su inventario o examina algún objeto del mismo, no tendría que poder hacerlo.

Frenar cada acción que requeira "luz" en un lugar en tinieblas sería muy engorroso. Para eso existe el concepto de "capturar todas las acciones".

```dfml
before(actions: "*", except: "LookAround, GoTo", cancel: true) {
   // ...
}
```

Esto se traduce como: `Antes de 'todas las acciones', menos 'LookAround' y 'GoTo', cancelar la acción.`

## Ejemplo

```dfml
dictionary {
   // La entrada a la gruta
   noun(names: "Camino de la Montaña, camino") {
      describe-place {
         "Llegando a la base de la montaña, puedo ver la entrada a la gruta."
      }

     noun(names: "-player")

      connection(exit: "adentro", destiny: "gruta")
   }

   // La gruta
   noun(names: "La Gruta, gruta, cueva") {

      describe-place {
         "Me cubren las tinieblas. Debería 'salir' de aquí."
      }

      // ANTES de TODAS las acciones, MENOS examinar el lugar e ir hacia...
      before(actions: "*", except: "LookAround, GoTo", cancel: true) {
         "Está todo oscuro. No puedo ver nada ..."
      }

      // Atendemos la acción exceptuada GoTo
      before(actions: "GoTo", cancel: true) {

         // Solo permite la salida "afuera"
         if-direct-equals-exit(exit: "afuera") {
            resume-event() break()
         }

         // Cancela cualquier dirección distinta a "afuera"
         "No creo poder ir por ahí."
      }

      connection(exit: "afuera", destiny: "camino")
      connection(exit: "norte", destiny: "acantilado")
   }
}

```

Exceptuar las acciones GoTo y LookAround permite dar la oportunidad al jugador de salir de la gruta y describir el lugar en sí, respectivamente.

## Se hace la luz ...

En el siguiente ejemplo, se describe el lugar, solo si el jugador tiene una lámpara. La lámpara se encuentra en la entrada de la gruta:

```dfml

// La entrada a la gruta
noun(names: "Camino de la Montaña, camino") {
   describe-place {
      "Llegando a la base de la montaña, puedo ver la entrada a la gruta."
   }

   noun(names: "lámpara, luz") {
      describe-object {
         "Una lámpara de aceite, milagrosamente encendida ..."
      }
   }

   noun(names: "-player")

   connection(exit: "adentro", destiny: "gruta")
}

// La gruta
noun(names: "La Gruta, gruta, cueva") {

   describe-place {
      if-not-contains(container: "-player", instance: "lampara") {
         "Me cubren las tinieblas. Debería 'salir' de aquí."
         break()
      }
      
      "La lámpara de aceite revela la estancia. Hay un pasadizo hacia el norte."
   }

   // ANTES de TODAS las acciones, MENOS examinar el lugar e ir hacia...
   before(actions: "*", except: "LookAround, GoTo", cancel: true) {
      if-contains(container: "-player", instance: "lampara") {
         resume-event() break()
      }

      if-contains(container: "gruta", instance: "lampara") {
         resume-event() break()
      }

      "Está todo oscuro. No puedo ver nada ..."
   }

   // Atendemos la acción exceptuada GoTo
   before(actions: "GoTo", cancel: true) {

      // Solo permite la salida "afuera"
      if-direct-equals-exit(exit: "afuera") {
         resume-event() break()
      }

      // Solo permite la salida "norte" si el jugador tiene la lámpara
      if-direct-equals-exit(exit: "norte") {
         if-contains(container: "-player", instance: "lampara") {
            resume-event() break()
         }
      }

      // Cancela cualquier dirección distinta a "afuera"
      "No creo poder ir por ahí."
   }

   connection(exit: "afuera", destiny: "camino")
   connection(exit: "norte", destiny: "acantilado")
}
```
