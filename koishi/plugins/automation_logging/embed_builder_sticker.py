__all__ = ()

from hata import Embed, StickerFormat

from .constants import COLOR_ADD, COLOR_DELETE, COLOR_UPDATE
from .embed_builder_shared import (
    add_bool_field, add_expression_context_fields_to, add_nullable_container_field, add_nullable_string_field,
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


def build_sticker_image_embed(sticker, color):
    """
    Builds a sticker image embed if applicable for sticker's type.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The sticker to show its image of.
    
    Returns
    -------
    embed : `None` ``Embed``
    """
    sticker_format = sticker.format
    if (sticker_format is StickerFormat.png) or (sticker_format is StickerFormat.apng):
        return Embed(color = color).add_image(sticker.url)


def with_sticker_image(embed, sticker):
    """
    Returns a list of embeds. If the `sticker`'s image can be shown, it adds an image embed to the returned embeds.
    
    Parameters
    ----------
    embed : ``Embed``
        Default embed to return.
    sticker : ``Sticker``
        The sticker to show its image of.
    
    Returns
    -------
    embeds : ``list<Embed>``
    """
    embeds = [embed]
    image_embed = build_sticker_image_embed(sticker, embed.color)
    if (image_embed is not None):
        embeds.append(image_embed)
    
    return embeds


def build_sticker_create_embeds(sticker):
    """
    Builds created sticker embeds.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The created sticker.
    
    Returns
    -------
    embeds : ``list<Embed>``
    """
    embed = Embed(
        f'Sticker created: {sticker.name} ({sticker.id})',
        color = COLOR_ADD,
        url =  sticker.url,
    )
    
    add_sticker_fields_to(embed, sticker)
    add_expression_context_fields_to(embed, sticker)
    
    return with_sticker_image(embed, sticker)


def build_sticker_update_embeds(sticker, old_attributes):
    """
    Builds updated sticker embeds.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The updated sticker.
    old_attributes : `dict<str, object>`
        The sticker's old attributes that have been updated.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        f'Sticker updated: {sticker.name} ({sticker.id})',
        color = COLOR_UPDATE,
        url =  sticker.url,
    )
    
    add_expression_context_fields_to(embed, sticker)
    
    maybe_add_modified_string_field(embed, sticker, old_attributes, 'name', 'Name')
    maybe_add_modified_nullable_string_field(embed, sticker, old_attributes, 'description', 'Description')
    maybe_add_modified_bool_field(embed, sticker, old_attributes, 'available', 'Available')
    maybe_add_modified_nullable_container_field(embed, sticker, old_attributes, 'tags', 'Tags')
    
    return with_sticker_image(embed, sticker)


def build_sticker_delete_embeds(sticker):
    """
    Builds deleted sticker embeds.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The deleted sticker.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        f'Sticker deleted: {sticker.name} ({sticker.id})',
        color = COLOR_DELETE,
        url =  sticker.url,
    )
    
    add_sticker_fields_to(embed, sticker)
    add_expression_context_fields_to(embed, sticker)
    
    return with_sticker_image(embed, sticker)
