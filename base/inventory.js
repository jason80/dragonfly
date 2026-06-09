export function check_inventory(action, player, noun) {
	if (!check_capacity(action, player)) return false;
	if (!check_magnitude("weight", action, player, noun)) return false;
	if (!check_magnitude("volume", action, player, noun)) return false;

	return true;
}

function get_variable_value(name, noun) {
	return name in noun.variables ?
		parseInt(noun.getVariable(name)) : 0;
}

function check_capacity(action, player) {
	const capacity = get_variable_value("capacity", player);

	if (capacity == 0) return true;

	if (capacity <= player.children().length) {
		return action.fireResponse("inventory-full");
	}

	return true;
}

function check_magnitude(mag, action, player, noun) {
	const value = get_variable_value(mag, player);

	if (value == 0) return true;

	let total = get_variable_value(mag, noun);

	for (const n of player.children()) {
		total += get_variable_value(mag, n);
	}

	if (value < total) return action.fireResponse("inventory-full");

	return true;
}
