import vampytest
from hata import Message

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..automation_reaction_role_item import AutomationReactionRoleItem


def _assert_fields_set(automation_reaction_role_entry):
    """
    Asserts whether the given uto react react role entry has all of its fields set.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The instance to test.
    """
    vampytest.assert_instance(automation_reaction_role_entry, AutomationReactionRoleEntry)
    vampytest.assert_instance(automation_reaction_role_entry.entry_id, int)
    vampytest.assert_instance(automation_reaction_role_entry.flags, int)
    vampytest.assert_instance(automation_reaction_role_entry.items, list, nullable = True)
    vampytest.assert_instance(automation_reaction_role_entry.message, Message)
    vampytest.assert_instance(automation_reaction_role_entry.message_cached, bool)


def test__AutomationReactionRoleEntry__new():
    """
    Tests whether ``AutomationReactionRoleEntry.__new__`` works as intended.
    """
    message = Message.precreate(
        202509270020,
        channel_id = 202509270021,
        guild_id = 202509270022,
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(message)
    
    _assert_fields_set(automation_reaction_role_entry)
    
    vampytest.assert_eq(automation_reaction_role_entry.entry_id, 0)
    vampytest.assert_eq(automation_reaction_role_entry.flags, 0)
    vampytest.assert_is(automation_reaction_role_entry.items, None)
    vampytest.assert_is(automation_reaction_role_entry.message, message)
    vampytest.assert_eq(automation_reaction_role_entry.message_cached, True)


def test__AutomationReactionRoleEntry__from_entry():
    """
    Tests whether ``AutomationReactionRoleEntry.from_entry`` works as intended.
    """
    emoji_id_0 = 202509270023
    role_id_0 = 202509270024
    
    data_version = 1
    flags = 1
    entry_id = 9999
    
    message_id = 202509270025
    channel_id = 202509270026
    guild_id = 202509270027
    
    entry = {
        'id': entry_id,
        'flags': flags,
        'data': b''.join([
            emoji_id_0.to_bytes(8, 'little'),
            (1).to_bytes(1, 'little'),
            (0).to_bytes(1, 'little'),
            role_id_0.to_bytes(8, 'little'),
        ]),
        'data_version': data_version,
        'message_id': message_id,
        'channel_id': channel_id,
        'guild_id': guild_id,
    }
    
    automation_reaction_role_entry = AutomationReactionRoleEntry.from_entry(entry)
    
    _assert_fields_set(automation_reaction_role_entry)
    
    vampytest.assert_eq(automation_reaction_role_entry.entry_id, entry_id)
    vampytest.assert_eq(automation_reaction_role_entry.flags, flags)
    vampytest.assert_eq(
        automation_reaction_role_entry.items,
        [
            AutomationReactionRoleItem(
                emoji_id_0,
                (role_id_0,),
                None,
            ),
        ],
    )
    vampytest.assert_is(
        automation_reaction_role_entry.message,
            Message.precreate(
            message_id,
            channel_id = channel_id,
            guild_id = guild_id,
        ),
    )
    vampytest.assert_eq(automation_reaction_role_entry.message_cached, False)


def test__AutomationReactionRoleEntry__repr():
    """
    Tests whether ``AutomationReactionRoleEntry.__repr__`` works as intended.
    """
    message = Message.precreate(
        202509270028,
        channel_id = 202509270029,
        guild_id = 202509270030,
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(message)
    
    output = repr(automation_reaction_role_entry)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    entry_id = 888
    flags = 1
    items = [
        AutomationReactionRoleItem(
            102,
            (202510010263, 202510010264),
            (202510010265, 202510010266),
        ),
        AutomationReactionRoleItem(
            103,
            None,
            (202510010267),
        ),
    ]
    message = Message.precreate(
        202510010260,
        channel_id = 202510010261,
        guild_id = 202510010262,
    )
    
    
    keyword_parameters = {
        'message': message,
    }
    
    attributes = {
        'entry_id': entry_id,
        'flags': flags,
        'items': items,
    }
    
    yield (
        keyword_parameters,
        attributes,
        keyword_parameters,
        attributes,
        True,
    )
    
    yield (
        keyword_parameters,
        attributes,
        {
            **keyword_parameters,
            'message': Message.precreate(
                202510010270,
                channel_id = 202510010271,
                guild_id = 202510010271,
            ),
        },
        attributes,
        False,
    )
    
    yield (
        keyword_parameters,
        attributes,
        keyword_parameters,
        {
            **attributes,
            'entry_id': 56,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        attributes,
        keyword_parameters,
        {
            **attributes,
            'flags': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        attributes,
        keyword_parameters,
        {
            **attributes,
            'items': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__AutomationReactionRoleEntry__eq(keyword_parameters_0, attributes_0, keyword_parameters_1, attributes_1):
    """
    Tests whether ``AutomationReactionRoleEntry.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    attributes_0 : `None | dict<str, object>`
        Additional attributes to assign.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    attributes_1 : `None | tuple<(str, object)>`
        Additional attributes to assign.
    
    Returns
    -------
    output : `bool`
    """
    automation_reaction_role_entry_0 = AutomationReactionRoleEntry(**keyword_parameters_0)
    if (attributes_0 is not None):
        for item in attributes_0.items():
            setattr(automation_reaction_role_entry_0, *item)
    
    automation_reaction_role_entry_1 = AutomationReactionRoleEntry(**keyword_parameters_1)
    if (attributes_1 is not None):
        for item in attributes_1.items():
            setattr(automation_reaction_role_entry_1, *item)
    
    output = automation_reaction_role_entry_0 == automation_reaction_role_entry_1
    vampytest.assert_instance(output, bool)
    return output


def test__AutomationReactionRoleEntry__copy():
    """
    Tests whether ``AutomationReactionRoleEntry.copy`` works as intended.
    """
    entry_id = 888
    flags = 1
    items = [
        AutomationReactionRoleItem(
            102,
            (202510010283, 202510010284,),
            (202510010285, 202510010286,),
        ),
        AutomationReactionRoleItem(
            103,
            None,
            (202510010287,),
        ),
    ]
    
    message = Message.precreate(
        202510010280,
        channel_id = 202510010281,
        guild_id = 202510010282,
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(message)
    automation_reaction_role_entry.entry_id = entry_id
    automation_reaction_role_entry.flags = flags
    automation_reaction_role_entry.items = items
    
    copy = automation_reaction_role_entry.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, automation_reaction_role_entry)
    vampytest.assert_eq(copy, automation_reaction_role_entry)
