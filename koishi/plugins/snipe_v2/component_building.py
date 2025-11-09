__all__ = ()

from itertools import islice

from hata import (
    Emoji, EntitySelectDefaultValue, EntitySelectDefaultValueType, InteractionForm, SoundboardSound, Sticker,
    StickerFormat, StringSelectOption, TextInputStyle, create_attachment_input, create_attachment_media, create_label,
    create_media_gallery, create_role_select, create_row, create_string_select, create_text_display, create_text_input
)

from .constants import (
    ACTION_ADD, ACTION_CLOSE, ACTION_DETAILS, ACTION_DM, ACTION_EDIT, ACTION_REMOVE, ACTION_REVEAL, EMOJI_ADD,
    EMOJI_CLOSE, EMOJI_DETAILS, EMOJI_DM, EMOJI_EDIT, EMOJI_REMOVE, EMOJI_REVEAL, FEATURE_FLAG_DETAILED,
    FEATURE_FLAG_DM, FEATURE_FLAG_REVEALED
)
from .content_building import (
    FORM_ROLES_DESCRIPTION_MIDDLE, get_entity_type_name, produce_description,
    produce_form_roles_component_long_description
)
from .custom_ids import (
    CUSTOM_ID_ENTITY_DESCRIPTION, CUSTOM_ID_ENTITY_EMOJI, CUSTOM_ID_ENTITY_FILE, CUSTOM_ID_ENTITY_GUILD,
    CUSTOM_ID_ENTITY_NAME, CUSTOM_ID_ENTITY_REASON, CUSTOM_ID_ENTITY_ROLES, CUSTOM_ID_ENTITY_TAGS,
    CUSTOM_ID_ENTITY_VOLUME, CUSTOM_ID_SNIPE_ACTION_BUILDER, CUSTOM_ID_SNIPE_ADD_BUILDER,
    CUSTOM_ID_SNIPE_CHOICE_BUILDER, CUSTOM_ID_SNIPE_EDIT_BUILDER, CUSTOM_ID_SNIPE_REMOVE_BUILDER
)
from .entity_packing import pack_entity, pack_entity_type
from .permission_helpers import can_add_anywhere, can_edit_or_delete_anywhere, get_add_guilds


def build_view_components(
    client,
    user,
    feature_flags,
    entity,
    choices,
    guild_id,
):
    """
    Builds view components.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client displaying the components.
    
    user : ``ClientUserBase``
        The user the components are displayed for.
    
    feature_flags : `int`
        How the message should be displayed as.
    
    entity : ``Emoji | Sticker | SoundboardSound``
        The entity to display.
    
    choices : ``None | list<Emoji | Sticker | SoundboardSound>``
        Additional choices to display.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # description
    components.append(create_text_display(''.join([*produce_description(
        entity, guild_id, feature_flags & FEATURE_FLAG_DETAILED
    )])))
    
    # Asset
    while True:
        entity_type = type(entity)
        if (entity_type is Emoji):
            asset_component = create_media_gallery(entity.url)
        
        elif (entity_type is Sticker):
            sticker_format = entity.format
            if (
                (sticker_format is StickerFormat.png) or
                (sticker_format is StickerFormat.apng) or
                (sticker_format is StickerFormat.gif)
            ):
                asset_component = create_media_gallery(entity.url)
            
            elif (sticker_format is StickerFormat.lottie):
                asset_component = create_attachment_media('attachment://structure.json')
            
            else:
                break
        
        elif (entity_type is SoundboardSound):
            asset_component = create_attachment_media('attachment://sound.mp3')
        
        else:
            break
        
        components.append(asset_component)
        break
    
    # Choices
    if (choices is not None):
        components.append(create_row(create_string_select(
            [
                StringSelectOption(
                    pack_entity(choice),
                    choice.name,
                    (choice if ((type(choice) is Emoji) and client.can_use_emoji(choice)) else None),
                    default = (choice is entity),
                ) for choice in choices
            ],
            custom_id = CUSTOM_ID_SNIPE_CHOICE_BUILDER(user.id, feature_flags),
            placeholder = 'Select an entity',
        )))
    
    # Control
    control_options = []
    
    if not (feature_flags & FEATURE_FLAG_DETAILED):
        control_options.append(
            StringSelectOption(
                ACTION_DETAILS,
                'Details',
                EMOJI_DETAILS,
            )
        )
    
    if not (feature_flags & FEATURE_FLAG_DM):
        control_options.append(
            StringSelectOption(
                ACTION_DM,
                'Dm me',
                EMOJI_DM,
            )
        )
    
    if not (feature_flags & FEATURE_FLAG_REVEALED):
        control_options.append(
            StringSelectOption(
                ACTION_REVEAL,
                'Reveal',
                EMOJI_REVEAL,
            )
        )
    
    if can_add_anywhere(entity_type, entity, user):
        control_options.append(
            StringSelectOption(
                ACTION_ADD,
                'Add',
                EMOJI_ADD,
            )
        )
    
    if can_edit_or_delete_anywhere(entity, user):
        control_options.append(
            StringSelectOption(
                ACTION_EDIT,
                'Edit',
                EMOJI_EDIT,
            )
        )
        
        control_options.append(
            StringSelectOption(
                ACTION_REMOVE,
                'Remove',
                EMOJI_REMOVE,
            )
        )
    
    control_options.append(
        StringSelectOption(
            ACTION_CLOSE,
            'Close',
            EMOJI_CLOSE,
        )
    )
    
    components.append(create_row(create_string_select(
        control_options,
        custom_id = CUSTOM_ID_SNIPE_ACTION_BUILDER(user.id, feature_flags, pack_entity(entity)),
        placeholder = 'Select an action',
    )))
    
    # Return
    return components


def _build_form_name_component(addition, entity_type_name, name):
    """
    Builds form name input component.
    
    Parameters
    ----------
    addition : `bool`
        Whether to build component for addition.
    
    entity_type_name : `str`
        The entity type's name.
    
    name : `None | str`
        Name value to use as default.
    
    Returns
    -------
    component : ``Component``
    """
    if addition:
        description = f'The name to add the {entity_type_name!s} with.'
    else:
        description = f'New name for the {entity_type_name!s}.'
        
    return create_label(
        'Name',
        description,
        create_text_input(
            min_length = 2,
            max_length = 32,
            custom_id = CUSTOM_ID_ENTITY_NAME,
            value = name,
        ),
    )


def _build_form_roles_component(addition, role_ids, entity_guild_id, local_guild_id):
    """
    Builds form roles select component.
    
    Parameters
    ----------
    addition : `bool`
        Whether to build component for addition.
    
    role_ids : `None |tuple<int>`
        Role identifiers to use as the default.
    
    entity_guild_id : `int`
        The entity's guild's identifier.
    
    local_guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    component : ``Component``
    """
    if (not addition) and ((not entity_guild_id) or (entity_guild_id != local_guild_id)):
        return create_text_display(''.join([*produce_form_roles_component_long_description(role_ids)]))
    
    return create_label(
        'Roles',
        FORM_ROLES_DESCRIPTION_MIDDLE,
        create_role_select(
            CUSTOM_ID_ENTITY_ROLES,
            default_values = (
                None
                if role_ids is None else
                [
                    EntitySelectDefaultValue(EntitySelectDefaultValueType.role, role_id)
                    for role_id in islice(role_ids, 0, 25)
                ]
            ),
            max_values = 25,
            min_values = 0,
        ),
    )


def _build_form_tags_component(tags):
    """
    Builds form tags input component.
    
    Parameters
    ----------
    tags : `None | tuple<str>`
        Tags to use as the default value.
    
    Returns
    -------
    component : ``Component``
    """
    return create_label(
        'Tags',
        'Additional values to be matched by auto completion, for custom stickers only 1 is recognized.',
        create_text_input(
            custom_id = CUSTOM_ID_ENTITY_TAGS,
            min_length = 0,
            max_length = 100,
            value = ('' if tags is None else ', '.join(tags)),
        ),
    )


def _build_form_description_component(description):
    """
    Builds form description input component.
    
    Parameters
    ----------
    description : `None | str`
        Description to use as the default value.
    
    Returns
    -------
    component : ``Component``
    """
    return create_label(
        'Description',
        'The sticker\'s description. Supposed to be used by screen readers.',
        create_text_input(
            custom_id = CUSTOM_ID_ENTITY_DESCRIPTION,
            min_length = 0,
            max_length = 1024,
            value = description,
            style = TextInputStyle.paragraph,
        ),
    )


def _build_form_emoji_component(emoji):
    """
    Builds form emoji input component.
    
    Parameters
    ----------
    emoji : ``None | Emoji``
        Emoji to use as the default value.
    
    Returns
    -------
    component : ``Component``
    """
    return create_label(
        'Emoji',
        'An emoji assigned to the sound.',
        create_text_input(
            custom_id = CUSTOM_ID_ENTITY_EMOJI,
            min_length = 0,
            max_length = 60,
            value = (None if emoji is None else emoji.as_emoji),
        ),
    )


def _build_form_volume_component(volume):
    """
    Builds form volume input component.
    
    Parameters
    ----------
    volume : ``None | volume``
        Volume to use as the default value.
    
    Returns
    -------
    component : ``Component``
    """
    return create_label(
        'volume',
        'An volume assigned to the sound.',
        create_text_input(
            custom_id = CUSTOM_ID_ENTITY_VOLUME,
            min_length = 0,
            max_length = 50,
            value = format(volume, '.02f'),
        ),
    )


def _build_form_reason_component():
    """
    Builds form reason input component.
    
    Returns
    -------
    component : ``Component``
    """
    return create_label(
        'Reason',
        'Additional reason that will show up in the guild\'s audit logs.',
        create_text_input(
            custom_id = CUSTOM_ID_ENTITY_REASON,
            min_length = 0,
            max_length = 400,
            style = TextInputStyle.paragraph,
        ),
    )


def build_add_form(user, entity_type, entity, guild_id):
    """
    Builds add entity form.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user adding the entity.
    
    entity_type : ``type<Emoji | Sticker | SoundboardSound>``
        The type of the entity.
    
    entity : ``None | Emoji | Sticker | SoundboardSound``
        Entity to use as default.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    interaction_form : ``InteractionForm``
    """
    entity_type_name = get_entity_type_name(entity_type)
    
    # Build title
    title_parts = ['Add ', entity_type_name]
    if (entity is not None):
        title_parts.append(': ')
        title_parts.append(entity.name)
    
    title = ''.join(title_parts)
    title_parts = None
    
    # Build components
    components = []
    
    # Guild
    guilds = get_add_guilds(user, entity_type, entity)
    guild_select_options = []
    if guilds is None:
        guild_select_options.append(
            StringSelectOption('0', 'none', default = True),
        )
    else:
        for guild in guilds:
            guild_select_options.append(
                StringSelectOption(format(guild.id, 'x'), guild.name, default = (guild.id == guild_id)),
            )
    
    components.append(create_label(
        'Guild',
        f'Select the guild to add the {entity_type_name!s} to.',
        create_string_select(
            guild_select_options,
            custom_id = CUSTOM_ID_ENTITY_GUILD,
        ),
    ))
    
    # Name
    components.append(_build_form_name_component(
        True,
        entity_type_name,
        (None if entity is None else entity.name),
    ))
    
    # Roles
    if (entity_type is Emoji):
        components.append(_build_form_roles_component(
            True,
            (None if ((entity is None) or (entity.guild_id != guild_id)) else entity.role_ids),
            (0 if entity is None else entity.guild_id),
            guild_id,
        ))
    
    # Tags
    if (entity_type is Sticker):
        components.append(_build_form_tags_component(
            (None if entity is None else entity.tags),
        ))
    
    # Description
    if (entity_type is Sticker):
        components.append(_build_form_description_component(
            (None if entity is None else entity.description),
        ))
    
    # Emoji
    if (entity_type is SoundboardSound):
        components.append(_build_form_emoji_component(
            (None if entity is None else entity.emoji),
        ))
    
    # Volume
    if (entity_type is SoundboardSound):
        components.append(_build_form_volume_component(
            (1.0 if entity is None else entity.volume),
        ))
    
    # File
    if (entity is None):
        components.append(create_label(
            'File',
            'Select the file to be used.',
            create_attachment_input(
                custom_id = CUSTOM_ID_ENTITY_FILE,
            ),
        ))
    
    # Reason
    # Ignore this due to discord allowing only up to 5 components.
    # components.append(_build_form_reason_component())
    
    return InteractionForm(
        title,
        components,
        CUSTOM_ID_SNIPE_ADD_BUILDER(pack_entity_type(entity_type) if entity is None else pack_entity(entity)),
    )


def build_edit_form(entity, guild_id):
    """
    Builds edit entity form.
    
    Parameters
    ----------
    entity : ``None | Emoji | Sticker | SoundboardSound``
        Entity to use as default.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    interaction_form : ``InteractionForm``
    """
    entity_type = type(entity)
    entity_type_name = get_entity_type_name(entity_type)
    
    # Build title
    title = f'Edit {entity_type_name!s}: {entity.name}'
    
    # Build components
    components = []
    
    # Name
    components.append(_build_form_name_component(
        False,
        entity_type_name,
        entity.name,
    ))
    
    # Roles
    if (entity_type is Emoji):
        components.append(_build_form_roles_component(
            False,
            entity.role_ids,
            (0 if entity is None else entity.guild_id),
            guild_id,
        ))
    
    # Tags
    if (entity_type is Sticker):
        components.append(_build_form_tags_component(
            entity.tags,
        ))
    
    # Description
    if (entity_type is Sticker):
        components.append(_build_form_description_component(
            entity.description,
        ))
    
    # Emoji
    if (entity_type is SoundboardSound):
        components.append(_build_form_emoji_component(
            entity.emoji,
        ))
    
    # Volume
    if (entity_type is SoundboardSound):
        components.append(_build_form_volume_component(
            entity.volume,
        ))
    
    # Reason
    components.append(_build_form_reason_component())
    
    return InteractionForm(
        title,
        components,
        CUSTOM_ID_SNIPE_EDIT_BUILDER(pack_entity(entity)),
    )


def build_remove_form(entity):
    """
    Builds remove entity form.
    
    Parameters
    ----------
    entity : ``None | Emoji | Sticker | SoundboardSound``
        Entity to use as default.
    
    Returns
    -------
    interaction_form : ``InteractionForm``
    """
    entity_type_name = get_entity_type_name(type(entity))
    
    # Build title
    title = f'Remove {entity_type_name!s}: {entity.name}'
    
    # Build components
    components = []
    
    # Reason
    components.append(_build_form_reason_component())
    
    return InteractionForm(
        title,
        components,
        CUSTOM_ID_SNIPE_REMOVE_BUILDER(pack_entity(entity)),
    )
