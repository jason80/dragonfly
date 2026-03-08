## El Parser

[English](../en/parser.md "Parser tutorial in English") | Español

El parser es el componente del motor de juego que se encarga de interpretar la entrada del jugador y traducirlos en acciones dentro del juego.

Descompone la oración ingresada por el jugador en sus partes constituyentes, identificando el verbo y los objetos involucrados. Luego, determina qué acción corresponde a ese verbo según las palabras clave y dichos objetos.

---

A continuación, se detallarán de forma general los pasos que sigue el parser para procesar la entrada del jugador:

### 1 - Limpia caracteres indeseados.

Se eliminan caracteres:

```
- _ # $ @ & + * ; /
```

Estos caracteres no aportan información relevante para el parser y pueden interferir con la interpretación de la entrada.

*Nota: se puede configurar el parser para que ignore ciertos caracteres específicos estableciendo en el nodo `book`:*
*```property(name: "parse-clean", value: "_#$@&+*;/")```*

### 2 - Busca verbos.
Busca en el diccionario verbos que coincidan con la primera palabra ingresada. Espera encontrar uno o más verbos que coincidan con esa palabra. Si no encuentra ninguno, salta al paso 2A.

#### 2A - Busca salidas.
Busca salidas registradas en el diccionario. Como `norte`, `sur`, `este`, `oeste`, etc. Si encuentra una salida que coincida con la palabra ingresada, ejecuta la acción `GoTo` de forma implícita, y pone como objeto directo la salida encontrada. El proceso se detiene aquí, y el parser arranca de nuevo con la entrada `ir hacia "salida"`. Si la salida existe o no en el lugar actual, será manejado por la acción `GoTo`.

Si no se encuentra ninguna salida que coincida con la palabra ingresada, el parser devuelve el típico mensaje `"no se lo que estás diciendo"`. El proceso se detiene aquí.

#### 2B - Encontró verbos.

Si encuentra uno o más verbos que coincidan con la palabra ingresada, el parser continúa para determinar cuál es el verbo más adecuado según la sintaxis.

### 3 - Revisa la sintaxis.

Cada verbo declarado en el diccionario tiene una sintaxis asociada, que indica qué tipo de objetos espera recibir. El parser busca en la oración ingresada por el jugador los objetos que coincidan con esa sintaxis. Algunas veces involucran palabras clave, como `con`, `a`, `en`, etc. Otras veces, simplemente esperan un objeto directo y/o indirecto.

Si no llega a coincidir con la sintaxis de ningún verbo encontrado, el parser devuelve el típico mensaje `"no se lo que estás diciendo"`. El proceso se detiene aquí.

### 4 - Ejecuta la acción.
Ejecuta la acción asociada al verbo encontrado, pasando como parámetros los objetos identificados en la sintaxis.

*Nota: en este punto todavía no se sabe si los objetos directo e indirecto son válidos o no, eso se maneja dentro de la acción ejecutada.*

---

## Diferencias entre sintaxis:

Los verbos se declaran con el nodo clave `verb`, y cada uno tiene una acción y una sintaxis asociada Vienen declarados en `templates/dict-es1.dfml`. Al ser `multiname` puede haber varios verbos con el mismo nombre pero con sintaxis diferentes. El parser se encarga de identificar cuál es el verbo más adecuado según la sintaxis de la oración ingresada por el jugador. Veamos cuatro verbos con el mismo nombre pero con sintaxis diferente:


```
verb(names: "examinar, examina, mirar, mira, busca, buscar, revisa, revisar, x, m",
        action: "LookInside", syntax: "en/dentro/adentro, 1") {
   response(id: "direct-not-found", string: "No encuentro eso.")
   response(id: "direct-is-the-player", string: "Puedes probar con: inventario o i.")
   response(id: "direct-is-not-container", string: "No puedo ver adentro de #1.")
   response(id: "direct-is-closed", string: "#^1 est@1(á,á,án,án) cerrad@1(o,a,os,as).")
   response(id: "container-is-empty", string: "No hay nada en #1.")
}
```

```
verb(names: "examinar, examina, mirar, mira, x, m",
         action: "ExamineObject", syntax: "a/al, 1") {
   response(id: "direct-not-found", string: "No hay eso.")
}
```
```
verb(names: "examinar, examina, mirar, mira, x, m",
         action: "ExamineObject", syntax: "1") {
   response(id: "direct-not-found", string: "No hay eso.")
}
```
```
verb(names: "examinar, examina, mirar, mira, ver, x, m",
         action: "LookAround")
```

Incluso dos de ellos apuntan a la misma acción, pero con sintaxis diferente.

---

### Casos especiales:

**Verbos multiparámetros:** Casos como TalkTo involucran una oración después del objeto directo, que se interpreta como un mensaje a enviar al personaje con el que se habla. En este caso, el parser identifica el verbo, busca un objeto directo que coincida con la sintaxis y luego toma el resto de la oración como el mensaje a enviar.

[<<< Condiciones](../es/conditions.md "Conditions tutorial in Spanish") | [>>>](.md)
