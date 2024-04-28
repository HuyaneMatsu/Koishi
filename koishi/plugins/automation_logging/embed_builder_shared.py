__all__ = ()

from datetime import datetime as DateTime
from hata import DATETIME_FORMAT_CODE, ROLES, ZEROUSER


def get_role_name(role_id):
    """
    Gets the role's name for the given identifier.
    
    Parameters
    ----------
    role_id : `int`
        The role's identifier.
    
    Returns
    -------
    role_name : `str`
    """
    try:
        role = ROLES[role_id]
    except KeyError:
        role_name = str(role_id)
    else:
        role_name = role.name
    
    return role_name


def get_role_ids_repr(role_ids, truncate, truncate_at):
    """
    Gets representation for the given role identifiers.
    
    Parameters
    ----------
    role_ids : `None`, `tuple` of `int`
        The roles' identifiers.
    truncate : `bool`
        Whether the amount of roles should be truncated.
    truncate_at : `int`
        The maximal amount of roles to show. Must be positive.
    
    Returns
    -------
    representation : `str`
    """
    repr_parts = []
    
    if (role_ids is None):
        repr_parts.append('null')
    
    else:
        if truncate:
            truncated = len(role_ids) - truncate_at
            if truncated < 0:
                truncated = 0
            else:
                if truncate_at > 0:
                    role_ids = role_ids[:truncate_at]
        else:
            truncated = 0
        
        length = len(role_ids)
        if length:
            index = 0
            while True:
                role_id = role_ids[index]
                repr_parts.append(get_role_name(role_id))
                
                index += 1
                if index == length:
                    break
                
                repr_parts.append(', ')
                continue
        
        if truncated:
            repr_parts.append(', ')
            repr_parts.append(str(truncated))
            repr_parts.append(' truncated ...\n')
    
    return ''.join(repr_parts)


def get_role_ids_repr_defaulted(role_ids):
    """
    Gets representation for the given role identifiers. Calls `get_role_ids_repr` with some default values.
    
    Parameters
    ----------
    role_ids : `None`, `tuple` of `int`
        The roles' identifiers.
    
    Returns
    -------
    representation : `str`
    """
    return get_role_ids_repr(role_ids, True, 10)


def get_bool_repr(value):
    """
    Gets the representation of the given boolean value.
    
    Parameters
    ----------
    value : `bool`
        The boolean value.
    
    Returns
    -------
    representation : `str`
    """
    return 'true' if value else 'false'


def get_preinstanced_repr(value):
    """
    Gets the representation of the given preinstanced value.
    
    Parameters
    ----------
    value : ``PreinstancedBase``
        Preinstanced value.
    
    Returns
    -------
    representation : `str`
    """
    return f'{value.name} ~ {value.value!r}'


def get_nullable_container_repr(value):
    """
    Gets the representation of the given nullable container.
    
    Parameters
    ----------
    value : `None`, `iterable` of `object`
        The container to get its representation of.
    
    Returns
    -------
    representation : `str`
    """
    return 'null' if value is None else ', '.join([repr(element) for element in value])


def get_nullable_string_repr(value):
    """
    Gets the representation of a nullable string.
    
    Parameters
    ----------
    value : `None`, `str`
        The nullable string to get its representation of.
    
    Returns
    -------
    representation : `str`
    """
    return 'null' if value is None else value


def get_flags_repr(value):
    """
    Gets the representation of a the flags value.
    
    Parameters
    ----------
    value : ``FlagBase``
        Flags to get their representation of.
    
    Returns
    -------
    representation : `str`
    """
    return 'null' if not value else ', '.join([flag_name.replace('_', ' ') for flag_name in value])


def get_icon_repr(value):
    """
    Gets the representation of an icon value.
    
    Parameters
    ----------
    value : `None`, ``Icon``
        Icon to get their representation of.
    
    Returns
    -------
    representation : `str`
    """
    return 'null' if (value is None) or (not value) else value.as_base_16_hash


def get_date_time_repr(value):
    """
    Gets the representation of a date time value.
    
    Parameters
    ----------
    value : `DateTime`
        Date time to get their representation of.
    
    Returns
    -------
    representation : `str`
    """
    return 'null' if value is None else format(value, DATETIME_FORMAT_CODE)


def add_modified_string_field(embed, name, old_value, new_value):
    """
    Adds a modification string fields to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    name : `str`
        the field's name.
    old_value : `str`
        The old value to render.
    new_value : `str`
        The new value to render.
    
    Returns
    -------
    embed : ``Embed``
    """
    return embed.add_field(
        name,
        (
            f'```\n'
            f'{old_value} -> {new_value}\n'
            f'```'
        )
    )


def try_get_modified_difference(entity, old_attributes, attribute_name):
    """
    Try to gets the field by name from the old attributes. If present, returns it with the entity's.
    
    Parameters
    ----------
    entity : `object`
        The entity in context.
    old_attributes : `dict` of (`str`, `object`) items
        The entity's old attributes that have been edited.
    attribute_name : `str`
        The attribute's name.
    
    Returns
    -------
    difference : `None`, `tuple` (`object`, `object`)
        The old and new values if applicable.
    """
    try:
        old_value = old_attributes[attribute_name]
    except KeyError:
        return None
    
    return old_value, getattr(entity, attribute_name)


def _maybe_add_difference_field(embed, entity, old_attributes, attribute_name, pretty_name, converter):
    """
    Adds difference field if the value was modified.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    entity : `object`
        The entity in context.
    old_attributes : `dict` of (`str`, `object`) items
        The entity's old attributes that have been edited.
    attribute_name : `str`
        The attribute's name.
    pretty_name : `str`
        Pretty name to use as field name.
    converter : `None`, `FunctionType`
        Converter to get the field value's representation from its value when required.
    
    Returns
    -------
    embed : ``Embed``
    """
    difference = try_get_modified_difference(entity, old_attributes, attribute_name)
    if (difference is not None):
        old_value, new_value = difference
        
        if (converter is not None):
            old_value = converter(old_value)
            new_value = converter(new_value)
        
        embed = add_modified_string_field(
            embed,
            pretty_name,
            old_value,
            new_value,
        )
    return embed


def maybe_add_modified_string_field(embed, entity, old_attributes, attribute_name, pretty_name):
    """
    Adds modified string field into the given embed if the value was modified.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    entity : `object`
        The entity in context.
    old_attributes : `dict` of (`str`, `object`) items
        The entity's old attributes that have been edited.
    attribute_name : `str`
        The attribute's name.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    return _maybe_add_difference_field(embed, entity, old_attributes, attribute_name, pretty_name, None)


def maybe_add_modified_bool_field(embed, entity, old_attributes, attribute_name, pretty_name):
    """
    Adds modified boolean field into the given embed if the value was modified.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    entity : `object`
        The entity in context.
    old_attributes : `dict` of (`str`, `object`) items
        The entity's old attributes that have been edited.
    attribute_name : `str`
        The attribute's name.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    return _maybe_add_difference_field(embed, entity, old_attributes, attribute_name, pretty_name, get_bool_repr)


def maybe_add_modified_nullable_string_field(embed, entity, old_attributes, attribute_name, pretty_name):
    """
    Adds modified nullable string field into the given embed if the value was modified.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    entity : `object`
        The entity in context.
    old_attributes : `dict` of (`str`, `object`) items
        The entity's old attributes that have been edited.
    attribute_name : `str`
        The attribute's name.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    return _maybe_add_difference_field(
        embed,
        entity,
        old_attributes,
        attribute_name,
        pretty_name,
        get_nullable_string_repr,
    )


def maybe_add_modified_nullable_container_field(embed, entity, old_attributes, attribute_name, pretty_name):
    """
    Adds modified nullable container into the given embed if the value was modified.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    entity : `object`
        The entity in context.
    old_attributes : `dict` of (`str`, `object`) items
        The entity's old attributes that have been edited.
    attribute_name : `str`
        The attribute's name.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    return _maybe_add_difference_field(
        embed,
        entity,
        old_attributes,
        attribute_name,
        pretty_name,
        get_nullable_container_repr,
    )


def maybe_add_modified_role_ids_field(embed, entity, old_attributes, attribute_name, pretty_name):
    """
    Adds modified `role_ids` field into the given embed if the value was modified.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    entity : `object`
        The entity in context.
    old_attributes : `dict` of (`str`, `object`) items
        The entity's old attributes that have been edited.
    attribute_name : `str`
        The attribute's name.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    return _maybe_add_difference_field(
        embed,
        entity,
        old_attributes,
        attribute_name,
        pretty_name,
        get_role_ids_repr_defaulted,
    )


def maybe_add_modified_role_ids_difference_field(embed, entity, old_attributes, attribute_name, pretty_name):
    """
    Adds a modified `role_ids` difference field into the given embed if the value was modified.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    entity : `object`
        The entity in context.
    old_attributes : `dict` of (`str`, `object`) items
        The entity's old attributes that have been edited.
    attribute_name : `str`
        The attribute's name.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    difference = try_get_modified_difference(entity, old_attributes, attribute_name)
    if (difference is not None):
        old_value, new_value = difference
        
        old_role_ids = set()
        if old_value is not None:
            old_role_ids.update(old_value)
        
        new_role_ids = set()
        if new_value is not None:
            new_role_ids.update(new_value)
        
        removed_role_ids = old_role_ids - new_role_ids
        added_role_ids = new_role_ids - old_role_ids
        
        parts = ['```diff\n']
        for removed_role_id in removed_role_ids:
            parts.append('- ')
            parts.append(get_role_name(removed_role_id))
            parts.append('\n')
        
        for added_role_id in added_role_ids:
            parts.append('+ ')
            parts.append(get_role_name(added_role_id))
            parts.append('\n')
        
        parts.append('```')
        
        embed.add_field(pretty_name, ''.join(parts))
    
    return embed


def maybe_add_modified_flags_field(embed, entity, old_attributes, attribute_name, pretty_name):
    """
    Adds modified `flags` field into the given embed if the value was modified.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    entity : `object`
        The entity in context.
    old_attributes : `dict` of (`str`, `object`) items
        The entity's old attributes that have been edited.
    attribute_name : `str`
        The attribute's name.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    return _maybe_add_difference_field(
        embed,
        entity,
        old_attributes,
        attribute_name,
        pretty_name,
        get_flags_repr,
    )


def maybe_add_modified_icon_field(embed, entity, old_attributes, attribute_name, pretty_name):
    """
    Adds modified `icon` field into the given embed if the value was modified.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    entity : `object`
        The entity in context.
    old_attributes : `dict` of (`str`, `object`) items
        The entity's old attributes that have been edited.
    attribute_name : `str`
        The attribute's name.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    return _maybe_add_difference_field(
        embed,
        entity,
        old_attributes,
        attribute_name,
        pretty_name,
        get_icon_repr,
    )


def maybe_add_modified_date_time_field(embed, entity, old_attributes, attribute_name, pretty_name):
    """
    Adds modified `date_time` field into the given embed if the value was modified.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    entity : `object`
        The entity in context.
    old_attributes : `dict` of (`str`, `object`) items
        The entity's old attributes that have been edited.
    attribute_name : `str`
        The attribute's name.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    return _maybe_add_difference_field(
        embed,
        entity,
        old_attributes,
        attribute_name,
        pretty_name,
        get_date_time_repr,
    )


def add_string_field(embed, value, pretty_name):
    """
    Adds a string field into the given contain.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    value : `str`
        The value to add.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    return embed.add_field(
        pretty_name,
        (
            f'```\n'
            f'{value}\n'
            f'```'
        ),
    )


def add_bool_field(embed, value, pretty_name):
    """
    Adds a boolean field into the given contain.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    value : `bool`
        The value to add.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    return add_string_field(embed, get_bool_repr(value), pretty_name)


def add_preinstanced_field(embed, value, pretty_name):
    """
    Adds a preinstanced field into the given contain.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    value : ``PreinstancedBase`
        The value to add.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    return add_string_field(embed, get_preinstanced_repr(value), pretty_name)


def add_nullable_container_field(embed, value, pretty_name):
    """
    Adds an iterable container field into the given contain.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    value : `None`, `iterable` of `object`
        The value to add.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    return add_string_field(embed, get_nullable_container_repr(value), pretty_name)


def add_nullable_string_field(embed, value, pretty_name):
    """
    Adds a nullable string field into the given contain.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    value : `None`, `str`
        The value to add.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    return add_string_field(embed, get_nullable_string_repr(value), pretty_name)


def add_role_ids_field(embed, role_ids, pretty_name):
    """
    Adds a `role_ids` field into the given contain.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    role_ids : `None`, `tuple` of `int`
        The value to add.
    pretty_name : `str`
        Pretty name to use as field name.
    
    Returns
    -------
    embed : ``Embed``
    """
    return add_string_field(embed, get_role_ids_repr_defaulted(role_ids), pretty_name)


def add_expression_context_fields_to(embed, entity):
    """
    Adds the context fields into the given embed.
    
    Context fields include author & footer.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    entity : ``Emoji``, ``Sticker``, ``SoundboardSound``
        The entity to pull the fields from.
    
    Returns
    -------
    embed :`` Embed``
    """
    created_at_string = format(entity.created_at, DATETIME_FORMAT_CODE)
    user = entity.user
    if user is ZEROUSER:
        author_text = created_at_string
        icon_url = None
    else:
        author_text = f'{user.full_name} | {created_at_string}'
        icon_url = user.avatar_url
    
    embed.add_author(author_text, icon_url)
    embed.add_footer(format(DateTime.utcnow(), DATETIME_FORMAT_CODE))
    
    return embed
