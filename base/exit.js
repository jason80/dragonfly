import { Entity } from "./entity.js";

/**
 * Represents a possible point where the player can go.
 *
 * @export
 * @class Exit
 * @extends {Entity}
 */
export class Exit extends Entity {
	/**
	 * Creates an instance of Exit.
	 * @memberof Exit
	 */
	constructor() {
		super();
	}

	/**
	 * Exit string description.
	 * @return {string} string of the entity.
	 *
	 * @memberof Exit 
	 */
	toString() {
		return `Exit: ${this.names}`;
	}
};
