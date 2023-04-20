__all__ = ()

from hata import Embed, StickerFormat

from .embed_builder_shared import (
    add_bool_field, add_context_fields_to, add_nullable_container_field, add_nullable_string_field,
    add_preinstanced_field, add_string_field, maybe_add_modified_bool_field,
    maybe_add_modified_nullable_container_field, maybe_add_modified_nullable_string_field,
    maybe_add_modified_string_field
)


def add_sticker_fields_to(embed, sticker):
    """
    Adds the sticker fields into the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    sticker : ``Sticker``
        The sticker to add its fields of.
    
    Returns
    -------
    embed : ``Embed``
    """
    add_string_field(embed, sticker.name, 'Name')
    add_nullable_string_field(embed, sticker.description, 'Description')
    add_preinstanced_field(embed, sticker.format, 'Format')
    add_bool_field(embed, sticker.available, 'Available')
    add_nullable_container_field(embed, sticker.tags, 'Tags')
    
    return embed


def add_sticker_image_field(embed, sticker):
    """
    Adds sticker image field into the embed if applicable for sticker's type.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    sticker : ``Sticker``
        The sticker to add its image of.
    
    Returns
    -------
    embed : ``Embed``
    """
    sticker_format = sticker.format
    if (sticker_format is StickerFormat.png) or (sticker_format is StickerFormat.apng):
        embed.add_image(sticker.url)
    
    return embed


def build_sticker_create_embed(sticker):
    """
    Builds a created sticker embed.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The created sticker.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(f'Sticker created: {sticker.name} ({sticker.id})', url =  sticker.url)
    
    add_sticker_fields_to(embed, sticker)
    add_context_fields_to(embed, sticker)
    add_sticker_image_field(embed, sticker)
    
    return embed


def build_sticker_edit_embed(sticker, old_attributes):
    """
    Builds an edited sticker embed.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The edited sticker.
    old_attributes : `dict` of (`str`, `object`) items
        The sticker's old attributes that have been edited.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(f'Sticker edited: {sticker.name} ({sticker.id})', url =  sticker.url)
    
    add_context_fields_to(embed, sticker)
    add_sticker_image_field(embed, sticker)
    
    maybe_add_modified_string_field(embed, sticker, old_attributes, 'name', 'Name')
    maybe_add_modified_nullable_string_field(embed, sticker, old_attributes, 'description', 'Description')
    maybe_add_modified_bool_field(embed, sticker, old_attributes, 'available', 'Available')
    maybe_add_modified_nullable_container_field(embed, sticker, old_attributes, 'tags', 'Tags')
    
    return embed


def build_sticker_delete_embed(sticker):
    """
    Builds a deleted sticker embed.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The deleted sticker.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(f'Sticker deleted: {sticker.name} ({sticker.id})', url =  sticker.url)
    
    add_sticker_fields_to(embed, sticker)
    add_context_fields_to(embed, sticker)
    add_sticker_image_field(embed, sticker)
    
    return embed
