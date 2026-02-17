## Movimiento

[English](../en/movement.md "Movement tutorial in English") | Español

La mayoría de juegos conversacionales no se limitan a una sola estancia. La forma de indicar al jugador que se mueva a través de ellas es con puntos cardinales. Supongamos que al `este` de nuestro jardín hay un camino empedrado. Vamos a crear el lugar:



```
noun(names: "El Camino Empedrado, camino") {
   describe-place() {
	  "Me encuentro caminando por un sendero empedrado. El mismo continúa hacia el este. Por el oeste se vuelve al jardín."
   }
}
```

Con "ir hacia el este" le diríamos al jugador que se dirija hacia el este. Pero en este caso no funcionará.

Esto se debe a que todavía no existe `conexion` entre el jardín y el camino empedrado.

Vamos a agregarla:

```
noun(names: "El Jardín, jardín") {
   # Aquí va la definicion del jardín
   # ...

   # Agregamos la conexion hacia el este
   connection(exit: "este", destiny: "camino")
}
```

Y para volver al jardín por el `oeste`:

```
noun(names: "El Camino Empedrado, camino") {
   # Aquí va la definicion del camino empedrado
   # ...

   # Agregamos la conexion hacia el oeste
   connection(exit: "oeste", destiny: "jardin")
}
```

Ahora el jugador se puede `ir hacia el este` o `ir hacia el oeste` navegando entre los lugares.

### Las salidas:

Para que las conexiones entre lugares funcionen, deben existir salidas. Todas las salidas posibles vienen en el diccionario "dict-xx.dfml". Aquí hay una lista completa:

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
<li>otro lado, cruza, cruzar</li>

</ul>

La sintaxis para moverse suele ser `"ir/ve hacia/al <salida>"`. También puedes escribir el nombre de la salida únicamente, por ejemplo `"norte"` o `"n"`. Dragonfly comprobará si es una salida posible y, en el caso de que lo sea, ejecutará la accion "ir hacia" del caso anterior.

Claro que si en nuestro jardín intentamos "ir hacia el sur". El resultado será:

*No puedo ir por ahí.*

Ya que en el lugar no existe la conexion cuya salida es "sur".

[<<< Comenzando](start.md) | [Abrir y cerrar >>>](open_close.md)

