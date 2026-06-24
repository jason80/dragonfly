# `print`, `append` y los estilos CSS.

[English](../en/print_styles.md) | Español

## La respuesta `print`

Se utiliza para mostrar texto durante el juego, agregando un nuevo párrafo. Es la respuesta principal que se utiliza en Dragonfly en todo lo que se refiere a la salida del motor.

El solo hecho de colocar un texto solitario entre comillas:

```dfml
describe-object() {
    "El pequeño pájaro te observa atentamente."
}
```

Dragonfly lo convierte automáticamente en un `print`. Entonces el equivalente sería:

```dfml
describe-object() {
    print() {
        "El pequeño pájaro te observa atentamente."
    }
}
```

Permite interpolar elementos dentro del texto, por ejemplo:

```dfml
noun(names: "pequeño canario, canario, pajaro, pajarito") {
    describe-object() {
        print() {
            "#1 te observa atentamente."
        }
    }
}
```

El resultado sería:
`el pequeño canario te observa atentamente.`

En la siguiente tabla se muestran las interpolaciones que se pueden realizar, siendo 1: el objeto directo y 2: el objeto indirecto.

*Nota: "3" se refiere a los parámetros para una sintaxis multiparámetro.*

Interpolación | Resultado
--- | ---
`#1 te observa atentamente.` | `el pequeño canario te observa atentamente.`
`%1 te observa atentamente.` | `un pequeño canario te observa atentamente.`
`#^1 te observa atentamente.` | `El pequeño canario te observa atentamente.`
`%^1 te observa atentamente.` | `Un pequeño canario te observa atentamente.`

#### Interpolación condicional:

Los cuatro valores entre los paréntesis se refieren a las formas de los adjetivos para cada género y número respectivamente.

En este ejemplo es masculino y singular.

Interpolación | Resultado
--- | ---
`#^1 asustad@1(o,a,os,as).` | `El pequeño canario asustado.`

También se pueden interpolar variables con '$'. Consulta [Variables](variables.md) para más información.

## La respuesta `append`

`append` es como `print`, pero a diferencia de este, no crea un nuevo párrafo: agrega el texto al último párrafo creado. También permite interpolar elementos dentro del texto.

```dfml
describe-object() {
    "El pequeño pájaro te observa atentamente "
    append() {
        "guardando un respetuoso silencio."
    }
}
```

Resultado:
`El pequeño pájaro te observa atentamente guardando un respetuoso silencio.`

Es ideal para construir un párrafo de forma condicional y con diferentes estilos.

Nótese que `append` agrega un espacio al final del texto anterior, por lo que no es necesario agregarlo manualmente.

## Estilos CSS

Se puede aplicar estilos CSS a los textos de `print` y `append` mediante la propiedad `style`. Por ejemplo:

```dfml
describe-place() {

    print(style: "font-weight: bold;") {
        "Hay una"
    }

    print(style: "color: red; font-weight: bold;") {
        "mesa de color rojo"
    }

    print(style: "font-weight: bold;") {
        "en el centro de la habitación."
    }
}
```

El resultado sería:
<p style="font-weight: bold;">Hay una <span style="color: red; font-weight: bold;">mesa de color rojo</span> en el centro de la habitación.</p>
