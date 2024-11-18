/**
 * Las condiciones son elementos a cumplir de un evento. Si al menos una condicion no se
 * cumple, el evento no ejecuta las respuestas.
*/

import { DFMLNode } from "../dfml/js/main/node.js";
import { Action } from "./action.js";

/**
 * Las condiciones son elementos a cumplir de un evento. Si al menos una condicion no se
 * cumple, el evento no ejecuta las respuestas.
 *
 * @export
 * @class Condition
 */
export class Condition {
	/**
	 * Creates an instance of Condition.
	 * @memberof Condition
	 */
	constructor() {}

	/**
	 * Comprueba la Condition (comportamiento que cambia según la condicion derivada).
	 *
	 * @param {Action} action Acción actual
	 * @return {boolean} verdadero si se cumple la condicion.
	 * @abstract
	 * @memberof Condition
	 */
	check(action) {
		return false;
	}

	/**
	 * Carga la condicion de un nodo dfml.
	 *
	 * @param {DFMLNode} node nodo dfml.
	 * @abstract
	 * @memberof Condition
	 */
	load(node) {

	}
};
