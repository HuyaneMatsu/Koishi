<p align="center">
    <img
        width="256px" height="256px" align="center" alt="Koishi"
        src="https://raw.githubusercontent.com/HuyaneMatsu/Koishi/master/library/koishi_avatar_0000_by_ashy.png"
    />
</p>

<h1 align="center">
    <b><a href="https://github.com/HuyaneMatsu/koishi">Koishi</a></b>
</h1>

<h5 align="center">
    The bot who borrows your fishing rods and eats your shrimp fry.
</h5>

<p align="center">
    <a href="https://discord.com/oauth2/authorize?client_id=486565096164687885&scope=bot%20applications.commands">
        Invite me!
    </a>
    •
    <a href="http://discord.gg/3cH2r5d">
        Join our gang!
    </a>
</p>

Koishi is a multi functional waifu stuffed out with all the new Discord features. She got over 100 fun and utility
commands to get the people together.

To get started with Koishi, use the `/help` command, which lists all the available global commands.

<h3 align="center">
    What she does?
</h3>

Koishi excels in a variety of areas, just to mention a few highlighted features:

- Games with multiplayer support and progression saving! Examples:
  - from simple games like XoX and Minesweeper (both supporting multiplayer) to advanced games like `ds` which is
  - a fully featured clone of Dungeon Sweeper but with Touhou theme (includes progression saving) and many more!

- Economy system
  - get your daily coins with daily command or voting for the bot.
  - marry and divorce other users, make them your waifus!
  - upgrade your waifu stats by buying better stats (bragging rights) or have more slots for waifus (more harem).
  - get to the top of the `/top-list` with the biggest coin bank!

Advanced commands
- `dupe-image-filter` find and remove duplicate images in the last X days to prevent spam!
- `/snipe` for emoji hoarders who want to save those rare emojis, snipe the message and get all wanted emojis/reactions/stickers to your DMs
- `touhou-feed` Touhou image feed for text channels and forum threads with advanced options such as multiple characters, specific interval and tags.
- advanced selfbot detection
- ... And much more!


<h1></h1>

<h3 align="center">
    Global commands
</h3>

- Administration
    
    `clear` • `dupe-image-filter` • `invite-create` • `mod` • `self-mod`

- Anime
    
    `anime` • `character` • `find-anime` • `find-character` • `find-manga` • `manga`

- Actions
    
    `bite` • `blush` • `bully` • `cringe` • `cry` • `dance` • `glomp` • `handhold` • `happy` • `highfive` • `hug` •
    `kick` • `kill` • `kiss` • `lick` • `nom` • `pat` • `pocky-kiss` • `poke` • `slap` • `smile` • `smug` • `wave` • 
    `wink` • `yeet`

- Economy
    
    `daily` • `gift` • `heart-shop` • `hearts` • `top-list`

- Fun
    
    `9ball` • `ascii` • `meme` • `message-me` • `oj` • `paranoia` • `random` • `rate` • `roll` •
    `sex` • `stats` • `touhou-feed` • `trivia` • `urban` • `yuno`

- Games
    
    `21` • `ds` • `kanako` • `lucky-spin` • `minesweeper` • `xox`

-  Help
    
    `about` • `help`

-  Marriage
    
    `divorce` • `love` • `propose` • `proposals` • `waifu-info`

- Utility
    
    `calc` • `choose` • `create-activity` • `color` • `guild` • `id` •
    `ping` • `rawr` • `sticker` • `sticker-info` • `role-info` • `roles` • `snipe` •
    `snipe-emojis` • `snipe-reactions` • `snipe-stickers` • `style-text` • `user`

- Waifus
    
    `nsfwbooru` • `safebooru` • `touhou-calendar` • `touhou-character` • `touhou-feed` • `vocaloid` • `waifu-sfw` •
    `waifu-nsfw`

<h3 align="center">
    Support server only commands
</h3>

`add-to-move-group` • `all-users` • `ask` • `award` • `bozosort` • `crywolf` • `daily-event` • `delete-from` •
`delete-till` • `docs-search` • `emoji` • `events` • `extension` • `github-profile` • `heart-event` • `in-role` •
`latest-users` • `markdown` • `paste` • `raw` • `roles` • `rules` • `sticker` • `take` • `transfer` • `todo` •
`move-channel` • `move-message` • `move-messages` • `voice`


<h4>Note: All NSFW commands are only usable in NSFW channels.</h4>

<h1></h1>

<h3 align="center">
    FAQ
</h3>

#### # Prefix

Koishi doesn't have old-style chat commands, only slash (*and other application commands*)!

#### # Not in member list, but her commands are present

This can happen if Koishi does not have view-channel permission, but you have use-application-commands.

Since Koishi is added without any permissions, make sure to assign a role to her, **else she will stay invisible and
be forgotten by everyone. That will make her sad.**

*Koishi so meta!*

#### # Commands do not show up

- Koishi was invited without `applications.commands` scope.

- You don't have `use-application-commands` permission.

- The guild has 50+ bots.

- Discord client is derping, give it a restart.

#### # Required intents
- Presence Intent
  - Koishi has advanced, admin only, functionality that allows us to see how often the user changes status and presence.
  - this allows us to determine whether they are automated accounts or alts.
  - also used for some misc commands, such as `/status`

- Server Members Intent
  - to welcome a user after they join a guild.
  - to keep the cache up-to-date without extra API requests (for example command `latest-users` filters latest users from user cache).
  - when the bot joins any guild it will check if it is a bot guild (more bots than users) and if so it will leave.

- Message Content Intent
  - duplicate image filter.
  - for ping logs (who pinged who).
  - for some misc commands, like `copy-message`, `move-channel`, `move-message` etc, which copy and send a message to previously set channel based on user emoji reaction.


<h1></h1>

<h3 align="center">
    Contribution
</h3>

If you want to contribute fork the repo and create a pull request.

You have no clue about coding, but still want to contribute? Open an
[issue](https://github.com/HuyaneMatsu/Koishi/issues) with all your crazy ideas!
