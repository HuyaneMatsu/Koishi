import vampytest

from ..automation_reaction_role_item import AutomationReactionRoleItem


def _assert_fields_set(automation_reaction_role_item):
    """
    Asserts whether every fields are set of the given auto react role item.
    
    Parameters
    ----------
    automation_reaction_role_item : ``AutomationReactionRoleItem``
    """
    vampytest.assert_instance(automation_reaction_role_item, AutomationReactionRoleItem)
    vampytest.assert_instance(automation_reaction_role_item.emoji_id, int)
    vampytest.assert_instance(automation_reaction_role_item.add_role_ids, tuple, nullable = True)
    vampytest.assert_instance(automation_reaction_role_item.remove_role_ids, tuple, nullable = True)


def test__AutomationReactionRoleItem__new():
    """
    Tests whether ``AutomationReactionRoleItem.__new__`` works as intended.
    """
    emoji_id = 202509270000
    add_role_ids = (202509270001, 202509270002)
    remove_role_ids = (202509270003, 202509270004)
    
    automation_reaction_role_item = AutomationReactionRoleItem(
        emoji_id,
        add_role_ids,
        remove_role_ids,
    )
    _assert_fields_set(automation_reaction_role_item)
    
    vampytest.assert_eq(automation_reaction_role_item.emoji_id, emoji_id)
    vampytest.assert_eq(automation_reaction_role_item.add_role_ids, add_role_ids)
    vampytest.assert_eq(automation_reaction_role_item.remove_role_ids, remove_role_ids)


def test__AutomationReactionRoleItem__repr():
    """
    Tests whether ``AutomationReactionRoleItem.__repr__`` works as intended.
    """
    emoji_id = 202509270005
    add_role_ids = (202509270006, 202509270007)
    remove_role_ids = (202509270008, 202509270009)
    
    automation_reaction_role_item = AutomationReactionRoleItem(
        emoji_id,
        add_role_ids,
        remove_role_ids,
    )
    _assert_fields_set(automation_reaction_role_item)
    
    output = repr(automation_reaction_role_item)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    emoji_id = 202509270050
    add_role_ids = (202509270051, 202509270052)
    remove_role_ids = (202509270053, 202509270054)
    
    keyword_parameters = {
        'emoji_id': emoji_id,
        'add_role_ids': add_role_ids,
        'remove_role_ids': remove_role_ids,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'emoji_id': 202509270055,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'add_role_ids': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'remove_role_ids': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__AutomationReactionRoleItem__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``AutomationReactionRoleItem.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    automation_reaction_role_item_0 = AutomationReactionRoleItem(**keyword_parameters_0)
    automation_reaction_role_item_1 = AutomationReactionRoleItem(**keyword_parameters_1)
    
    output = automation_reaction_role_item_0 == automation_reaction_role_item_1
    vampytest.assert_instance(output, bool)
    return output


def test__AutomationReactionRoleItem__copy():
    """
    Tests whether ``AutomationReactionRoleItem.copy`` works as intended.
    """
    emoji_id = 202510010250
    add_role_ids = (202510010251, 202510010252)
    remove_role_ids = (202510010253, 202510010254)
    
    automation_reaction_role_item = AutomationReactionRoleItem(
        emoji_id,
        add_role_ids,
        remove_role_ids,
    )
    copy = automation_reaction_role_item.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, automation_reaction_role_item)
    vampytest.assert_eq(copy, automation_reaction_role_item)
