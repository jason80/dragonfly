## Condiciones

[English](../en/conditions.md) | Español

Atender un evento se vuelve más dinámico cuando se pueden agregar condiciones a la par de las respuestas. Esto permite que el evento solo se ejecute si se cumplen estas condiciones.

Vamos a suponer que queremos describir un lugar mostrando un texto cuando el mismo se visita por primera vez, y otro texto diferente para las siguientes visitas. Para esto podemos usar una condición que revise si el lugar fue visitado o no.

```dfml
noun(names: "La Ciénaga, cienaga") {

   describe-place() {
      if-is-not-set(instance: "cienaga", attr: "described") {
         "Ni bien llego a la ciénaga, me doy cuenta que es un lugar muy húmedo y lleno de vegetación. El aire es denso y el olor a tierra mojada es fuerte. Es un lugar misterioso y un poco inquietante."
      }

      if-is-set(instance: "cienaga", attr: "described") {
         "Entre el aire denso y el olor a tierra mojada, vuelvo a estar en este inquietante lugar."
      }

      append { "Una suerte de camino entre el barro se desprende hacia el oeste, por el sur vuelvo a la selva." }
   }
}
```

De esta forma, la primera vez que se ejecute el evento `LookAround` en el lugar `La Ciénaga`, se mostrará el primer texto y le establecerá el atributo `described`. En las siguientes ejecuciones del mismo evento, se mostrará el segundo texto. El tercer evento `LookAround` se ejecutará siempre, sin importar si el lugar fue visitado o no, ese texto se agregará a continuación de la última línea mostrada.

### Condiciones anidadas

Puede haber más de una condición en un mismo evento. La forma de presentarlas en el evento es la siguiente:

```dfml
noun(names: "carta, papel, sobre, correo") {

   after(actions: "ReadObject", cancel: false) {
      if-contains(instance: "vela", container: "oficina") {
         if-is-set(instance: "vela", attr: "encendida") {
            if-contains(instance: "gafas", container: "jugador") {
               "Es otra carta del señor magistrado."
               cancel-event()
            }
         }
      }
   }
}
```

En este caso, el texto `"Es otra carta del señor magistrado."` se mostrará solo si la vela está en la oficina, la vela está encendida y el jugador tiene las gafas. Si alguna de estas condiciones no se cumple, el evento no se cancelará y se mostrará la frase por defecto: `"No se puede leer la carta."`.

Al igual que las respuestas, Dragonfly reemplazará las condiciones por sus equivalentes utilizando el nodo nativo `response`. Las condiciones también son clases de Javascript que extienden de `Response`.

El equivalente de `if-is-set(instance: "vela", attr: "encendida")` es el siguiente:

```dfml
response(class: "IfIsSet", instance: "vela", attr: "encendida") {
   // respuestas a ejecutar
}
```

Estas son algunas de las condiciones disponibles:

Condición | Descripción
--- | ---
if-is-set | Se cumple si el atributo de la instancia está establecido.
if-is-not-set | Se cumple si el atributo de la instancia no está establecido.
if-direct-equals-exit | Se cumple si el `objeto directo` equivale a una `salida` registrada en el diccionario.
if-contains | Se cumple si una instancia contiene otra instancia.
if-not-contains | Se cumple si una instancia no contiene otra instancia.
if-direct-equals | Se cumple si el `objeto directo` es igual a una instancia.
if-direct-not-equals | Se cumple si el `objeto directo` no es igual a una instancia.
if-indirect-equals | Se cumple si el `objeto indirecto` es igual a una instancia.
if-indirect-not-equals | Se cumple si el `objeto indirecto` no es igual a una instancia.
if-variable-equals | Se cumple si el valor de una variable es igual a un valor dado.
if-connection-exists | Se cumple si existe una conexión en un lugar indicando su salida.
if-connection-not-exists | Se cumple si no existe una conexión en un lugar indicando su salida.

[<<< Respuestas](responses.md) | [El Parser >>>](parser.md)
