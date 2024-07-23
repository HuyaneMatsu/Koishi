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
    - `farewell`
        - `channel (channel : null | Channel<channel_types = [0, 5]> = null)`
        - `state (state : Choice<str>)`
        - `style (value : Choice<str>)`
    - `log-emoji` (emoji create / modify / delete)
        - `channel (channel : null | Channel<channel_types = [0, 5]> = null)`
        - `state (state : Choice<str>)`
    - `log-mention` (message create / edit)
        - `channel (channel : null | Channel<channel_types = [0, 5]> = null)`
        - `state (state : Choice<str>)`
    - `log-sticker` (sticker create / modify / delete)
        - `channel (channel : null | Channel<channel_types = [0, 5]> = null)`
        - `state (state : Choice<str>)`
    - `log-user` (user join / leave)
        - `channel (channel : null | Channel<channel_types = [0, 5]> = null)`
        - `state (state : Choice<str>)`
    - `reaction-copy`
        - `about`
        - `list-channels`
        - `parse (name-unicode : bool, topic-custom : bool, topic-unicode : bool)`
        - `state (state : Choice<str>)`
    - `touhou-feed`
        - `about`
        - `list-channels (page : int<min = 1, max = 100> = 1)`
        - `state (state : Choice<str>)`
    - `welcome`
        - `channel (channel : null | Channel<channel_types = [0, 5]> = null)`
        - `reply-buttons (state : Choice<str>)`
        - `state (state : Choice<str>)`
        - `style (value : Choice<str>)`


Additional commands limited for a few guilds (KW, KU and OD):

- `/automation`
    - `log-satori` 
        - `channel (channel : Channel<channel_types = [4]>)`
        - `state (state : Choice<str>)`
        - `auto-start (state : Choice<str>)`
