# Embed Image Refresh

Contains logic for refreshing message embed images.

Its a common issue at guilds with higher load that discord wont update `message.embed.image.width` and `.height`
making the image not load.
This plugin is here to fix it by editing the message with the same embed.
As weird as it sounds the image is already cached by discord when we do it, so it will just trigger a new size update.

## API

- `schedule_image_refresh(
    client : Client,
    message : Message,
    interaction_event : None | InteractionEvent = None
) : None`

    Schedules an embed image refresh.
