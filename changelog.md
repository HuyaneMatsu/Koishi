### 2024-12-14

- How balance is handled is completely rewritten; hoping no new bugs were made.
- `/gift` is now affected by `accessibility`.
- `/award` is now affected by `accessibility`.
- `/gift` now picks up nick names.
- `/award` now picks up nick names.
- Add new `/accessibility notification-settings change notification_type: gift` option.
- `/daily` now respects the user's nick name.
- When playing `/21` in single player player mode now you are playing actually against the bot.
    The bot is required to have enough hearts & its balance also changes depending on the outcome.
- `/daily` does not mix `love` and `hearts` to have it consistent. Perhaps related to a future update?
- Users without a balance entry in the database can also be retrieve random hearts randomly by using a command.
- `/daily` is now available when user installed.
- Rename `/heart-shop` to `/shop`.

### 2024-12-04

- Fix commands using `booru` were not working (since last update).
- Fix a few new edge cases popping up in `auotmation touhou-feed` due to recent changes.
- Add new `/accessibility notification-settings change notification_type: vote` option.
- Voting on Koishi on `top.gg` now triggers a notification.
- `top.gg` vote rewards now scale with roles.
- `/daily` now gives higher reward if a user is a booster.
- Update `/daily` message to include how much streak the user lost.
- Rewards are now dynamic.
- `/hearts` rewritten to support dynamic reward rendering.
- Add `extrenal_events` plugin.

### 2024-11-21

- Fix `/oj card` `Red & Blue` had its asset incorrectly assigned.
- Fix `/oj character` `Mimyuu (Jailbird)` had its hyper incorrectly linked.
- Fix `/oj character` `Mimyuu` did not have both of its hypers linked.
- Fix `gateway timeout` were propagated while acknowledging in `/daily`.
- Fix `internal server error` were propagated in `/automation log satori` presence logging.
- Fix `/mod mute` now handles when the user leaves while the action is performed.
- Fix `auotmation touhou-feed` not updating when: a role is deleted, a role is modified, a role is given / taken.
- Add `self-target` rendering to `upload-action-assets` cli command.
- Update `Krila` -> `Krilalaris` in `/OJ card` `Bloodlust` & `/OJ character` `Krilalaris`.
- Add new `Claim poll role` button into `/rules` (support guild only).
- Add `Alice` bot.
- `/lap-sleep` command now uses `lap_sleep` tag in its images' names (from `lap-sleep`).
- Add **1** images to `/kon`.
- Add **9** images to `/hug`.
- Add **2** images to `/kiss`.
- Add **2** images to `/lap-sleep`.

### 2024-10-27

- Fix `/automation log-satori` activity timestamp difference rendered incorrectly.
- Fix `/automation log-satori` emoji difference rendered incorrectly.
- Fix `/automation log-satori` not separating added activities enough from entries under them.
- `/automation log-satori` now correctly shows custom & hanging activities.
- Fix `/snipe` did not update `embed.footer` correctly when switching between detailed entity views.
- Fix `automation touhou-feed list-channels` failed if the channel had too much (around 40+) characters tagged.
- `/vocaloid` is now available when user installed.
- Add more touhou character nicks for better matching.
- Add **6** images to `/hug`.
- Add **22** images to `/stare`.
- Fix `/automation farewell` was not working since localization support was added.

### 2024-10-13

- Add `Vivit` touhou character.
- Add `Prismriver Layla` touhou character.
- Add `Mishaguji` touhou character.
- Add `Okazaki Yumemi` touhou character.
- Add `Miyadeguchi Mizuchi` touhou character.
- Add `Genjii` touhou character.
- Add `Hourai` touhou character.
- Add `Shanghai` touhou character.
- Add `Yumeko` touhou character.
- Add `Konpaku Youki` touhou character.
- Add `Tokiko` touhou character.
- Add `Label` touhou character.
- Add `Jacket` touhou character.
- Add `Goliath` touhou character.
- Add `Haruru` touhou character.
- Add `Tsubame` touhou character.
- Add `Akiyo` touhou character.
- Add `Satowa` touhou character.
- Add `Yorumi` touhou character.
- Add `Tomomi` touhou character.
- Add `Unnamed Exotic Girl - 20000-hit Girl` touhou character (really could not find how it is called).
- Add `Unnamed Exotic Girl - Cleaning Maid` touhou character (really could not find how it is called).
- Remove `embed.author` in `/ds`. The existence of `message.interaction` field makes it duplicate.
- Add `convert_action_asset_formats` cli command to help with registering new images.
- Add `upload-action-assets` cli command to help with uploading new images.
- Add many touhou character nicks for better matching.
- `/pocky (self)` images now have their own `pocky_self` tag.
- `/like` images now use a shared `like` tag in their names.
- Add **14** images to `/meme`.
- Add **20** images to `/hug`.
- Add **10** images to `/kiss`.
- Add **5** images to `/pat`.
- Add **2** images to `/fluff`.
- Add **377** images to `/stare` (74 is so nue).
- Add **1** images to `/pocky-kiss`.
- Add **2** images to `/lick`.
- `/sex` now silences when discord is derping. Also tries to respond with a normal message if Discord is slow.
- `/sex` now has rate limit per `user_id` as well (teehee).
- Fix `/sex` rate limit was not updated on repeated uses.

### 2024-09-26

- `/todo list` now allows filtering.
- `/todo list` now allows switching between pages.
- Fix `/safebooru` returning incorrect content type headers when auto completing. (So just a workaround.)
- Fix `Game21JoinRunner` not updating the message on timeout.
- `/ask` is now a global command & available when user installed.
- `/oj` command's dataset updated.
- `/oj` is available when user installed.
- `style-text` and `/style-text` commands are available when user installed.
- `escape` now available when user installed.
- Add `/peg` command.

### 2024-09-15

- Fix `Teireida Mai`'s nick shadowing `Mai` in `/touhou-character`.
- Fix `Game21PlayerRunner` tried to add interaction waiter after failed to create the message.
- Fix `/lucky-spin` infinite heart glitch, teehee.
- Fix `format-time` applying `timezone-offset` the wrong way around.
- Fix `/21` multi player timeout not editing the message.
- Rebrand `CursedSakuya` to `ToyKoishi`.
- `/format-time absolute` now has new `time-zone` and `daylight-saving-time` parameters.
- Fix `ZeroDivisionError` in event payload analyzer. (This is a new discord feature testing tool actually.)
- Fix `/heart-shop roles` used the user's global avatar instead of the local one.
- Fix action commands (such as `/hug`) used black color if a user had no color (instead of no color).
- Add `/mod edit-ban-reason` command.
- `/daily` now shows the waifus on cooldown too. Also shows their cooldown too.
- Fix `/daily` telling someone is not a waifu if they are on cooldown.
- Ignore a random permission error caused when responding to an action command like `/hug`.
    When this happen the client will try to default back to sending a normal message.
    Tho that would fail on permission check probably.
- `anilist` commands are now available when user installed.
    This includes: `/show-anime`, `/find-anime`, `/show-character`, `/find-character`, `/show-manga`, `/find-manga`.
- Fix `/trivia` removed embed author on chained interactions when completed. (Caused by a Discord change)
- Fix `escape` now escaping grave character. (Forgot to add it back after fixing `escape` previously.)
- `/minesweeper` now uses `:skull:` emoji when used through orin.
- Fix `/ds` underflow in yukari skill calculation. 
- Fix `/emoji` commands not showing up (support guild only).
- Fix koishi news are not auto crossposted.
- `/plugins list-all` and `/plugins list-per-client` merged into one `/plugins list` command. (Owner only)
- `/plugins list` is now paged. 
- Add new `/stare` command with **70** image.
- Add **3** image to `/pat`.
- Add **13** image to `/hug`.
- Add **5** image to `/fluff`.
- Add **1** image to `/kon`.

### 2024-08-20

- `/gift` is now available when user installed.
- `/touhou_calendar` is now available when user installed.
- `/touhou_character` is now available when user installed.
- All action commands (like `/handhold`) are available when user installed.
- Fix an error in `/21` multiplayer timeout not updating the embed.
- `image_refresh` now handles the case when the message is deleted.
    Apparently this edge case is pretty common scenario.
- `/kanako` now handles the case if the message is deleted on timeout.
    Apparently this edge case is pretty common scenario.
- `/minesweeper` now aborts the command if the client is affected by slowmode in the channel.
    Apparently this edge case is pretty common scenario. It is an api bug too.
- Add `/user banner` command.
- Add `Gengetsu` touhou character.
- Add `Mugetsu` touhou character.
- Add `Mai` touhou character.
- Add `Yuki` touhou character.
- Add `Sariel` touhou character.
- Add `Kurumi` touhou character.
- Add `Meira` touhou character.
- Add `Louise` touhou character.
- Add `Elis` touhou character.
- Add `Rika` touhou character.
- Add `Sara` touhou character.
- Add `Kikuri` touhou character.
- Add `Shingyoku` touhou character.
- Add `Orange` touhou character.
- Add `Yuugen Magan` touhou character.
- Add `Ruukoto` touhou character.
- Add `Noroiko` touhou character.
- Add `Rengeteki` touhou character.
- Add `Matenshi` touhou character.
- Add `Wayousei` touhou character.
- Add `Ayana` touhou character.
- Add `Kokuu Haruto` touhou character.
- Add **5** image to `/kon`.
- Add **5** image to `/kiss`.
- Add **1** image to `/pat`.
- Add **3** image to `/hug`.
- Add **1** image to `/lick`.

### 2024-08-07

- `/calc` is now available when user installed.
- Allow expressions in `/gift` command for `amount` parameter.
- `/format-time` is now available when user installed.
- `/hearts` is now available when user installed.
- `/21` is now available when user installed. Also available in private channels too.
- `/21` multiplayer now uses invoking user only messages instead of private messages.
- `/21` multiplayer now also refunds if everyone loses.
- Fix unsupported operand in `/lucky-spin`. (since 2024-07-23)

### 2024-07-23

- Fix `/heart-shop roles` rejected if you had the same amount as required.
- Fix `/lucky-spin` float precision issues causing heart loss.
- Fix `/9ball` displayed who invoked the command in both `embed.author` and in the command headers as well.
- Fix `bozosort` now should handle listings with `as` keywords correctly.
- Fix `&execute` removed empty lines from input causing unexpected behaviors when working with multi-line strings.
- Fix `embed_image_refresh` now does not force update external images that the client(s) cant see.
- Add new error messages when an interaction raises.

### 2024-07-14

- Fix anilist query returned on rate limit instead of retrying.
- Fix various errors when handing date times. Couldn't compare date time with timezone without. (Since last update)
- Add new `/automation farewell` commands. Sends farewell messages when a user is removed from a guild.
    Add initial styles for: flandre, koishi, orin and yoshika.
- `/automation welcome` messages now also mention who created the image.
- Fix discord misbehaving at a few cases when `/action` responding.
- Add **3** image to `/pat`.
- Add **12** image to `/kiss`.
- Add **26** image to `/hug`.
- Add **2** image to `/pocky-kiss`.
- Add **1** image to `/feed`.
- Add **2** image to `/lap-sleep`.
- Add **1** image to `/pocky-kiss` (self).
- Add **7** image to `/like`.
- Add **1** image to `/fluff`.

### 2024-07-07

- Add `nazrin` easter egg to `/mod mute`.
- Add **6** image to `/pat`.
- Add **10** image to `/kiss`.
- Add **16** image to `/hug`.
- Add **3** image to `/pocky-kiss`.
- Add **7** image to `/feed`.
- Add **1** image to `/lap-sleep`.

### 2024-06-12

- `/ds` does not require `manage messages` permission anymore, only `use external emojis`.
- Fix `/ds` did not reset `skill` on restart.
- Fix `/ds` had `next` button inactive when finishing the last stage of a chapter.
- `/automation reaction-copy list-channels` did not sort channels without categories.
- `/automation reaction-copy list-channels` showed different output for each client.
- `/automation reaction-copy list-channels` now also shows in which channels the client(s) cannot copy the message.
- Add `/automation reaction-copy parse` command.

### 2024-05-31

- Fix `user_settings` table primary key stopped working (???). Could restore 3 / 5 affected entries.
- Add `Tsukumo Benben` touhou character.
- Add `Tsukumo Yatsuhashi` touhou character.
- Add `Kotohime` touhou character.
- Add `Asakura Rikako` touhou character.
- Add `Anaberal Kana` touhou character.
- Add `Ellen` touhou character.
- Add `Sokrates` touhou character.
- Add **34** image to `/kiss`.
- Add **38** image to `/hug`.
- Add **1** image to `/lick`.
- Add **5** image to `/lap-sleep`.
- Add **1** image to `/fluff`.
- Add **7** image to `/pat`.
- Add **1** image to `/pocky-kiss`.
- Each automation under `/automation` now has separate `enabled` and `channel` fields.
     This also changes the command structure.

### 2024-05-21

- Fix `/action` suggestion cases where `source == target` (Now they can suggest the same character as expected).
- Action commands such as `/hug` now have reduced chance to select a character for the other user(s) that you
    preferred yourself.
- `cosplay` is now a new action tag, so `tsukasa` + `ran` kons are now separated to `kon` + `tsukasa`
    and `cosplay` + `tsukasa` + `ran`. In short tsukasa cosplaying as ran wont count as ran anymore!!
- Add **4** image to `/kiss`.
- Add **6** image to `/hug`.
- Add **2** image to `/feed`.
- Add **1** image to `/lick`.
- `/automation welcome` now instead of removing the components disables them.

### 2024-05-14

- Add new `/lap-sleep` interaction with **18** image.
- Add **1** image to `/lick`.
- Add **3** image to `/hug`.
- Add **2** image to `/like`.
- Add **5** image to `/kiss`.
- Make the text on `orin-body-collecting` more readable.
- Fix Cursed Sakuya's headers.
- Orin joins the club.
- Add new hidden `/action` command. You have to user install a bot to use it.
- Fix a bug in action commands such as `/hug` that reverse sorted images by match rate producing wrong results
    if many images were matched partially.

### 2024-05-10

- Moving message now wont fail on empty messages (they are ignored).
- Moving message now also moves polls.
- Action commands such as `/hug` now also attaches who created the image if known. 
- Add new `generate-action-assets` cli command.
- Action commands preference system is redone to provide better output. Preferred count is also lowered to 6 (from 10).

### 2024-04-28

- Add new `link-assets` cli command.
- Add **6** image to `/like`.
- Add **9** image to `/kiss`. Also remove 1 for being too explicit.
- Add **1** image to `/pocky-kiss`.
- Add `Shinki` touhou character.
- Add **4** image to `/hug`.
- Add **1** image to `/pat`.
- Add **1** image to `/feed`.
- Add **2** image to `/kon`.
- Add **1** image to `/lick`.
- `/automation welcome reply` now will prompt an error message if the user already left.
- Fix an error in `/automation logging satori` when rendering activity type change.
- Move `/accessibility notification-settings set-notifier` to `/accessibility preference-settings set-preferred-client`.
- Add `/accessibility preference-settings show`.
- Add `/accessibility preference-settings set-preferred-image-source`.
- Action commands such as `/hug` now respect `preferred-client` when replying.
- Action commands now respect `preferred-image-source`.
- `/automation log-satori` now also logs `reaction-add` and `reaction-delete` events.

### 2024-03-31

- Add `Hakurei Miko` touhou character.
- Add `Install me!` button under `/about`.
- Fix a `snipe` bug when sniping reactions.
- Add **4** image to `/pocky-kiss` (1 was there just unused).
- Add **33** image to `/pat`.
- Add **1** image to `/like`.
- Add **26** image to `/lick`.
- Add **1** image to `/kon`.
- Add **36** image to `/kiss` (1 was there just unused).
- Add **51** image to `/hug`.
- Add **2** image to `/fluff`.
- Sort `/pocky-kiss` images alphabetically.
- Grouped image handlers how will go though every registered handler before failing.
- Sending some embeds failed.
- Koishi, Flandre, Yoshika, Cursed Sakuya now can be user installed.
- Fix Internal server error when requesting a non existing guide page.

### 2024-03-18

- Add `feed` interaction with **13** image. (Will get more in the future obviously.)
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
- Add new `/fluff` interaction with **68** image.
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
- Add new `/kon` interaction (with **41** image!!).
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
