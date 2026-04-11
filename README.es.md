![Logo](media/logo.png)

*Versión actual: 0.4.1*

[English](./README.md) | Español

## ¿Qué es Dragonfly?

Dragonfly es un motor de juegos de ficción interactiva. Permite crear y jugar aventuras de conversacionales directamente en el navegador.

## Filosofía

- **Desarrollo sencillo**. Para ello, Dragonfly utiliza **DFML**: un lenguaje simple y fácil de entender (el uso de JavaScript es prácticamente innecesario).

- **Sin compilación, sin motores, sin máquinas virtuales**. Se ejecuta directamente en el navegador. No necesitas ningún programa especial para ejecutar tu juego. Puedes integrarlo fácilmente en cualquier sitio web.

---

![Game sample 1](media/sample1-es.png)

---

## Juegos de ejemplo

| Juego | Descripción | Temas abordados
|---|---|---|
| [El Bosque](https://jason80.github.io/dragonfly/samples/es/bosque/bosque.html) | Un juego simple con cinco locaciones | Básicos: Movimiento, atributos, contenedores, final |
| [Chooser](https://jason80.github.io/dragonfly/samples/es/chooser/chooser.html) | Prueba de diálogo de objetos | Básicos: Diálogo, objetos, contenedores, inventario |

---

## Configuración del proyecto

La estructura inicial del proyecto es:

```sh
index.html
mygame.js
mygame.dfml
```

## Ejemplo del archivo "index.html":

```html
<!DOCTYPE html>
<html lang="es">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>Mi Juego</title>
</head>
<body>
   <div id="game-area"></div>
   <script type="module" src="mygame.js"></script>
</body>
</html>
```

## Ejemplo del archivo "mygame.js":

```javascript
import { Book } from "https://jason80.github.io/dragonfly/base/book.js"

window.onload = function() {
   const book = new Book("game-area", "mygame.dfml");

   book.run();
}
```

## Ejemplo del archivo "mygame.dfml":

```dfml
# Nodo del libro (cabecera del libro):
book(title: "Mi Juego", author: "Juan Pérez") {

   # Indica a Dragonfly quién es el jugador:
   property(name: "player", value: "-player")

   # Incluye un diccionario predefinido (primera persona):
   include(src: "https://jason80.github.io/dragonfly/templates/dict-es1.dfml")
}

# Todos los objetos (sustantivos) se definen en el nodo dictionary:
dictionary {
   # Definición de un jardín:
   noun(names: "El Jardín, jardín") {
      describe-place {
         "Estoy de pie en medio de un jardín lleno de colores."
      }

      # Definición del jugador:
      noun(names: "Vincent, jugador, -player") {
         describe-object {
            "Un aventurero, listo para explorar el mundo que me rodea."
         }
      }
   }
}
```

---

## Ejecutar el juego:

Ejecuta el juego en tu navegador usando un servidor local:

### Usando Python3:

En tu terminal, introduce:

```sh
python3 -m http.server
```

Copia la URL indicada y ábrela en tu navegador.

### Usando VSCode:

Abre la carpeta del proyecto y ejecuta el comando Run with Live Server
(instala la extensión Live Server si es necesario).

![Game sample 1](media/sample2-es.png)

## Descargar Dragonfly

Puedes clonar el proyecto utilizando git de la siguiente forma:

```sh
git clone --recurse-submodules https://github.com/jason80/dragonfly mygame
```

El parámetro `--recurse-submodules` sirve para descargar el módulo `dfml` del cuál Dragonfly depende.

## Tutoriales:
[English](./tutorial/en/start.md) | [Español](./tutorial/es/start.md)

#### Mas documentación:

* [Doors](./tutorial/en/doors.md) | [Puertas](./tutorial/es/doors.md)

* [Darkness](./tutorial/en/darkness.md) | [Oscuridad](./tutorial/es/darkness.md)

* [Ambient sounds (Sequences)](./tutorial/en/sequences.md) | [Sonidos ambientales (Secuencias)](./tutorial/es/sequences.md)

* [Debug](./tutorial/en/debug.md) | [Depuración](./tutorial/es/debug.md)

* [Actions table](./tutorial/en/actions_table.md) | [Tabla de acciones](./tutorial/es/actions_table.md)
