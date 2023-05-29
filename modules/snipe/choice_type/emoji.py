__all__ = ()

from hata import DATETIME_FORMAT_CODE, GUILDS, ZEROUSER, elapsed_time
from hata.ext.slash import Option
from scarletio import class_property, copy_docs

from ..cache_emoji import update_emoji_details
from ..component_translate_tables import SELECT_EMOJI_DISABLED, SELECT_EMOJI_INSIDE, SELECT_EMOJI_OUTSIDE
from ..constants import (
    BUTTON_SNIPE_ACTIONS_EMOJI, BUTTON_SNIPE_ADD_EMOJI, BUTTON_SNIPE_DETAILS_EMOJI, BUTTON_SNIPE_EDIT_EMOJI,
    BUTTON_SNIPE_REMOVE_STICKER
)
from ..embed_builder_base import create_base_embed
from ..embed_parsers import get_emoji_from_event

from .base import ChoiceTypeBase


@copy_docs(ChoiceTypeBase)
class ChoiceTypeEmoji(ChoiceTypeBase):
    __slots__ = ()
    
    @class_property
    def name(cls):
        return 'emoji'
    
    
    @class_property
    def button_actions_enabled(cls):
        return BUTTON_SNIPE_ACTIONS_EMOJI
    
    
    @class_property
    def button_details_enabled(cls):
        return BUTTON_SNIPE_DETAILS_EMOJI
    
    
    @class_property
    def button_action_add(cls):
        return BUTTON_SNIPE_ADD_EMOJI
    
    
    @class_property
    def button_action_edit(cls):
        return BUTTON_SNIPE_EDIT_EMOJI
    
    
    @class_property
    def button_action_remove(cls):
        return BUTTON_SNIPE_REMOVE_STICKER
    
    
    @class_property
    def select_table_disabled(cls):
        return SELECT_EMOJI_DISABLED
    
    
    @class_property
    def select_table_inside(cls):
        return SELECT_EMOJI_INSIDE
    
    
    @class_property
    def select_table_outside(cls):
        return SELECT_EMOJI_OUTSIDE
    
    
    @classmethod
    def _create_emoji_option_value(cls, entity):
        """
        Creates an emoji option value. Helper method of ``.select_option_builder``.
        
        Parameters
        ----------
        entity : ``Emoji``
            The emoji to build the option value for.
        
        Returns
        -------
        value : `str`
        """
        if entity.is_unicode_emoji():
            emoji_id = 0
            name = entity.unicode
            animated = ''
        else:
            emoji_id = entity.id
            name = entity.name
            animated = format(entity.animated, 'd')
        
        return cls._create_select_option_value(emoji_id, name, animated)
    
    
    @classmethod
    @copy_docs(ChoiceTypeBase.select_option_builder)
    def select_option_builder(cls, entity):
        return Option(cls._create_emoji_option_value(entity), entity.name, entity)
    
    
    @classmethod
    @copy_docs(ChoiceTypeBase.update_entity_details)
    async def update_entity_details(cls, entity, client):
        await update_emoji_details(client, entity)
    
    
    @classmethod
    @copy_docs(ChoiceTypeBase.build_embed_detailed)
    def build_embed_detailed(cls, entity):
        embed = create_base_embed(entity, f'{cls.name.capitalize()} details')
        
        if entity.is_unicode_emoji():
            embed.add_field(
                'Unicode',
                (
                    f'```\n'
                    f'{entity.unicode}\n'
                    f'```'
                ),
                inline = True,
            )
        
        else:
            embed.add_field(
                'Animated',
                (
                    f'```\n'
                    f'{"true" if entity.animated else "false"}\n'
                    f'```'
                ),
                inline = True,
            )
            
            created_at = entity.created_at
            
            embed.add_field(
                'Created at',
                (
                    f'```\n'
                    f'{created_at:{DATETIME_FORMAT_CODE}} | {elapsed_time(created_at)} ago\n'
                    f'```'
                ),
            )
            
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
            
            roles = entity.roles
            if roles is None:
                roles_description = 'N/A'
            
            else:
                roles_description_parts = []
                
                limit = len(roles)
                if limit > 10:
                    truncated_count = limit - 10
                    limit = 10
                else:
                    truncated_count = 0
                
                index = 0
                while True:
                    role = roles[index]
                    roles_description_parts.append(role.name)
                    
                    index += 1
                    if index == limit:
                        break
                    
                    roles_description_parts.append('\n')
                    continue
                
                if truncated_count:
                    roles_description_parts.append('\n\n... ')
                    roles_description_parts.append(str(truncated_count))
                    roles_description_parts.append(' truncated...')
                
                roles_description = ''.join(roles_description_parts)
                roles_description_parts = None
            
            
            embed.add_field(
                'Roles',
                (
                    f'```\n'
                    f'{roles_description}\n'
                    f'```'
                ),
            )
            
            embed.add_field(
                'Available',
                (
                    f'```\n'
                    f'{"true" if entity.available else "false"}\n'
                    f'```'
                ),
                inline = True,
            ).add_field(
                'Managed',
                (
                    f'```\n'
                    f'{"true" if entity.managed else "false"}\n'
                    f'```'
                ),
                inline = True,
            )
        
        return embed
    
    
    @classmethod
    @copy_docs(ChoiceTypeBase.parse_and_get_entity_id_and_entity)
    async def parse_and_get_entity_id_and_entity(cls, client, event):
        emoji = get_emoji_from_event(event)
        if emoji is None:
            emoji_id = 0
        else:
            emoji_id = emoji.id
        
        return emoji_id, emoji
