# Automation - Chat interactions

Contains logic and interactions for automated chat based interactions.

If a message satisfies basic conditions it has a chance for a chat interaction executed on it.
Note that only up to one interaction can be executed on each message making the maximal trigger chance just 4%.


Possible interactions:

- Check when the client is mentioned in a message. If it is mirror the mentions and send it as a message.
- Check for `omae wwe maou` content and send a `NANI?` in the chat.
- Check for `owo` like content and send an other `OwO` in the chat.
- Check for `roblox` related content and send an image: *only kids play roblox*.
