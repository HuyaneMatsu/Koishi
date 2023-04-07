### 2023-04-07

- Fix `/mod ban`'s Orin easter egg ignored the actions done directly by the user.
- Add `/mod top-list` command.
- Add a new interaction where `action` command responses (for example of `hug`, `kiss`) can be replied with an
  `action`'s name to produce an inline action reply.

### 2023-03-26

- Hotfix: The bug causing dungeon sweeper stages to be yeeted when a record is beaten has been (finally)
  identified and fixed.

### 2023-03-24

- Hotfix: A bug in a dependency caused tasks to be garbage collected prematurely.
  This left a few commands like `/safebooru` in eternal *thinking* state.

### 2023-03-22

- Fix `/automation log-satori` (experimental) had no emoji difference renderer registered.
- Fix `user.waifu_stats` failed on saving.
- Add `/stats upgrade` command.
- Start writing `changelog`, so later we can have a cool `/about changelog` (?) command. 
