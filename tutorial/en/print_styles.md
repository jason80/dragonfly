# `print`, `append` and CSS styles.

English | [Español](../es/print_styles.md)

## The `print` response

It is used to display text during the game, adding a new paragraph. It is the main response used in Dragonfly for all that relates to the engine's output.

The mere fact of placing a solitary text between quotes:

```dfml
describe-object() {
    "The little bird watches you closely."
}
```

Dragonfly automatically converts it into a `print`. So the equivalent would be:

```dfml
describe-object() {
    print() {
        "The little bird watches you closely."
    }
}
```

Allows you to interpolate elements within the text, for example:

```dfml
noun(names: "little canary, canary, bird, little bird") {
    describe-object() {
        print() {
            "#1 watches you closely."
        }
    }
}
```

The result would be:
`the little canary watches you closely.`

In the following table, the interpolations that can be performed are shown, with 1: the direct object and 2: the indirect object.

*Note: "3" refers to the parameters for a multi-parameter syntax.*

Interpolation | Result
--- | ---
`#1 watches you closely.` | `the little canary watches you closely.`
`%1 watches you closely.` | `a little canary watches you closely.`
`#^1 watches you closely.` | `The little canary watches you closely.`
`%^1 watches you closely.` | `A little canary watches you closely.`

#### Conditional Interpolation:

The four values between the parentheses refer to the forms of the adjectives for each gender and number respectively.

In this example it is masculine and singular.

Interpolation | Result
--- | ---
`#^1 @1(is,is,are,are) scared.` | `The little canary is scared.`

Variables can be interpolated as well with '$'. See [Variables](variables.md) for more information.

## The `append` response

`append` is like `print`, but unlike it, it does not create a new paragraph: it adds the text to the last paragraph created. It also allows interpolating elements within the text.

```dfml
describe-object() {
    "The little bird watches you closely"
    append() {
        "keeping a respectful silence."
    }
}
```

Result:
`The little bird watches you closely keeping a respectful silence.`

It is ideal for building a paragraph conditionally and with different styles.

Note that `append` adds a space at the end of the previous text, so it is not necessary to add it manually.

## CSS Styles

You can apply CSS styles to the texts of `print` and `append` using the `style` property. Here's an example:

```dfml
describe-place() {

    print(style: "font-weight: bold;") {
        "There is a"
    }

    print(style: "color: red; font-weight: bold;") {
        "red table"
    }

    print(style: "font-weight: bold;") {
        "in the center of the room."
    }
}
```

The result would be:
<p style="font-weight: bold;">There is a <span style="color: red; font-weight: bold;">red table</span> in the center of the room.</p>
