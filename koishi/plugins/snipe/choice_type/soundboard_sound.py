__all__ = ()

from hata import DATETIME_FORMAT_CODE, GUILDS, StringSelectOption, ZEROUSER, elapsed_time
from scarletio import class_property, copy_docs

from ..cache_soundboard_sound import get_soundboard_sound, update_soundboard_sound_details
from ..component_translate_tables import (
    SELECT_SOUNDBOARD_SOUND_DISABLED, SELECT_SOUNDBOARD_SOUND_INSIDE, SELECT_SOUNDBOARD_SOUND_OUTSIDE
)
from ..constants import (
    BUTTON_SNIPE_ACTIONS_SOUNDBOARD_SOUND, BUTTON_SNIPE_ADD_SOUNDBOARD_SOUND, BUTTON_SNIPE_DETAILS_SOUNDBOARD_SOUND,
    BUTTON_SNIPE_EDIT_SOUNDBOARD_SOUND, BUTTON_SNIPE_REMOVE_SOUNDBOARD_SOUND
)
from ..embed_builder_base import create_base_embed
from ..embed_parsers import get_guild_and_entity_id_from_event

from .base import ChoiceTypeBase


@copy_docs(ChoiceTypeBase)
class ChoiceTypeSoundboardSound(ChoiceTypeBase):
    __slots__ = ()
    
    @class_property
    def name(cls):
        return 'soundboard sound'
    
    
    @class_property
    def prefix(cls):
        return 'o'
    
    
    @class_property
    def button_actions_enabled(cls):
        return BUTTON_SNIPE_ACTIONS_SOUNDBOARD_SOUND
    
    
    @class_property
    def button_details_enabled(cls):
        return BUTTON_SNIPE_DETAILS_SOUNDBOARD_SOUND
    
    
    @class_property
    def button_action_add(cls):
        return BUTTON_SNIPE_ADD_SOUNDBOARD_SOUND
    
    
    @class_property
    def button_action_edit(cls):
        return BUTTON_SNIPE_EDIT_SOUNDBOARD_SOUND
    
    
    @class_property
    def button_action_remove(cls):
        return BUTTON_SNIPE_REMOVE_SOUNDBOARD_SOUND
    
    
    @class_property
    def select_table_disabled(cls):
        return SELECT_SOUNDBOARD_SOUND_DISABLED
    
    
    @class_property
    def select_table_inside(cls):
        return SELECT_SOUNDBOARD_SOUND_INSIDE
    
    
    @class_property
    def select_table_outside(cls):
        return SELECT_SOUNDBOARD_SOUND_OUTSIDE
    
    
    @classmethod
    @copy_docs(ChoiceTypeBase.select_option_builder)
    def select_option_builder(cls, entity):
        return StringSelectOption(cls._create_select_option_value(entity.guild_id, entity.id, '', ''), entity.name)
    
    
    @classmethod
    @copy_docs(ChoiceTypeBase.update_entity_details)
    async def update_entity_details(cls, entity, client):
        await update_soundboard_sound_details(client, entity)


    @classmethod
    @copy_docs(ChoiceTypeBase.build_embed_detailed)
    def build_embed_detailed(cls, entity):
        embed = create_base_embed(entity, f'{cls.name.capitalize()} details')
        
        # Row 2 | created_at
        
        created_at = entity.created_at
        embed.add_field(
            'Created at',
            (
                f'```\n'
                f'{created_at:{DATETIME_FORMAT_CODE}} | {elapsed_time(created_at)} ago\n'
                f'```'
            ),
        )
        
        # Row 3 | volume | emoji
        
        embed.add_field(
            'Volume',
            (
                f'```\n'
                f'{entity.volume:.02f}\n'
                f'```'
            ),
            inline = True,
        )
        
        emoji = entity.emoji
        if emoji is None:
            emoji_name = 'N / A'
        else:
            emoji_name = emoji.name
        
        embed.add_field(
            'Emoji',
            (
                f'```\n'
                f'{emoji_name}\n'
                f'```'
            ),
            inline = True,
        )
        
        # Row 4 | Type
        
        if entity.is_custom_sound():
            type_name = 'custom'
        elif entity.is_default_sound():
            type_name = 'default'
        else:
            type_name = 'unknown'
        
        embed.add_field(
            'Type',
            (
                f'```\n'
                f'{type_name}\n'
                f'```'
            ),
        )
        
        
        if entity.is_custom_sound():
            
            # Row 5 | creator | guild
            
            user = entity.user
            if user is ZEROUSER:
                creator_name = 'unknown'
            else:
                creator_name = f'{user.full_name}\n{user.id}'
            
            embed.add_field(
                'Creator',
                (
                    f'```\n'
                    f'{creator_name}\n'
                    f'```'
                ),
                inline = True,
            )
            
            guild_id = entity.guild_id
            if guild_id == 0:
                guild_name = 'unknown'
            
            else:
                guild = GUILDS.get(guild_id, None)
                if guild is None:
                    guild_name = str(guild_id)
                
                else:
                    guild_name = f'{guild.name}\n{guild_id}'
            
            embed.add_field(
                'Guild',
                (
                    f'```\n'
                    f'{guild_name}\n'
                    f'```'
                ),
                inline = True,
            )
        
        return embed
    
    
    @classmethod
    @copy_docs(ChoiceTypeBase.parse_and_get_entity_id_and_entity)
    async def parse_and_get_entity_id_and_entity(cls, client, event):
        guild_id, sound_id = get_guild_and_entity_id_from_event(event)
        sound = await get_soundboard_sound(client, guild_id, sound_id)
        return sound_id, sound
    
    
    @classmethod
    @copy_docs(ChoiceTypeBase.get_file)
    async def get_file(cls, entity, client):
        async with client.http.get(entity.url) as response:
            data = await response.read()
        
        return 'sound.mp3', data
