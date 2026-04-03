import vampytest
from hata import Emoji, InteractionForm, SoundboardSound, Sticker, TextInputStyle, create_label, create_text_input

from ..component_building import build_remove_form
from ..entity_packing import pack_entity


def _iter_options():
    guild_id_0 = 202511030050
    
    emoji_id_0 = 202511030051
    sticker_id_0 = 202511030052
    soundboard_sound_id_0 = 202511030053
    
    emoji_0 = Emoji.precreate(
        emoji_id_0,
        name = 'satori',
        guild_id = guild_id_0,
        role_ids = [guild_id_0],
    )
    
    sticker_0 = Sticker.precreate(
        sticker_id_0,
        name = 'kasha',
        guild_id = guild_id_0,
        tags = ['orin'],
        description = 'Carting to hell.',
    )
    
    soundboard_sound_0 = SoundboardSound.precreate(
        soundboard_sound_id_0,
        name = 'yama',
        guild_id = guild_id_0,
        emoji = emoji_0,
        volume = 0.5,
    )
    
    yield (
        emoji_0,
        [],
        InteractionForm(
            f'Remove emoji: {emoji_0.name!s}',
            [
                create_label(
                    'Reason',
                    'Additional reason that will show up in the guild\'s audit logs.',
                    create_text_input(
                        custom_id = 'reason',
                        min_length = 0,
                        max_length = 400,
                        style = TextInputStyle.paragraph,
                    ),
                ),
            ],
            f'snipe.remove.{pack_entity(emoji_0)}',
        ),
    )
    
    yield (
        sticker_0,
        [],
        InteractionForm(
            f'Remove sticker: {sticker_0.name!s}',
            [
                create_label(
                    'Reason',
                    'Additional reason that will show up in the guild\'s audit logs.',
                    create_text_input(
                        custom_id = 'reason',
                        min_length = 0,
                        max_length = 400,
                        style = TextInputStyle.paragraph,
                    ),
                ),
            ],
            f'snipe.remove.{pack_entity(sticker_0)}',
        ),
    )
    
    yield (
        soundboard_sound_0,
        [],
        InteractionForm(
            f'Remove sound: {soundboard_sound_0.name!s}',
            [
                create_label(
                    'Reason',
                    'Additional reason that will show up in the guild\'s audit logs.',
                    create_text_input(
                        custom_id = 'reason',
                        min_length = 0,
                        max_length = 400,
                        style = TextInputStyle.paragraph,
                    ),
                ),
            ],
            f'snipe.remove.{pack_entity(soundboard_sound_0)}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_remove_form(entity, entity_cache):
    """
    Tests whether ``build_remove_form`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user removing the entity.
    
    entity_type : ``type<Emoji | Sticker | SoundboardSound>``
        The type of the entity.
    
    entity : ``None | Sticker | SoundboardSound``
        Entity to use as default.
    
    guild_id : `int`
        The local guild's identifier.
    
    entity_cache : `list<object>`
        Additional entities to keep cached.
    
    Returns
    -------
    interaction_form : ``InteractionForm``
    """
    output = build_remove_form(entity)
    vampytest.assert_instance(output, InteractionForm)
    return output
