## Respuestas

[English](../en/responses.md "Verbs and Actions tutorial in English") | Español

Al atender un evento, por ejemplo **before**, pudimos observar que mostramos un mensaje personalizado, se cancele o no la acción:

```dfml
noun(names: "serpiente, víbora") {
   describe-object() {
      "Parece una serpiente venenosa, mejor no me acerco mucho."
   }

   before(actions: "TakeObject, TouchObject", cancel: true) {
      "¡Ni loco me acerco a eso!"
   }
}
```

Ese mensaje `"¡Ni loco me acerco a eso!"` es una respuesta de acción (action response).

Otra forma de representar la misma respuesta es:

```dfml
print {
   "¡Ni loco me acerco a eso!"
}
```

En ambos casos, el resultado es el mismo, y Dragonfly lo reemplazará por el "nodo nativo" `response`:

```dfml
response(class: "Print") {
   "¡Ni loco me acerco a eso!"
}
```

Existen diferentes tipos de respuestas, cada una con su propia función.
Vamos a hacer que la serpiente se aleje del jugador si intenta tocarla:

```dfml
noun(names: "serpiente, víbora") {
   describe-object() {
      "Parece una serpiente venenosa, mejor no me acerco mucho."
   }

   before(actions: "TakeObject, TouchObject", cancel: true) {
      "La serpiente se aleja rápidamente."
      move(instance: "serpiente", destiny: "otra-estancia")
   }
}

```

Como se puede observar, la función `move` es una respuesta de acción que mueve un objeto a otro lugar. En este caso, movemos la serpiente a otra estancia. Y sí, puede haber varias respuestas en un mismo evento.

En este caso, Dragonfly también transformará el response `move` en `response(class: "Move", instance: "serpiente", destiny: "otra-estancia")`.

Si no queremos mover la serpiente a otra estancia y queremos llevarla a la raíz del árbol de objetos, podemos usar:

```dfml
root(instance: "serpiente")
```

Internamente root convertirá el `padre` de "serpiente" a `null` llevándola a la raíz del árbol de objetos.

Algunas respuestas están descritas en la siguiente tabla:

Respuesta | Descripción
--- | ---
print | Muestra un mensaje personalizado.
append | Como `print`, pero el mensaje se agrega a continuación del último mensaje mostrado.
attr | Agrega o quita un atributo a un objeto.
variable | Agrega o quita una variable a un objeto estableciendo su valor.
append-name | Agrega un nombre a un objeto.
move | Mueve un objeto a otro lugar.
tip | Muestra un mensaje de ayuda al jugador.
execute | Ejecuta una oración como si lo hiciera el jugador: ej: `soltar el pañuelo`.
add-connection | Agrega una conexión entre dos estancias.
remove-connection | Elimina una conexión entre dos estancias.
show-title | Muestra un título del juego.
run-conversation | Inicia una conversación con un personaje.
pause | Se queda esperando a que el jugador presione `Enter`.
clear | Limpia la pantalla.
end-game | Finaliza el juego mostrando un mensaje de victoria o derrota.
restart-game | Reinicia el juego.

[<<< Verbos y Acciones](verbs_actions.md) | [Condiciones >>>](conditions.md)
