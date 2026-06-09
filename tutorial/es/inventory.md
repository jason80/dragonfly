## Límite del inventario

[English](../en/inventory.md) | Español

Se puede limitar el inventario con diferentes magnitudes que reconoce Dragonfly y se pueden combinar entre sí.

* **Capacidad:**

La más simple de manejar. Establece una variable `capacity` con la cantidad de objetos máximos que podrá llevar el jugador:

```
noun(names: "jugador") {
   // Podrá cargar hasta 5 objetos.
   variable(name: "capacity", value: "5")
}
```

Cuando sobrepasa el máximo al intentar obtener un objeto, se disparará la respuesta `inventory-full`. Lo mismo ocurrirá con las siguientes magnitudes.

* **Peso:**

Peso máximo que podrá levantar el jugador.
Primero se establece el máximo:

```
noun(names: "jugador") {
   // Podrá cargar hasta un peso de 100.
   variable(name: "weight", value: "100")
}
```

Hay que tener en cuenta establecer el peso de los objetos que va a cargar:

```
noun(names: "llaves") {
   variable(name: "weight", value: "2")
}

noun(names: "linterna") {
   variable(name: "weight", value: "10")
}

noun(names: "billetera") {
	variable(name: "weight", value: "5")
}

```
* **Volumen:**

El volumen tiene el mismo funcionamiento que el peso. Solo reemplaza el nombre de la variable por `volume`.
