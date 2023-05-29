__all__ = ()

from hata import DATETIME_FORMAT_CODE, GUILDS, StickerFormat, StickerType, ZEROUSER, elapsed_time
from hata.ext.slash import Option
from scarletio import class_property, copy_docs

from ..cache_sticker import get_sticker
from ..component_translate_tables import SELECT_STICKER_DISABLED, SELECT_STICKER_INSIDE, SELECT_STICKER_OUTSIDE
from ..constants import (
    BUTTON_SNIPE_ACTIONS_STICKER, BUTTON_SNIPE_ADD_STICKER, BUTTON_SNIPE_DETAILS_STICKER, BUTTON_SNIPE_EDIT_STICKER,
    BUTTON_SNIPE_REMOVE_STICKER
)
from ..embed_builder_base import create_base_embed
from ..embed_parsers import get_entity_id_from_event

from .base import ChoiceTypeBase


@copy_docs(ChoiceTypeBase)
class ChoiceTypeSticker(ChoiceTypeBase):
    __slots__ = ()
    
    @class_property
    def name(cls):
        return 'sticker'
    
    
    @class_property
    def button_actions_enabled(cls):
        return BUTTON_SNIPE_ACTIONS_STICKER
    
    
    @class_property
    def button_details_enabled(cls):
        return BUTTON_SNIPE_DETAILS_STICKER
    
    
    @class_property
    def button_action_add(cls):
        return BUTTON_SNIPE_ADD_STICKER
    
    
    @class_property
    def button_action_edit(cls):
        return BUTTON_SNIPE_EDIT_STICKER
    
    
    @class_property
    def button_action_remove(cls):
        return BUTTON_SNIPE_REMOVE_STICKER
    
    
    @class_property
    def select_table_disabled(cls):
        return SELECT_STICKER_DISABLED
    
    
    @class_property
    def select_table_inside(cls):
        return SELECT_STICKER_INSIDE
    
    
    @class_property
    def select_table_outside(cls):
        return SELECT_STICKER_OUTSIDE
    
    
    @classmethod
    @copy_docs(ChoiceTypeBase.select_option_builder)
    def select_option_builder(cls, entity):
        return Option(cls._create_select_option_value(entity.id, '', ''), entity.name)
    
    
    @classmethod
    @copy_docs(ChoiceTypeBase.update_entity_details)
    async def update_entity_details(cls, entity, client):
        await get_sticker(client, entity.id)


    @classmethod
    @copy_docs(ChoiceTypeBase.build_embed_detailed)
    async def build_embed_detailed(cls, entity):
        embed = create_base_embed(entity, f'{cls.name.capitalize()} details')
        
        sticker_format = entity.format
        if sticker_format is StickerFormat.apng:
            is_sticker_animated = True
        elif sticker_format is StickerFormat.lottie:
            is_sticker_animated = True
        else:
            is_sticker_animated = False
        
        embed.add_field(
            'Animated',
            (
                f'```\n'
                f'{"true" if is_sticker_animated else "false"}\n'
                f'```'
            ),
            inline = True,
        )
        
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
        
        # Row 3 | description
        
        description = entity.description
        if description is None:
            description = 'N / A'
        
        embed.add_field(
            'Description',
            (
                f'```\n'
                f'{description}\n'
                f'```'
            ),
        )
        
        # Row 4 | type | format
        
        sticker_type = entity.type
        
        embed.add_field(
            'Type',
            (
                f'```\n'
                f'{sticker_type.name}\n'
                f'```'
            ),
            inline = True,
        ).add_field(
            'Format',
            (
                f'```\n'
                f'{sticker_format.name}\n'
                f'```'
            ),
            inline = True,
        )
        
        # Row 5 | tags
        
        tags = entity.tags
        if tags is None:
            tags_listed = 'N / A'
        
        else:
            tags_listed = ', '.join(sorted(tags))
        
        embed.add_field(
            'Tags',
            (
                f'```\n'
                f'{tags_listed}\n'
                f'```'
            ),
        )
        
        if sticker_type is StickerType.standard:
            
            # Row 6 | pack id | sort value
            
            embed.add_field(
                'Pack id',
                (
                    f'```\n'
                    f'{entity.pack_id}\n'
                    f'```'
                ),
                inline = True,
            ).add_field(
                'Sort value',
                (
                    f'```\n'
                    f'{entity.sort_value}\n'
                    f'```'
                ),
                inline = True,
            )
        
        elif sticker_type is StickerType.guild:
            
            # Row 6 | creator | guild
            
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
        sticker_id = get_entity_id_from_event(event)
        if sticker_id:
            sticker = await get_sticker(client, sticker_id)
        else:
            sticker = None
        
        return sticker_id, sticker
