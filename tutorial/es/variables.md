# Variables

[English](../en/variables.md) | Español

Los sustantivos (nouns) pueden tener variables. Las variables permiten guardar información que puede variar durante la partida. El tipo de dato que almacenan son cadenas de caracteres, siempre.

Al igual que los atributos, se pueden declarar variables en el cuerpo del sustantivo:

```dfml
noun(names: "fósforos, cerillas, fosforo, cerilla") {
   set { "plural" }

   variable(name: "cantidad", value: "3")

   describe-object() {
      "Estos fósforos son usados para iluminar. Hay $(fosforos.cantidad) cerillas."
   }
}
```

---

### Respuestas

Existen varias respuestas para manipular las variables:

Respuesta | Descripción | Uso
--- | --- | ---
variable-set | Establece el valor de una variable a un objeto. | `variable-set(instance: "cerillas", name: "cantidad", value: "5")`
variable-add | Suma un valor a una variable. El valor debe ser un número auque esté dentro de comillas y si no se especifica, el valor será "1" | `variable-add(instance: "cerillas", name: "cantidad", value: "2")`.
variable-sub | Resta un valor a una variable. El resto se comporta como `variable-add` | `variable-sub(instance: "cerillas", name: "cantidad", value: "2")`.

Se pueden interpolar elementos en los valores de las variables:

```dfml
variable-set(instance: "jugador", name: "pasos", value: "$(contador.pasos)")
```

---

### Condiciones

Condición | Descripción
--- | ---
if-variable-equals | Se cumple si el valor de una variable es igual a un valor dado.
if-variable-not-equals | Se cumple si el valor de una variable no es igual a un valor dado.
if-variable-lt | Se cumple si el valor de una variable es menor que un valor dado.
if-variable-lte | Se cumple si el valor de una variable es menor o igual que un valor dado.
if-variable-gt | Se cumple si el valor de una variable es mayor que un valor dado.
if-variable-gte | Se cumple si el valor de una variable es mayor o igual que un valor dado.

Para todas estas condiciones, los parametros son los mismos y se pueden interpolar.

---

### Variables globales (No implementado)

Las variables globales no están contenidas por sustantivos. La forma de declarar una variable global es dentro del nodo `dictionary`.

La forma de modificar o acceder a una variable global es obviando el atributo `instance` de las respuestas y condiciones.

Y la forma de interpolar una variable global es simplemente `$(variable)` (tambien obviando el sustantivo).

[<<< Procedimientos](procedures.md)
