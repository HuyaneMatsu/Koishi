# Shared

Contains shared system event handlers between all clients.

### Event handlers

- `unknown_dispatch_event__structurize` -> `unknown_dispatch_event`

    Guesses the unknown dispatch event's structure.

- `unknown_dispatch_event__notify` -> `unknown_dispatch_event`
    
    Notifies about unknown dispatch event in the support guild. Runs after `unknown_dispatch_event__structurize`.

- `error__notify` -> `error`
    
    Notifies about an error in the support guild.

