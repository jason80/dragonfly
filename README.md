# Dragonfly
*Interactive Fiction Game Engine in Javascript*

## Setting up the project

Clone the git repository with submodules:

```sh
git clone --recurse-submodules https://github.com/jason80/dragonfly/
```

Create and navigate mygame dir:

```sh
mkdir dragonfly/mygame
cd dragonfly/mygame
```

Create the files "index.html" and "mygame.js".

## Basic "index.html":

```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>My Game</title>
</head>
<body>
	<div id="game-area"></div>
	<script type="module" src="mygame.js"></script>
</body>
</html>
```

## File "mygame.js":

```javascript
import { Book } from "../base/book.js"

window.onload = function() {
	const book = new Book("game-area");

	book.run();
}
```

## Tutorial:
[Español](./tutorial/spanish.md "Tutorial en español")
