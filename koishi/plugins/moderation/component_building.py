__all__ = ()

from hata import (
    InteractionForm, StringSelectOption, TextInputStyle, create_button, create_container, create_label,
    create_media_gallery, create_row, create_section, create_separator, create_string_select, create_text_display,
    create_text_input, create_thumbnail_media, create_user_select
)

from ..unit_core import produce_duration, produce_duration_sophisticated

from .constants import (
    ACTION_TYPE_BAN, ACTION_TYPE_KICK, ACTION_TYPE_MASK_BOUND_GUILD, ACTION_TYPE_MASK_BOUND_USER,
    ACTION_TYPE_MASK_NOTIFIABLE, ACTION_TYPE_MUTE, DURATION_ALLOWED_LENGTH_MAX_THRESHOLD, EMOJI_CLOSE, EMOJI_PAGE_NEXT,
    EMOJI_PAGE_PREVIOUS, REASON_ALLOWED_LENGTH_THRESHOLD, TOP_LIST_PAGE_SIZE
)
from .content_building import (
    produce_mod_other_completion_header, produce_mod_other_form_title, produce_mod_other_notification_header,
    produce_mod_self_completion_header, produce_mod_self_form_title, produce_top_list_content, produce_top_list_header,
    produce_user_banned
)
from .custom_ids import (
    CUSTOM_ID_DELETE_MESSAGE_DURATION, CUSTOM_ID_DURATION, CUSTOM_ID_MOD_OTHER_BUILDER, CUSTOM_ID_MOD_SELF_BUILDER,
    CUSTOM_ID_MOD_TOP_LIST_CLOSE_BUILDER, CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_BUILDER,
    CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_DECREMENT_DISABLED, CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_NOTIFY_USER, CUSTOM_ID_REASON, CUSTOM_ID_USERS
)
from .easter_eggs import IMAGE_URL_NAZRIN, IMAGE_URL_ORIN


def build_reason_input_component(reason):
    """
    Builds reason input component.
    
    Parameters
    ----------
    reason : `None | str`
        Reason.
    
    Returns
    -------
    component : ``Component``
    """
    return create_label(
        'Reason',
        None,
        create_text_input(
            custom_id = CUSTOM_ID_REASON,
            max_length = REASON_ALLOWED_LENGTH_THRESHOLD,
            value = reason,
            style = TextInputStyle.paragraph,
        ),
    )


def build_users_input_component():
    """
    Builds user input component.
    
    Returns
    -------
    component : ``Component``
    """
    return create_label(
        'Select users',
        None,
        create_user_select(
            custom_id = CUSTOM_ID_USERS,
            min_values = 1,
            required = True,
        ),
    )


def build_notify_user_input_component():
    """
    Builds delete message days component.
    
    Returns
    -------
    component : ``Component``
    """
    return create_label(
        'Notify user',
        None,
        create_string_select(
            [
                StringSelectOption('0', 'Nah', default = True),
                StringSelectOption('1', 'Yes'),
            ],
            custom_id = CUSTOM_ID_NOTIFY_USER,
        ),
    )


def build_delete_message_duration_input_component(default):
    """
    Builds delete message duration component.
    
    Parameters
    ----------
    default : `int`
        Default duration to use.
    
    Returns
    -------
    component : ``Component``
    """
    return create_label(
        'Delete message duration',
        'w for week, d for day, h for hour, m for minute, s for second.',
        create_text_input(
            custom_id = CUSTOM_ID_DELETE_MESSAGE_DURATION,
            max_length = DURATION_ALLOWED_LENGTH_MAX_THRESHOLD,
            value = (''.join([*produce_duration(default)]) if default else None),
        ),
    )


def build_duration_input_component(default):
    """
    Builds duration component.
    
    Parameters
    ----------
    default : `int`
        Default duration to use.
    
    Returns
    -------
    component : ``Component``
    """
    return create_label(
        'Duration',
        'w for week, d for day, h for hour, m for minute, s for second.',
        create_text_input(
            custom_id = CUSTOM_ID_DURATION,
            max_length = DURATION_ALLOWED_LENGTH_MAX_THRESHOLD,
            value = (''.join([*produce_duration(default)]) if default else None),
        ),
    )


def build_mod_other_form(
    action_type, target, guild, reason_default, delete_message_days_duration_default, duration_default
):
    """
    Builds mod other components.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    target : ``None | ClientUserBase``
        The targeted user if any.
    
    guild : ``Guild``
        The local guild.
    
    reason_default : `None | str`
        Default reason to use.
    
    delete_message_days_duration_default : `int`
        Default delete message days duration.
    
    duration_default : `int`
        Default duration.
    
    Returns
    -------
    interaction_form : ``InteractionForm``
    """
    components = []
    
    if (action_type & ACTION_TYPE_MASK_BOUND_USER) and (target is None):
        components.append(build_users_input_component())
    
    components.append(build_reason_input_component(reason_default))
    
    if action_type & ACTION_TYPE_MASK_NOTIFIABLE:
        components.append(build_notify_user_input_component())
    
    if (action_type == ACTION_TYPE_BAN):
        components.append(build_delete_message_duration_input_component(delete_message_days_duration_default))
    
    if (action_type == ACTION_TYPE_MUTE):
        components.append(build_duration_input_component(duration_default))
    
    return InteractionForm(
        ''.join([*produce_mod_other_form_title(action_type, target, guild)]),
        components,
        custom_id = CUSTOM_ID_MOD_OTHER_BUILDER(action_type, (0 if target is None else target.id)),
    )


def build_mod_self_form(
    action_type, guild, duration_default
):
    """
    Builds mod self components.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    guild : ``Guild``
        The local guild.
    
    duration_default : `int`
        Default duration.
    
    Returns
    -------
    interaction_form : ``InteractionForm``
    """
    components = []
    
    components.append(build_reason_input_component(None))
    
    if (action_type == ACTION_TYPE_MUTE):
        components.append(build_duration_input_component(duration_default))
    
    return InteractionForm(
        ''.join([*produce_mod_self_form_title(action_type, guild)]),
        components,
        custom_id = CUSTOM_ID_MOD_SELF_BUILDER(action_type),
    )


def build_mod_other_notification_components(action_type, guild, reason, duration):
    """
    Builds notification components.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    guild : ``Guild``
        The local guild.
    
    reason : `None | str`
        Reason to use.
    
    duration : `int`
        Duration.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    components.append(create_text_display(''.join([*produce_mod_other_notification_header(action_type, guild)])))
    
    if (reason is not None):
        components.append(create_text_display('Reason:'))
        components.append(create_container(create_text_display(reason)))
    
    if (action_type == ACTION_TYPE_MUTE):
        components.append(create_text_display(''.join([
            'Duration: ', *produce_duration_sophisticated(duration),
        ])))
    
    return components


def build_mod_other_completion_components(
    action_type, targets, guild, reason, notify_user, delete_message_duration, duration, easter_egg_mode
):
    """
    Builds completion components.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    targets : ``None | tuple<ClientUserBase>``
        Targeted users.
    
    guild : ``Guild``
        The local guild.
    
    reason : `None | str`
        Reason to use.
    
    notify_user : `bool`
        Whether the user has been notified.
    
    delete_message_duration : `int`
        How old messages to delete.
    
    duration : `int`
        Duration.
    
    easter_egg_mode : `bool`
        Whether easter egg image should be shown.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    header_component = create_text_display(''.join([*produce_mod_other_completion_header(action_type, targets, guild)]))
    
    icon_url = None
    if action_type & ACTION_TYPE_MASK_BOUND_GUILD:
        icon_url = guild.icon_url
    
    elif action_type & ACTION_TYPE_MASK_BOUND_USER:
        if (targets is not None) and (len(targets) == 1):
            icon_url = targets[0].avatar_url_at(guild.id)
    
    if (icon_url is not None):
        header_component = create_section(
            header_component,
            thumbnail = create_thumbnail_media(icon_url),
        )
    
    components.append(header_component)
    
    if (reason is None):
        components.append(create_text_display('Reason: \*none\*'))
    else:
        components.append(create_text_display('Reason:'))
        components.append(create_container(create_text_display(reason)))
    
    if action_type & ACTION_TYPE_MASK_NOTIFIABLE:
        
        components.append(create_text_display(
            'Notify user: ' + ('yes' if notify_user else 'no'),
        ))
    
    if (action_type == ACTION_TYPE_BAN):
        components.append(create_text_display(''.join([
            'Delete messages duration: ', *produce_duration_sophisticated(delete_message_duration),
        ])))
    
    if (action_type == ACTION_TYPE_MUTE):
        components.append(create_text_display(''.join([
            'Duration: ', *produce_duration_sophisticated(duration),
        ])))
    
    if easter_egg_mode:
        if (action_type == ACTION_TYPE_BAN) or (action_type ==ACTION_TYPE_KICK):
            components.append(create_media_gallery(IMAGE_URL_ORIN))
        elif (action_type == ACTION_TYPE_MUTE):
            components.append(create_media_gallery(IMAGE_URL_NAZRIN))
    
    return components


def build_mod_self_completion_components(
    action_type, user, guild_id, reason, duration
):
    """
    Builds completion components.
    
    Parameters
    ----------
    action_type : `int`
        The action's type to be executed.
    
    user : ``ClientUserBase``
        The user actioning themselves.
    
    guild_id : `int`
        The local guild's identifier.
    
    reason : `None | str`
        Reason to use.
    
    duration : `int`
        Duration.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    components.append(create_section(
        create_text_display(''.join([*produce_mod_self_completion_header(action_type, user, guild_id)])),
        thumbnail = create_thumbnail_media(user.avatar_url_at(guild_id)),
    ))
    
    if (reason is None):
        components.append(create_text_display('Reason: \*none\*'))
    else:
        components.append(create_text_display('Reason:'))
        components.append(create_container(create_text_display(reason)))
    
    if (action_type == ACTION_TYPE_MUTE):
        components.append(create_text_display(''.join([
            'Duration: ', *produce_duration_sophisticated(duration),
        ])))
    
    return components


def build_mod_top_list_components(user_id, guild, page_index, entries, sort_by, days):
    """
    Builds mod top-list components.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    guild : ``Guild```
        The local guild.
    
    page_index : `int`
        The page to show. Used to calculate entry index.
    
    entries : ``list<(ClientUserBase, ActionCounter)>``
        Top list entries.
    
    sort_by : `int`
        The actions' identifier to sort by. Used to highlight that specific row.
    
    days : `int`
        The days to query for.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Header.
    header_component = create_text_display(''.join([*produce_top_list_header(guild, page_index, sort_by, days)]))
    icon_url = guild.icon_url
    if (icon_url is not None):
        header_component = create_section(
            header_component,
            thumbnail = create_thumbnail_media(icon_url),
        )
    
    components.append(header_component)
    components.append(create_separator())
    
    # Content.
    
    entries_slice = entries[page_index * TOP_LIST_PAGE_SIZE : (page_index + 1) * TOP_LIST_PAGE_SIZE]
    if entries_slice:
        components.append(create_text_display(''.join([*produce_top_list_content(
            page_index, entries_slice, sort_by, guild.id
        )])))
        components.append(create_separator())
    
    # Control.
    
    if page_index == 0:
        page_index_decrement_button_custom_id = CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_DECREMENT_DISABLED
        page_index_decrement_button_enabled = False
    else:
        page_index_decrement_button_custom_id = CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_BUILDER(
            user_id, page_index - 1, sort_by, days
        )
        page_index_decrement_button_enabled = True
    
    if len(entries) <= (page_index + 1) * TOP_LIST_PAGE_SIZE:
        page_index_increment_button_custom_id = CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_INCREMENT_DISABLED
        page_index_increment_button_enabled = False
    else:
        page_index_increment_button_custom_id = CUSTOM_ID_MOD_TOP_LIST_PAGE_INDEX_BUILDER(
            user_id, page_index + 1, sort_by, days
        )
        page_index_increment_button_enabled = True
    
    components.append(create_row(
        create_button(
            f'Page {page_index}',
            EMOJI_PAGE_PREVIOUS,
            custom_id = page_index_decrement_button_custom_id,
            enabled = page_index_decrement_button_enabled,
        ),
        create_button(
            f'Page {page_index + 2}',
            EMOJI_PAGE_NEXT,
            custom_id = page_index_increment_button_custom_id,
            enabled = page_index_increment_button_enabled,
        ),
        create_button(
            'Close',
            EMOJI_CLOSE,
            custom_id = CUSTOM_ID_MOD_TOP_LIST_CLOSE_BUILDER(user_id),
        ),
    ))
    
    return components


def build_mod_ban_question_components(target, guild_id, banned, reason):
    """
    Builds ban questioning components.
    
    Parameters
    ----------
    target : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The local guild's identifier.
    
    banned : `bool`
        Whether the user is banned.
    
    reason : `None | str`
        Ban reason.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    components.append(create_section(
        create_text_display(''.join([*produce_user_banned(target, guild_id, banned)])),
        thumbnail = create_thumbnail_media(target.avatar_url_at(guild_id)),
    ))
    
    if banned:
        if (reason is None):
            components.append(create_text_display('Reason: \*none\*'))
        else:
            components.append(create_text_display('Reason:'))
            components.append(create_container(create_text_display(reason)))
    
    return components
