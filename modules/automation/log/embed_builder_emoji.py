__all__ = ()
from hata import Embed

from .embed_builder_shared import (
    add_bool_field, add_context_fields_to, add_role_ids_field, add_string_field, maybe_add_modified_bool_field,
    maybe_add_modified_role_ids_field, maybe_add_modified_string_field
)


def add_emoji_fields_to(embed, emoji):
    """
    Adds the emoji fields into the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    emoji : ``EMoji``
        The emoji to add its fields of.
    
    Returns
    -------
    embed : ``Embed``
    """
    add_string_field(embed, emoji.name, 'Name')
    add_bool_field(embed, emoji.animated, 'Animated')
    add_bool_field(embed, emoji.available, 'Available')
    add_role_ids_field(embed, emoji.role_ids, 'Allowed roles',)
    add_bool_field(embed, emoji.managed, 'Managed')
    add_bool_field(embed, emoji.require_colons, 'Require colons')
    
    return embed


def build_emoji_create_embed(emoji):
    """
    Builds a created emoji embed.
    
    Parameters
    ----------
    emoji : ``Emoji``
        The created emoji.
    
    Returns
    -------
    embed : ``Embed``
    """
    emoji_url = emoji.url
    
    embed = Embed(f'Emoji created: {emoji.name} ({emoji.id})', url = emoji_url).add_thumbnail(emoji_url)
    
    add_emoji_fields_to(embed, emoji)
    add_context_fields_to(embed, emoji)
    
    return embed


def build_emoji_edit_embed(emoji, old_attributes):
    """
    Builds an edited emoji embed.
    
    Parameters
    ----------
    emoji : ``Emoji``
        The edited emoji.
    old_attributes : `dict` of (`str`, `object`) items
        The emoji's old attributes that have been edited.
    
    Returns
    -------
    embed : ``Embed``
    """
    emoji_url = emoji.url
    
    embed = Embed(f'Emoji edited: {emoji.name} ({emoji.id})', url = emoji_url).add_thumbnail(emoji_url)
    
    add_context_fields_to(embed, emoji)
    
    maybe_add_modified_string_field(embed, emoji, old_attributes, 'name', 'Name')
    maybe_add_modified_bool_field(embed, emoji, old_attributes, 'animated', 'Animated')
    maybe_add_modified_bool_field(embed, emoji, old_attributes, 'available', 'Available')
    maybe_add_modified_role_ids_field(embed, emoji, old_attributes, 'role_ids', 'Allowed roles')
    maybe_add_modified_bool_field(embed, emoji, old_attributes, 'managed', 'Managed')
    maybe_add_modified_bool_field(embed, emoji, old_attributes, 'require_colons', 'Require colons')
    
    return embed



def build_emoji_delete_embed(emoji):
    """
    Builds a deleted emoji embed.
    
    Parameters
    ----------
    emoji : ``Emoji``
        The deleted emoji.
    
    Returns
    -------
    embed : ``Embed``
    """
    emoji_url = emoji.url
    embed = Embed(f'Emoji deleted: {emoji.name} ({emoji.id})', url = emoji_url).add_thumbnail(emoji_url)
    
    embed = add_emoji_fields_to(embed, emoji)
    
    return embed
