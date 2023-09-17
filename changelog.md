### 2023-09-17

- Add missing `Yamashiro Takane` touhou character.
- Add missing `Komakusa Sannyo` touhou character.
- `/automation welcome` now sends images.
- Now you can reply with interactions (such as `hug`, ...) on welcome messages.
- Restructure old `/accessibility` command, now `notification-settings` is a sub-command group (also rename commands).
- Add new `/accessibility character-preference` commands (show, add and remove).
- Actions, such as `/pocky-kiss` now will respect your character preference.

### 2023-09-09

- Add **1** image to `/like` interaction.
- Add new `/kon` interaction (with **41** images!!).
- Fix `/automation log-satori` sent `guild_user_update` events to all guilds instead of just the current.

### 2023-09-03

- `/ds play` discord lag checking had bad condition. :KoishiFail:
- `/mod top-list` now disables the `next` button if there is nothing next.
- `/mod top-list` is now partially tested. (So less bugs, yay).
- `/top-list` and `/mod top-list` outputs are now standardised.
- `/automation log-sticker` now uses `2` embeds, so Discord will stop adjusting embed width to sticker size!!!
- `/snipe` now uses `2` embeds for stickers, for the same reason as above ^.
- `/automation log-users` now says how much users are in the guild!!
- `/automation log-satori` now sends messages for guild profile updates.

### 2023-08-23

- Fix `/snipe` assigned bad `yeet` button for emojis, causing it to not pop up the confirmation form.
- `Renes` now will tell where `Alice` went live.
- `/top-list` now has buttons to move between pages!.
- `/top-list` is now tested.
- `/top-list` color scheme updated.
- Fix error while creating new `/automation` entries.

### 2023-08-16

- Fix `/automation log-satori` raising on activity create. :KoishiFail:
- Fix `/automation log-satori` initial message raising on activity (without custom). :KoishiFail:
- Add `Yomotsu Hisami` touhou character.
- Add `Mitsugashira Enoko` touhou character.
- Add `Tenkajin Chiyari` touhou character.
- Add `Son Biten` touhou character.
- Add `Nippaku Zanmu` touhou character.
- Add `6` new images to `like` interaction.
- Add `/like` as an actual command.
- Fix `/automation reaction-copy` raising when turned off.

### 2023-08-11

- `snipe` now checks for the new `create-guild-expression` permission when borrowing.
- `/automation reaction-copy list-channels` now has new `refresh` and `close` buttons.
- `/automation log-satori` initial message now shows user presence.
- `/automation log-satori` now creates initial messages for every channel and not only for auto-started ones.
- Fix `/ascii avatar` command now wont ignore `size` parameter when getting global avatar.
- `/ascii` commands now support a new `colored` parameter.

### 2023-07-25

- `/automation welcome` now respects onboarding.
- Add `/automation reaction-copy role-set` allowing to specify an additional role for the feature to be used by.
- Add `/automation reaction-copy role-remove` to remove the role.
- Rename `/automation show-all` to `/automation list-all`.

### 2023-07-24

- Add `2` new images to `like` interaction.
- `/automation log-user` messages show `user flags` and `display name` fields.
- `/automation log-satori auto-start` messages show `user flag` and `display name` fields.

### 2023-07-22

- `/user info` now shows 3 new fields: `user flags`, `guild profile flags`, `display name`.

### 2023-07-15

- `touhou-feed` now works in media channels too.
- Rewrite `anilist` plugin and fix various bugs.
- Koishi now uses a more package-like format to keep it matched with best hata practices.

### 2023-07-03

- `/automation` settings are not lost anymore on restart. It got its own db table and load / save logic.
- `/automation` command is now public. This includes `welcome`, `log-emoji`, `log-sticker`, `log-mention`, `log-user`.
    `log-satori` is not public and probably will not be in the future either.
- `touhou-feed` is now an option of `/automation`. Guilds that used it before have it set as `true` by default.
- `reaction-copy` is now public.
- `reaction-copy` is now an option of `/automation`. Guilds that used it before have it set as `true` by default.
- Fix `reaction-copy` case: users could target channels they had no access to. 

### 2023-07-01

- Add `2` new images to `like` interaction.
- `Satori` now will auto crosspost messages in the new `koishi-news` channel.

### 2023-06-17

- When replying on an interaction (such as: `hug`, `kiss`, ...) now supports an additional `like` action.

### 2023-06-11

- Fix `/meme` got `forbidden` back from reddit.

### 2023-06-05

- `booru` tags are now separated by `,` (from `|`).
- Fix `booru` command autocompletion ignored already defined tags.
- Parsing multiple `booru` tags improved. Now they handle more amount and more different characters too.

### 2023-05-30

- Fix `satori log` channel check. When channel's name was not decimal the conversion was handled incorrectly.
- Fix `/snipe` when switching between choices. (From previous update.)
- Add `/snipe soundboard-sound`.

### 2023-05-29

- Add 3 new items to `/trivia`.
- Add `/snipe message`.
- `snipe / detials` and `snipe / actions` will not drop exception if the entity is yeeted.
- `/automation log user` now colors embeds + add new `Guild profile flags` field.
- Fix `/help` command's header formatting.

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
- Fix `Renes` (bot) now reads `Est`'s name instead of using a hardcoded one.
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
