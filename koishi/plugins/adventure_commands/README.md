# Adventure - Commands

This plugin contains the commands and other interactions related to adventuring.

# commands

- `/adventure`
    - `depart (
        location : Autocomplete,
        target : Autocomplete,
        duration : Autocomplete,
        return : Choice<str>,
        auto-cancellation : Choice<str>
    )`
    - `view`
    - `cancel`
    - `history`


The built messages are the following:
- `/adventure depart` -> `adventure create confirmation`
- `/adventure view` -> `adventure view active`
- `/adventure cancel` -> `adventure cancellation`
- `/adventure history` -> `adventure listing view`

Each message also may contain links to other ones:

- `adventure create confirmation`
    - `adventure create confirm`
    - `adventure create cancel`

- `adventure view active`
    - itself | `adventure view finalized`
    - `adventure action view`
    - `adventure listing view`
    - `adventure action listing view`
    - `adventure cancellation`

- `adventure cancellation`

- `adventure listing view`
    - itself
    - `adventure view active` | `adventure view finalized`

- `adventure create confirm`
    - `adventure view active` | `adventure view finalized`

- `adventure create cancel`

- `adventure view finalized`
    - itself
    - `adventure listing view`
    - `adventure action listing view`
    - `adventure cancellation`

- `adventure action view`
    - `adventure view active` | `adventure view finalized`
    - `adventure action listing view`
    - `adventure action battle logs`

- `adventure action listing view`
    - `adventure action view`
    - `adventure view active` | `adventure view finalized`
    - itself
