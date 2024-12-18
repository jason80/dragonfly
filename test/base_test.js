import { Utils } from "../base/utils.js";

describe("Base", function() {
	it("(Utils) isEquals", function() {
		const name1 = '\u0041\u006d\u00e9\u006c\u0069\u0065'; // Amélie
		const name2 = '\u0041\u006d\u0065\u0301\u006c\u0069\u0065'; // Amélie
		expect(Utils.isEquals(name1, name2)).toBeTrue();

		expect(Utils.isEquals("ñandú", "nandu")).toBeTrue();
	});
});
