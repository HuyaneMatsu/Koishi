### 2024-03-31

- Add `Hakurei Miko` touhou character.
- Add `Install me!` button under `/about`.
- Fix a `snipe` bug when sniping reactions.
- Add **4** images to `/pocky-kiss` (1 was there just unused).
- Add **33** images to `/pat`.
- Add **1** image to `/like`.
- Add **26** image to `/lick`.
- Add **1** image to `/kon`.
- Add **36** images to `/kiss` (1 was there just unused).
- Add **51** images to `/hug`.
- Add **2** images to `/fluff`.
- Sort `/pocky-kiss` images alphabetically.
- Grouped image handlers how will go though every registered handler before failing.
- Sending some embeds failed.
- Koishi, Flandre, Yoshika, Cursed Sakuya now can be user installed.

### 2024-03-18

- Add `feed` interaction with **13** images. (Will get more in the future obviously.)
- Fix interactions like `/kiss` counted the invoking user into the cooldown since a previous update fixing source
    user's mention showing up incorrectly.

### 2024-03-02

- Add **1** image to `/like` interaction.
- Add **1** image to `/kon` interaction.
- Refreshing embed images is now retried **2** times. Turned out once is not enough.
- `/automation log-user`, `/automation log-emoji`, `/automation log-sticker`, `/atiomation log-satori` now requires
    `embed links` permission as intended.
- `/automation log-mention` now requires `attach files` permission as intended.
- Add new `daily reminder` options to `/accessibility notification-settings change` command (false by default).
- Add new `/accessibility notification-settings set-notifier` command allowing you to configure who should deliver
    your configurations.
- Add new `daily_reminder` plugin. Linked to the newly added notification setting.
    Notifies the user about not claiming their daily just because they would lose their first streak.

### 2024-02-18

- Add **2** blacklisted (explicit) tags to safe booru queries.
- Add **1** image to `/meme` command.
- Add **2** image to `/kon` interaction.
- Add new `/fluff` interaction with **68** images.
- Add `pocky` alternative version of `pocky-kiss` reply interaction.
- Add **1** image to `/pocky-kiss` interaction.

### 2024-02-03

- Add `list of shame` to booru image handler to filter out artists who use ai.
- `/automation touhou-feed` now respects `embed links` permission.
- Action command replies, such as `/hug` replies now mention the invoking user as intended.
    Was intended to be part of the last update, but turned out replies work a little differently this regard.
- Add **6** image to `/kon` interaction.
- Add **6** image to `/meme` command.
- Add new `/automation community-message-moderation log-state` and `... log-channel` commands.
- Fix `/mod regret-un-ban` failing. (Since last update.)
- Add **1** image to `/like` interaction.

### 2024-01-17

- Add new `automation_community_message_moderation` plugin to allow users vote for deleting messages.
- Add new `/automation community-message-moderation` commands to configure the feature..
- `/automation welcome` replies now mention the invoking user as well to fix `source-user` was not showing up correctly
    in the message's content. (Discord issue)
- Action command and replies, such as `/hug` now mention the invoking user as well to fix `source-user` was not
    showing up correctly in the message's content. (Discord issue)

### 2023-11-13

- When claiming roles (in rules) the original message was edited instead of new being created.
    The fact that it worked before makes it sus.

### 2023-12-31

- Separate image commands into multiple directories.
- Add blacklist for waifu api images to filter a little bit too spicy images out.
- Write new `/meme` command now filled with berigoos!!
- Add headers for Cursed Sakuya.
- Add assets & their information to `pocky-kiss (self)` interaction.
- A few `pocky-kiss (self)` images were registered incorrectly (duplicate, bad character or being omitted).
- Add **2** image to `/kon` interaction.
- Separate the `image_handling_commands` into multiple plugins.

### 2023-12-17

- Add **8** image to `/kon` interaction.
- Action commands (such as `/hug`) now user the color of the user.
- Action replies now use the color of the user.
- `/automation reaction-copy` always only selected the first client. (Messed up the fix last update.)
- Add `flandre` themed welcome style. Flandre will use her own style by default.
- Add `/automation welcome style` command where you can select a non-default welcome style as well.
- Rename `/automation welcome button` to `/automation welcome reply-buttons`.
- Add `Your greeting` welcome reply button.
- `/automation welcome reply-buttons` now sends reply with the color of the user.
- `/heartshop roles` costs and names adjusted.

### 2023-12-09

- `/waifu-info` no longer sets `embed.timestamp` since it shows the same date as when the message was created at.
- `/automation reaction-copy` did not select the first client satisfying the required permission.
- `/automation touhou-feed` now handles permission changes without cancelling itself.
- Add `embed_image_refresh` plugin which allows refreshing embed image if requested.
- `/atiomation welcome` now refreshes embed image.
- `/automation welcome button` now refreshes embed image.
- Action commands (such as `/hug`) now refresh embed image.
- Action replies now refresh embed mage.
- Add **1** image to `/kon` interaction.
- Add new sex tier (`totally sex`).
- Add headers for all feature clients.
- Fix `AttributeError` in `/automation log satori`'s `guild_delete` event handler (from feature-clients update).

### 2023-11-19

- Add `Satsuki Rin` touhou character.
- Touhou feed now has a 80% chance to skip images if there are too many characters on it.
- `/automation welcome button` now has its own emoji for each button label.
- `/automation logging` messages are now more colorful.
- Actions such as `/hug` now support targeting roles.

### 2023-11-05

- Add `/automation welcome button` command.
- `automation_welcome` now can put a button under the welcome message to reply.
- Fix a `/automation` bug that made new guilds to not be correctly stored in the database.
- Add `automation_chat_interaction` plugin which will randomly trigger after a message is sent.
    It has different context presets that will send a topic related message.

### 2023-10-31

- Add `/blacklist` commands. These are owner only.
- Reaction copy, action reply and all interaction commands now respect the blacklist.
- Speed up koishi startup by 3 seconds.

### 2023-10-15

- Add **3** image to `/kon` interaction.

### 2023-10-08

- Fix `/snipe` errored when adding a sticker. This was a quickfix pushed after last update.
- `/sex` now has a new 7th tier with 0.2% chance.
- `/automation welcome` messages will use colored embeds, following the scheme of `/hug` and such.
- `/automation welcome` now will send the same message if a user rejoins the guild.
- Fix `/mod mute` now aborts if the target user is an admin. You cannot mute admins.
- Fix `self-mod mute` now aborts if the invoking user is an admin. You cannot mute admins.
- When clicking on `accept rules` / `claim announcements role` it will acknowledge the interaction to avoid timeout.
- Actions like `/hug` sometimes timed out thanks to Discord lagging. If that happens now a normal message will be sent.
    Since these are popular commands it happened once every few week.
- Fix `/automation reaction-copy` did not ignore reactions of bots.
- Replying to an action such as `/hug`, will work even if the message starts with a slash.
- Add **1** image to `/like` interaction.
- Add **2** image to `/kon` interaction.
- `/about field: cache` now also includes the about components.
- `/help` responses now include a close button.

### 2023-09-30

- Add `1` image to `/kon`.
- `/pocky-kiss` images have been uploaded and their creator referenced. (Self pockies excluded for now.)
- Fix the touhou character preference deleting. Before it yeeted all entries. :KoishiFail:
- Notification settings are now separated down from user common model and accessibility.
    They got their own model, plugin and tests as well.

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
