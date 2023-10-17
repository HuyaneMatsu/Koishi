# Blacklist core

Contains core logic for blacklisting users from using the application.

## API

- `BLACKLIST: dict<int, int>`

    `user-id` to `entry-id` relation containing the blacklisted users. Populated on startup.


- `build_blacklist_user_add_embed(user: ClientUserBase, success: bool): Embed`

    Builds blacklist user add embed.


- `build_blacklist_user_entry_embed(user: ClientUserBase, success: blacklisted): Embed`

    Builds a user blacklist entry embed.


- `build_blacklist_user_remove_embed(user: ClientUserBase, success: bool): Embed`

    Builds blacklist user remove embed.


- `is_user_id_in_blacklist(user_id: int): bool`

    Returns whether the given user identifier is blacklisted.


- `add_user_id_to_blacklist(user_id: int): Coroutine<bool>`

    Adds the user's identifier to the blacklist. Returns whether they were added. So false if they are already in.


- `add_user_id_to_blacklist_with_connector(user_id: int, connector: AsyncConnection): Coroutine<bool>`

    Familiar to `add_user_id_to_blacklist`, but uses an existing database connector.


- `remove_user_id_from_blacklist(user_id: int): Coroutine<bool>`

    Adds the user's identifier to the blacklist. Returns whether they were removed. So false if they are were not in.


- `remove_user_id_from_blacklist_with_connector(user_id: int, connector: AsyncConnection): Coroutine<bool>`

    Familiar to `remove_user_id_from_blacklist`, but uses an existing database connector.
