# Automation - Commands

Contains control commands for other automation features.

# Commands

- `/automation`
    - `list-all`
    - `disable-all`
    - `community-message-moderation`
        - `state (state : Choice<str>)`
        - `availability-duration (hours : int = 0, minutes : int = 0, seconds : int = 0)`
        - `down-vote-emoji (emoji : null | str = null)`
        - `up-vote-emoji (emoji : null | str = null)`
        - `vote-threshold (threshold : int<min = 2, max = 20> = 0)`
        - `log-state (state : Choice<str>)`
        - `log-channel (channel : null | Channel<channel_types = [0, 5]> = null)`
    - `log-emoji` (emoji create / modify / delete)
        - `enable (channel : null | Channel<channel_types = [0, 5]> = null)`
        - `disable`
    - `log-mention` (message create / edit)
        - `enable (channel : null | Channel<channel_types = [0, 5]> = null)`
        - `disable`
    - `log-sticker` (sticker create / modify / delete)
        - `enable (channel : null | Channel<channel_types = [0, 5]> = null)`
        - `disable`
    - `log-user` (user join / leave)
        - `enable (channel : null | Channel<channel_types = [0, 5]> = null)`
        - `disable`
    - `reaction-copy`
        - `enable`
        - `disable`
        - `about`
        - `list-channels`
    - `touhou-feed`
        - `enable`
        - `disable`
        - `about`
        - `list-channels (page : int<min = 1, max = 100> = 1)`
    - `welcome`
        - `enable (channel : null | Channel<channel_types = [0, 5]> = null)`
        - `disable`
        - `reply-buttons (value : bool)`
        - `style (value : Choice<str>)`


Additional commands limited for a few guilds (KW, KU and OD):

- `/automation`
  - `log-satori` 
    - `enable (channel : Channel<channel_types = [4]>)`
    - `disable`
    - `auto-start (value : bool)`
