### 2023-05-??

- Add 3 new items to `/trivia`.
- Add `/snipe message`.
- `snipe / detials` and `snipe / actions` will not drop exception if the entity is yeeted.
- `/automation log user` now colors embeds + add new `Guild profile flags` field.

### 2023-05-08

- Rewrite `/trivia`. Now it is fully Koishi themed.
- Fix broken channel name changer (support guild only feature).
- Booru image handler now handles connection reset. Added retry too.
- Booru image handler now handles better if the response structure is invalid.
- `/ds` now handles discord server errors better. It will try to edit the message instead of destructing the game.

### 2023-04-25

- Fix `touhou-feed` now handles gateway-timeout and other server side errors.
- Fix `/touhou-calendar` now handles the case correctly when there are 0 users in a month.
  In case someone wanna copy and modify it.
- Fix `renes` (bot) now reads `Est`'s name instead of using a hardcoded one.
- Fix `/role-info` now shows integration name as intended.
- `/mod` commands now have `notify-user` parameter as `false` by default.

### 2023-04-14

- Remove redundant embed fields (example: embed footer that tells who called the command).
- Add `close` button to `/about`.

### 2023-04-11

- Fix `/mod top-list` rendered `sorted by` embed field incorrectly.
- Fix `/mod top-list` counted `self-mod` calls.

### 2023-04-07

- Fix `/mod ban`'s Orin easter egg ignored the actions done directly by the user.
- Add `/mod top-list` command.
- Add a new interaction where `action` command responses (for example of `hug`, `kiss`) can be replied with an
  `action`'s name to produce an inline action reply.

### 2023-03-26

- Fix the bug causing dungeon sweeper stages to be yeeted when a record is beaten has been (finally)
  identified and fixed.

### 2023-03-24

- Fix a bug in a dependency caused tasks to be garbage collected prematurely.
  This left a few commands like `/safebooru` in eternal *thinking* state.

### 2023-03-22

- Fix `/automation log-satori` (experimental) had no emoji difference renderer registered.
- Fix `user.waifu_stats` failed on saving.
- Add `/stats upgrade` command.
- Add `changelog.md` so later we can have a cool `/about changelog` (?) command.
