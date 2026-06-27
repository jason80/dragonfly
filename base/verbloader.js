import { Entity } from "./entity.js";
import { Verb } from "./verb.js";
import { Utils } from "./utils.js";
import { actions } from "./actions.js";
import { DFMLElement } from "../dfml/js/main/element.js";

export function loadVerb(dictionary, node) {

    // Get syntax
    const originalSyntax = [];
    if (node.hasAttr("syntax")) {
        node.getAttr("syntax").getValue().split(',').forEach(n => {
            originalSyntax.push(n.trim());
        });
    } else {
        dictionary.verbs.push(_loadVerb(node, dictionary, originalSyntax));
        return ;
    }

    // Get first syntax
    let syntax = [];
    let optional = false;
    originalSyntax.forEach(s => {
        if (s.startsWith("[") && s.endsWith("]")) {
            s = s.substring(1, s.length - 1);
            optional = true;
        }
        syntax.push(s);
    });
    
    dictionary.verbs.push(_loadVerb(node, dictionary, syntax));

    // Second syntax: remove optional
    if (!optional) return ;

    syntax = [];
    originalSyntax.forEach(s => {
        if (!s.startsWith("[")) {
            syntax.push(s);
        }
    });

    dictionary.verbs.push(_loadVerb(node, dictionary, syntax));
}

function _loadVerb(node, action, syntax) {

    const verb = new Verb();
    
    // Call load Entity base function
    Entity.prototype.load.call(verb, node);

    // Set syntax
    verb.syntax = syntax;

    // Load action
    if (!Utils.expectedAttributes(node, "action")) return ;
    
    const actionClassName = node.getAttr("action").getValue();
    let actionClass = actions[actionClassName];

    if (!actionClass) {
        actionClass = debugActions[actionClassName];
    }

    if (!actionClass) {
        Output.error(`action class "${actionClassName}" not exists.`);
    } else {
        verb.action = actionClass;
    }

    // Responses
    node.children.forEach((e) => {
        if (e.getElementType() === DFMLElement.NODE) {
            if (e.getName() === "response") {

                if (!Utils.expectedAttributes(e, "id", "string")) return ;

                verb.setResponse(e.getAttr("id").getValue(), 
                e.getAttr("string").getValue());
            }
        }
    });

    return verb;
}