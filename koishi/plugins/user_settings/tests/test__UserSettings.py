import vampytest

from ..constants import (
    PREFERRED_IMAGE_SOURCE_NONE, PREFERRED_IMAGE_SOURCE_TOUHOU, USER_SETTINGS_FEATURE_FLAG_DEFAULT,
    USER_SETTINGS_FEATURE_FLAG_DEFAULT_MARKET_PLACE_INBOX, USER_SETTINGS_FEATURE_FLAG_SHIFT_MARKET_PLACE_INBOX,
    USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT, USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_ADVENTURE_RECOVERY_OVER,
    USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_BY_WAIFU, USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_REMINDER,
    USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_GIFT,
    USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_MARKET_PLACE_ITEM_FINALISATION,
    USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_PROPOSAL, USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_VOTE,
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_ADVENTURE_RECOVERY_OVER, USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_BY_WAIFU,
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_REMINDER, USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_GIFT,
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_MARKET_PLACE_ITEM_FINALISATION,
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_PROPOSAL, USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_VOTE
)
from ..user_settings import UserSettings


def _assert_fields_set(user_settings):
    """
    Assets whether every field is set of the given notification settings.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        Notification settings to check.
    """
    vampytest.assert_instance(user_settings, UserSettings)
    
    vampytest.assert_instance(user_settings, UserSettings)
    vampytest.assert_instance(user_settings.entry_id, int)
    vampytest.assert_instance(user_settings.feature_flags, int)
    vampytest.assert_instance(user_settings.notification_flags, int)
    vampytest.assert_instance(user_settings.preferred_client_id, int)
    vampytest.assert_instance(user_settings.preferred_image_source, int)
    vampytest.assert_instance(user_settings.user_id, int)
    

def test__UserSettings__new():
    """
    Tests whether ``UserSettings.__new__`` works as intended.
    """
    user_id = 202604250000
    user_settings = UserSettings(
        user_id,
    )
    _assert_fields_set(user_settings)
    
    vampytest.assert_eq(user_settings.entry_id, 0)
    vampytest.assert_eq(user_settings.feature_flags, USER_SETTINGS_FEATURE_FLAG_DEFAULT)
    vampytest.assert_eq(user_settings.notification_flags, USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT)
    vampytest.assert_eq(user_settings.preferred_client_id, 0)
    vampytest.assert_eq(user_settings.preferred_image_source, PREFERRED_IMAGE_SOURCE_NONE)
    vampytest.assert_eq(user_settings.user_id, user_id)


def test__UserSettings__create_with_specification():
    """
    Tests whether ``UserSettings.create_with_specification`` works as intended.
    """
    user_id = 202309240000
    feature_market_place_inbox = not USER_SETTINGS_FEATURE_FLAG_DEFAULT_MARKET_PLACE_INBOX
    notification_adventure_recovery_over = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_ADVENTURE_RECOVERY_OVER
    notification_daily_by_waifu = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_BY_WAIFU
    notification_daily_reminder = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_REMINDER
    notification_gift = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_GIFT
    notification_market_place_item_finalisation = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_MARKET_PLACE_ITEM_FINALISATION
    notification_proposal = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_PROPOSAL
    notification_vote = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_VOTE
    preferred_client_id = 202402250005
    preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU
    
    user_settings = UserSettings.create_with_specification(
        user_id,
        feature_market_place_inbox = feature_market_place_inbox,
        notification_adventure_recovery_over = notification_adventure_recovery_over,
        notification_daily_by_waifu = notification_daily_by_waifu,
        notification_daily_reminder = notification_daily_reminder,
        notification_gift = notification_gift,
        notification_market_place_item_finalisation = notification_market_place_item_finalisation,
        notification_proposal = notification_proposal,
        notification_vote = notification_vote,
        preferred_client_id = preferred_client_id,
        preferred_image_source = preferred_image_source,
    )
    _assert_fields_set(user_settings)
    
    vampytest.assert_eq(user_settings.entry_id, 0)
    vampytest.assert_eq(user_settings.user_id, user_id)
    vampytest.assert_eq(
        user_settings.feature_flags,
        (
            (feature_market_place_inbox << USER_SETTINGS_FEATURE_FLAG_SHIFT_MARKET_PLACE_INBOX)
        ),
    )
    vampytest.assert_eq(
        user_settings.notification_flags,
        (
            (notification_adventure_recovery_over << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_ADVENTURE_RECOVERY_OVER) |
            (notification_daily_by_waifu << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_BY_WAIFU) |
            (notification_daily_reminder << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_REMINDER) |
            (notification_gift << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_GIFT) |
            (notification_market_place_item_finalisation << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_MARKET_PLACE_ITEM_FINALISATION) |
            (notification_proposal << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_PROPOSAL) |
            (notification_vote << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_VOTE)
        ),
    )
    vampytest.assert_eq(user_settings.preferred_client_id, preferred_client_id)
    vampytest.assert_eq(user_settings.preferred_image_source, preferred_image_source)


def test__UserSettings__from_entry():
    """
    Tests whether ``UserSettings.from_entry`` works as intended.
    """
    entry_id = 69
    feature_flags = 5
    notification_flags = 11
    preferred_client_id = 202402250006
    preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU
    user_id = 202309240001
    
    entry = {
        'id': entry_id,
        'feature_flags': feature_flags,
        'notification_flags': notification_flags,
        'preferred_client_id': preferred_client_id,
        'preferred_image_source': preferred_image_source,
        'user_id': user_id,
    }
    
    user_settings = UserSettings.from_entry(entry)
    _assert_fields_set(user_settings)
    
    vampytest.assert_eq(user_settings.entry_id, entry_id)
    vampytest.assert_eq(user_settings.feature_flags, feature_flags)
    vampytest.assert_eq(user_settings.notification_flags, notification_flags)
    vampytest.assert_eq(user_settings.preferred_client_id, preferred_client_id)
    vampytest.assert_eq(user_settings.preferred_image_source, preferred_image_source)
    vampytest.assert_eq(user_settings.user_id, user_id)


def test__UserSettings__repr():
    """
    Tests whether ``UserSettings.__repr__`` works as intended.
    """
    entry_id = 69
    user_id = 202309240002
    
    user_settings = UserSettings(user_id)
    user_settings.entry_id = entry_id
    vampytest.assert_instance(repr(user_settings), str)


def test__UserSettings__eq():
    """
    Tests whether ``UserSettings.__eq__`` works as intended.
    """
    user_id = 202309170036
    feature_market_place_inbox = not USER_SETTINGS_FEATURE_FLAG_DEFAULT_MARKET_PLACE_INBOX
    notification_adventure_recovery_over = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_ADVENTURE_RECOVERY_OVER
    notification_daily_by_waifu = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_BY_WAIFU
    notification_daily_reminder = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_REMINDER
    notification_gift = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_GIFT
    notification_market_place_item_finalisation = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_MARKET_PLACE_ITEM_FINALISATION
    notification_proposal = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_PROPOSAL
    notification_vote = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_VOTE
    preferred_client_id = 202402250007
    preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU
    
    user_settings = UserSettings.create_with_specification(
        user_id,
        feature_market_place_inbox = feature_market_place_inbox,
        notification_adventure_recovery_over = notification_adventure_recovery_over,
        notification_daily_by_waifu = notification_daily_by_waifu,
        notification_daily_reminder = notification_daily_reminder,
        notification_gift = notification_gift,
        notification_market_place_item_finalisation = notification_market_place_item_finalisation,
        notification_proposal = notification_proposal,
        notification_vote = notification_vote,
        preferred_client_id = preferred_client_id,
        preferred_image_source = preferred_image_source,
    )
    vampytest.assert_eq(user_settings, user_settings)
    vampytest.assert_ne(user_settings, object())
    
    vampytest.assert_ne(user_settings, UserSettings.create_with_specification(user_id))
    vampytest.assert_ne(
        user_settings,
        UserSettings.create_with_specification(
            user_id,
            feature_market_place_inbox = not feature_market_place_inbox,
        ),
    )
    vampytest.assert_ne(
        user_settings,
        UserSettings.create_with_specification(
            user_id,
            notification_daily_by_waifu = USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_DAILY_BY_WAIFU,
        ),
    )
    vampytest.assert_ne(
        user_settings,
        UserSettings.create_with_specification(
            202309170037,
            notification_proposal = USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_PROPOSAL,
        ),
    )


def _iter_options__bool():
    yield (
        'with default',
        UserSettings.create_with_specification(202309170050),
        False,
    )
    
    yield (
        'with feature_market_place_inbox',
        UserSettings.create_with_specification(
            202604230000,
            feature_market_place_inbox = not USER_SETTINGS_FEATURE_FLAG_DEFAULT_MARKET_PLACE_INBOX,
        ),
        True,
    )
    
    yield (
        'with notification_adventure_recovery_over',
        UserSettings.create_with_specification(
            202604230000,
            notification_adventure_recovery_over = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_ADVENTURE_RECOVERY_OVER,
        ),
        True,
    )
    
    yield (
        'with notification_daily_by_waifu',
        UserSettings.create_with_specification(
            202309170038,
            notification_daily_by_waifu = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_BY_WAIFU,
        ),
        True,
    )
    
    yield (
        'with notification_daily_reminder',
        UserSettings.create_with_specification(
            202402250008,
            notification_daily_reminder = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_REMINDER,
        ),
        True,
    )
    
    yield (
        'with notification_gift',
        UserSettings.create_with_specification(
            202309170039,
            notification_gift = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_GIFT,
        ),
        True,
    )
    
    yield (
        'with notification_market_place_item_finalisation',
        UserSettings.create_with_specification(
            202604230001,
            notification_market_place_item_finalisation = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_MARKET_PLACE_ITEM_FINALISATION,
        ),
        True,
    )
    
    yield (
        'with notification_proposal',
        UserSettings.create_with_specification(
            202309170039,
            notification_proposal = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_PROPOSAL,
        ),
        True,
    )
    
    yield (
        'with notification_vote',
        UserSettings.create_with_specification(
            202411250000,
            notification_vote = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_VOTE,
        ),
        True,
    )
    
    yield (
        'with preferred_client_id',
        UserSettings.create_with_specification(
            202402250009,
            preferred_client_id = 202402250010,
        ),
        True,
    )
    
    yield (
        'with preferred_image_source',
        UserSettings.create_with_specification(
            202402250009,
            preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU,
        ),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__bool()).named_first().returning_last())
def test__UserSettings__bool(user_settings):
    """
    Tests whether ``UserSettings.__bool__`` works as intended.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        Notification settings to get their boolean value of.
    
    Returns
    -------
    output : `bool`
    """
    output = bool(user_settings)
    vampytest.assert_instance(output, bool)
    return output


def test__UserSettings__copy():
    """
    Tests whether ``UserSettings.copy`` works as intended.
    """
    user_id = 20230926004
    feature_market_place_inbox = not USER_SETTINGS_FEATURE_FLAG_DEFAULT_MARKET_PLACE_INBOX
    notification_adventure_recovery_over = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_ADVENTURE_RECOVERY_OVER
    notification_daily_by_waifu = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_BY_WAIFU
    notification_daily_reminder = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_DAILY_REMINDER
    notification_gift = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_GIFT
    notification_market_place_item_finalisation = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_MARKET_PLACE_ITEM_FINALISATION
    notification_proposal = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_PROPOSAL
    notification_vote = not USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT_VOTE
    preferred_client_id = 202402250011
    preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU
    
    user_settings = UserSettings.create_with_specification(
        user_id,
        feature_market_place_inbox = feature_market_place_inbox,
        notification_adventure_recovery_over = notification_adventure_recovery_over,
        notification_daily_by_waifu = notification_daily_by_waifu,
        notification_daily_reminder = notification_daily_reminder,
        notification_gift = notification_gift,
        notification_market_place_item_finalisation = notification_market_place_item_finalisation,
        notification_proposal = notification_proposal,
        notification_vote = notification_vote,
        preferred_client_id = preferred_client_id,
        preferred_image_source = preferred_image_source,
    )
    
    copy = user_settings.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(user_settings, copy)
    vampytest.assert_eq(user_settings, copy)
