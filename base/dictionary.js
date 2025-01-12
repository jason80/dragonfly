import { DFMLElement } from "../dfml/js/main/element.js";
import { Article } from "./article.js";
import { Book } from "./book.js";
import { Noun } from "./noun.js";
import { Verb } from "./verb.js";
import { Exit } from "./exit.js";
import { actions } from "./actions.js";
import { ListDialog, ObjectChooserDialog, PropperListDialog,
			loadListDialog, loadObjectChooserDialog, loadPropperListDialog } from "./dialogs.js";
import { Conversation } from "./conversation.js";

/**
 * Contains a list of nouns, verbs and exits.
 *
 * @export
 * @class Dictionary
 */
export class Dictionary {
	/**
	 * Creates an instance of Dictionary.
	 * @param {Book} book the book instance.
	 * @memberof Dictionary
	 */
	constructor(book) {
		this.book = book;

		this.articles = [];
		this.nouns = [];
		this.verbs = [];
		this.exits = [];
		this.conversations = {};

		this.seeListDialog = new ListDialog("You can see: ", ", ", " and ");
		this.propperListDialog = new PropperListDialog("is here", "are here", ", ", " and ");
		this.objectChooserDialog = new ObjectChooserDialog(this.book, "Which one?", "Never mind.", "Please, enter the correct option.");
		this.inventoryDialog = new ListDialog("You have: ", ", ", " and ");
		this.lookInsideDialog = new ListDialog("Inside there is: ", ", ", " and ");
	}

	/**
	 * Returns the verbs that match the given name. 
	 * If the name is empty, returns all of them.
	 *
	 * @param {string} [name=""] name of the verb.
	 * @return {Array.<Verb>} list of verbs.
	 * @memberof Dictionary
	 */
	getVerbs(name = "") {
		if (name === undefined || name === "") return this.verbs;

		let result = [];
		this.verbs.forEach(v => {
			if (v.responds(name)) result.push(v);
		});

		return result;
	}

	/**
	 * Return a first ocurrence of the verb indicating the action class name.
	 * Action class name must be fully name (module.Class), for otherwise use 'actions'
	 * module by default.
	 *
	 * @param {string} className action class name
	 * @return {Verb} result verb 
	 * @memberof Dictionary
	 */
	verbByAction(className) {
		const actionClass = actions[className];

		if (!actionClass) {
			Output.error(`action class "${className}" not exists.`);
			return null;
		}

		let result = null;

		this.verbs.forEach(v => {
			if (v.action === actionClass) {
				result = v;
			}
		});

		return result;
	}

	/**
	 * Returns the nouns that match the given name. 
	 * If the name is empty, returns all of them.
	 *
	 * @param {string} [name=""] name of the noun.
	 * @return {Array.<Noun>} list of nouns.
	 * @memberof Dictionary
	 */
	getNouns(name = "") {
		if (name === "") return this.nouns;

		let result = [];
		this.nouns.forEach(n => {
			if (n.responds(name)) result.push(n);
		});

		return result;
	}

	/**
	 * Returns the noun indicating his id number.
	 * The id numbers are generated automatically for Save Game system.
	 *
	 * @param {number} id id of the noun.
	 * @return {Noun} the noun with the given id.
	 * @memberof Dictionary
	 */
	nounByID(id) {
		for (const n of this.nouns) {
			if (n.id === id) return n;
		}
		return null;
	}

	/**
	 * Returns the exit that match the given name.
	 *
	 * @param {string} name name of the exit.
	 * @return {Exit} the exit.
	 * @memberof Dictionary
	 */
	getExit(name) {
		let exit = null;
		this.exits.forEach(e => {
			if (e.responds(name))  exit = e;
		});
		return exit;
	}

	/**
	 * Returns the article with the given name.
	 * 
	 * @param {string} name name of the article.
	 * @return {Article} the article.
	 */
	getArticle(name) {
		let article = null;

		this.articles.forEach(a => {
			if (a.name === name) article = a;
		});

		return article;
	}

	/**
	 * Gets the conversation giving an owner noun.
	 *
	 * @param {string} owner the owner noun.
	 * @return {Conversation} the conversation instance.
	 * @memberof Dictionary
	 */
	getConversation(owner) {
		return this.conversations[owner];
	}

	/**
	 * Load the dictionary from dfml document.
	 *
	 * @param {Node} node dfml node.
	 * @memberof Dictionary
	 */
	load(node) {

		node.children.forEach((child) => {
			if (child.getElementType() === DFMLElement.NODE) {
				if (child.getName() === "noun") {
					const noun = new Noun(null);
					noun.book = this.book;
					noun.dictionary = this;
					noun.load(child);
					this.nouns.push(noun);
				} else if(child.getName() === "verb") {
					const verb = new Verb();
					verb.load(child);
					this.verbs.push(verb);
				} else if (child.getName() === "article") {
					const article = new Article();
					article.load(child);
					this.articles.push(article);
				} else if (child.getName() === "exit") {
					const exit = new Exit();
					exit.load(child);
					this.exits.push(exit);
				} 

				// Dialogs
				else if (child.getName() ===  "see-list-dialog") {
					this.seeListDialog = loadListDialog(child); }
				else if (child.getName() ===  "propper-list-dialog") {
					this.propperListDialog = loadPropperListDialog(child); }
				else if (child.getName() ===  "inventory-dialog") {
					this.inventoryDialog = loadListDialog(child); }
				else if (child.getName() ===  "look-inside-dialog") {
					this.lookInsideDialog = loadListDialog(child); }
				else if (child.getName() ===  "object-chooser-dialog") {
					this.objectChooserDialog = loadObjectChooserDialog(this.book, child); }

				// Conversations
				else if (child.getName() === "conversation") {
					const conversation = new Conversation();
					conversation.load(child);
					this.conversations[conversation.owner] = conversation;
				}
			}
		});

	}
}
