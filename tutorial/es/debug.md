# Depuración

[English](./debug.md) | Español

Dragonfly ofrece herramientas para depurar, es decir, permiten ver el proceso de parsing, consultar los elementos del juego y establecer atributos y valores de variables en tiempo de ejecución.

## Diccionario de depuración

Incluyendo el diccionario de depuración dict-debug.dfml, puedes incluir los siguientes verbos especiales:

* **info**: Muestra la información de uno o varios sustantivos: nombres, contenedor, atributos, variables y conexiones. (Uso: `info <sustantivo>`).

* **tree**: Muestra todos los sustantivos en forma de árbol. (Uso: `tree`). Si se le pasa un sustantivo, muestra el árbol de ese sustantivo. (Uso: `tree <sustantivo>`).

* **attribute, attr**: Añade o quita un atributo a un sustantivo. (Uso: `attr <sustantivo> set/unset <atributo>`).

* **move, mv**: Mueve un sustantivo adentro de otro. (Uso: `mv <sustantivo> to <destino>`).

* **root**: Mueve un sustantivo a la raíz del árbol de objetos. (Uso: `root <sustantivo>`).

* **verb**: Muestra información de uno o varios verbos: nombres, acciones asociadas, sintaxis. (Uso: `verb <verbo>`).

* **action**: Devuelve las respuestas de una accion. Útil para crear nuevos verbos. (Uso: `action <accion>`).

* **exitlist**: Muestra la lista de todas las posibles salidas. (Uso: `exitlist`).

## El parser

#### **show-parsing-process**

Se puede habilitar mostrar el proceso interno del parser habilitando la propiedad `book`:

```dfml
property(name: "show-parsing-process", value: true)
```

Después de cada entrada se muestra:

*> x nota*

```dfml
Parser: for x, 4 verb(s) found, checking syntax ...
Parser: executing action: "ExamineObject".
Parser: Params 1=nota
```

*Una nota arrugada, con tinta pálida apenas legible.*

Esta característica es muy util para conocer la acción que se ejecuta con cada verbo.

#### **parser-clean**

El parser limpia la entrada del jugador de caracteres indeseados. Pero si el desarrollador lo necesita, se puede deshabilitar, porque hay veces que los nombres de los sustantivos incluyen caracteres indeseados y no se pueden, por ejemplo, mover de un lado a otro con `mv` o mostrar la `info`.

Para NO quitar los caracteres indeseados:

```dfml
property(name: "parser-clean", value: "")
```

Esto permite depurar de la siguiente manera:

```dfml
move serpiente to -interior-caverna
```