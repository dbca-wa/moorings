/**
 * A global event bus powered by the `mitt` library.
 * This is a replacement for the Vue 2 event bus, as Vue 3 removed
 * the built-in `$on` and `$off` methods from component instances.
 * The name `bus` is kept for easier migration from a Vue 2 codebase.
 */
import mitt from 'mitt'

export const bus = mitt()