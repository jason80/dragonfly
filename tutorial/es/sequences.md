# Secuencias

[English](../en/sequences.md "Sequences english Tutorial") | Español

Las secuencias son respuestas que agrupan otras respuestas. Internamente tienen un contador, cuando la secuencia se "ejecuta" se ejecuta la respuesta donde apunta el índice del contador y luego incrementa el contador. Si ya se ejecutaron todas las respuestas, vuelven a empezar con la primera.

```dfml
sequence {
   "El tendero dice: '¡Hola, bienvenido a mi tienda!'"
   "El tendero dice: 'No olvides consultar mis precios.'"
   "El tendero dice: 'Estoy aquí para ayudarte con tus compras.'"
   "El tendero dice: '¡Las pociones están de oferta!'"
   "El tendero dice: 'Debería abrir los sábados ...'"
}
```

Como la secuencia es una respuesta, va adentro de un evento o un procedimiento. Veamos un ejemplo de un procedimiento para activar la verborragia del tendero:

```dfml
procedure(name: "tendero-habla") {

   "El tendero dice:"

   sequence {
      append { "'¡Hola, bienvenido a mi tienda!'" }
      append { "'No olvides consultar mis precios.'" }
      append { "'Estoy í para ayudarte con tus compras.'" }
      append { "'¡Las pociones están de oferta!'" }
      append { "'Debería abrir los sábados ...'" }
   }
}
```

```dfml
noun(names "Tienda") {
   describe-place() {
      // ....
   }

   // Se define al tendero dentro de la tienda, entre otras cosas
   // ....

   // Llama al procedimiento todas las veces que haya una acción en la tienda.
   after(actions: "*", except: "GoTo") {
      call(procedure: "tendero-habla")
   }
}
```

---

## Chances

Se vuelve bastante molesto que el tendero hable por cada cosa que haga el jugador. Para que el tendero hable menos podemos agregar una chance de ejecutar la secuencia:

```dfml

sequence(chance: 0.2) {
   append { "'¡Hola, bienvenido a mi tienda!'" }
   append { "'No olvides consultar mis precios.'" }
   ...
}
```

Ahora, dirá una frase con un 20% de probabilidad por cada acción que haga el jugador. Por defecto, la probabilidad es 100% (1.0).

---

## Mezcla

Si queremos que el tendero hable de forma aleatoria, podemos mezclar las respuestas:

```dfml
sequence(shuffle: true, chance: 0.2) {
   append { "'¡Hola, bienvenido a mi tienda!'" }
   append { "'No olvides consultar mis precios.'" }
   append { "'Estoy aquí para ayudarte con tus compras.'" }
   append { "'¡Las pociones están de oferta!'" }
   append { "'Debería abrir los sábados ...'" }
}
```

Dragonfly *mezclará las respuestas solo al principio del juego*, cuando se carga el diccionario. NO se escogerán respuestas al azar en tiempo de ejecución.

---

## Sonidos de Ambiente

De forma similar, podemos simular sonidos de ambiente agregando un evento similar, aprovechando las características aleatorias de las secuencias y las chances de aparecer.

Frases como:

```dfml
sequence(shuffle: true, chance: 0.2) {
   print(style: "class: df-ambient") { "Se escucha un grito a lo lejos ..." }
   print(style: "class: df-ambient") { "Se escuchan ruidos en las paredes ..." }
   print(style: "class: df-ambient") { "Los grillos suenan por todas partes ..." }
   ...
}
```
