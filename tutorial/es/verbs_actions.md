## Verbos y Acciones

[English](../en/verbs_actions.md "Verbs and Actions tutorial in English") | Español

Cuando el jugador escribe una oración, Dragonfly la analiza sintácticamente para identificar el verbo y los parámetros. Por ejemplo, si el jugador escribe `mirar la caja`, Dragonfly identifica el verbo `mirar` y el parámetro `caja`.

Pero identificar el verbo es el primer paso. Luego, el analizador sintáctico debe determinar qué acción corresponde a ese verbo. Para eso, Dragonfly tiene un sistema de acciones.

Cada verbo puede tener una o varias acciones asociadas. Por ejemplo, el verbo `mirar` puede tener una acción para mirar un objeto, otra para mirar un lugar, otra para mirar dentro de un contenedor, etc.

Veamos la diferencia en la siguiente tabla:

| Oración | Acción | Detalle | Parámetros
| --- | --- | --- | --- |
| mirar | LookAround | Para mostrar el entorno del jugador | N/A
| mirar dentro de la caja | LookInside | Para una lista de objetos dentro del contenedor | caja
| mirar el anillo | ExamineObject | Descripción de un objeto determinado | anillo

El primero no toma parámetros, el segundo y el tercero sí. Son objetos directos.

Cuando se ejecuta una acción, se envía una serie de eventos a objetos determinados.

En el caso de LookAround, se envían los eventos al lugar actual (donde está el jugador). En el caso de LookInside, se envían los eventos al objeto directo, lo mismo que ExamineObject.

## Eventos

Existen dos eventos que se envían a los objetos cuando se ejecuta una acción:

* **before** (antes)
* **after** (después)

Para la siguiente oración:

```dejar el brazalete en el cofre```

Se ejecutarán las siguientes acciones:

1) El parser analiza e identifica la acción `LeaveIn` con dos parámetros: brazalete y cofre (objeto directo e indirecto).

2) Verifica que existan los objetos (directo e indirecto). En el caso de que existan, los objetos deben estar al alcance del jugador. *Si no, SE CANCELA LA ACCIÓN mostrando un mensaje de error.*

3) **Evento before**: Se envía el evento `before` a cada uno de los objetos involucrados (brazalete y cofre).
Es posible que alguno de los objetos cancele la acción ya que el desarrollador puede capturar el evento con la opción de cancelarlo. *Si sucede esto SE CANCELA LA ACCIÓN sin mostrar ningún mensaje.*

4) Ejecuta comprobaciones específicas de la acción. En este caso, que los objetos no sean el "jugador" en sí, que el cofre sea un "contenedor" y que esté abierto en el caso de que sea un objeto "cerrable". *Si no se cumplen estas condiciones SE CANCELA LA ACCIÓN mostrando un mensaje de error.*

5) **Evento after**: Continúa enviando el evento `after` a cada uno de los objetos involucrados (brazalete y cofre). Es posible que alguno de los objetos cancele la acción. *Si sucede esto SE CANCELA LA ACCIÓN sin mostrar ningún mensaje.*

6) En éste punto, la acción se ejecuta completamente. El brazalete se mueve al cofre y se muestra un mensaje de confirmación: `dejo el brazalete en el cofre`.

### Capturar eventos

#### before:

Vamos a suponer que tengo el siguiente objeto dentro de un lugar cualquiera:

```dfml
noun(names: "leño, tronco, madera") {
   describe-object() {
      "Es un leño seco, carbonizado, usado recientemente para una fogata."
   }
}
```

Mediante `recoger leño` o `coger el leño`, el jugador puede recoger el leño y llevarlo consigo.

Vamos a cancelar esta acción para que el jugador no pueda recoger el leño. Para eso, capturamos el evento `before` (antes) de la acción `TakeObject` y la cancelamos:

```dfml
noun(names: "leño, tronco, madera") {
   describe-object() {
      "Es un leño seco, carbonizado, usado recientemente para una fogata."
   }

   before(actions: "TakeObject", cancel: true) {
	  "¡El leño está caliente! mejor espero que se enfríe un poco antes de recogerlo."
   }
}
```

Nota: Se pueden capturar varias acciones a la vez, por ejemplo: `before(actions: "TakeObject, TouchObject, PushObject", cancel: true)`. En este caso, el jugador no podrá ni recoger, ni tocar, ni empujar el leño.

Si el evento no se cancela `cancel: false`, la acción se ejecutará normalmente, obtendríamos el siguiente resultado:

```> recoger el leño```
```¡El leño está caliente! mejor espero que se enfríe un poco antes de recogerlo.```
```Recojo el leño.```

La acción se ejecuta normalmente, el leño se mueve al inventario del jugador.

#### after:

El evento after se puede capturar de la misma manera que el evento before, pero se ejecuta después de que la acción se haya ejecutado completamente. Por ejemplo, si queremos mostrar un mensaje después de que el jugador haya recogido el leño, (y no mostrar el mensaje que viene por defecto) podemos hacer lo siguiente:

```dfml
noun(names: "leño, tronco, madera") {
   describe-object() {
      "Es un leño seco, carbonizado, usado recientemente para una fogata."
   }

   after(actions: "TakeObject", cancel: true) {
	  "Recojo el leño, está caliente pero lo llevo conmigo de todas formas."
   }
}
```

De la misma manera, si no cancelamos el evento, el mensaje por defecto se mostrará junto con el mensaje personalizado:

```recoger el leño```
```Recojo el leño, está caliente pero lo llevo conmigo de todas formas.```
```Recojo el leño.```

[<<< Abrir y Cerrar](open_close.md) | [Respuestas >>>](responses.md)	
