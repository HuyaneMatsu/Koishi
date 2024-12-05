import vampytest

from ..constants import PREFERRED_IMAGE_SOURCE_TOUHOU
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
    vampytest.assert_instance(user_settings.user_id, int)
    vampytest.assert_instance(user_settings.notification_daily_by_waifu, bool)
    vampytest.assert_instance(user_settings.notification_proposal, bool)
    vampytest.assert_instance(user_settings.notification_vote, bool)
    vampytest.assert_instance(user_settings.notification_daily_reminder, bool)
    vampytest.assert_instance(user_settings.preferred_client_id, int)
    vampytest.assert_instance(user_settings.preferred_image_source, int)
    

def test__UserSettings__new():
    """
    Tests whether ``UserSettings.__new__`` works as intended.
    """
    user_id = 202309240000
    notification_daily_by_waifu = False
    notification_daily_reminder = True
    notification_proposal = False
    notification_vote = False
    preferred_client_id = 202402250005
    preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU
    
    user_settings = UserSettings(
        user_id,
        notification_daily_by_waifu = notification_daily_by_waifu,
        notification_daily_reminder = notification_daily_reminder,
        notification_proposal = notification_proposal,
        notification_vote = notification_vote,
        preferred_client_id = preferred_client_id,
        preferred_image_source = preferred_image_source,
    )
    _assert_fields_set(user_settings)
    
    vampytest.assert_eq(user_settings.entry_id, -1)
    vampytest.assert_eq(user_settings.user_id, user_id)
    vampytest.assert_eq(user_settings.notification_daily_by_waifu, notification_daily_by_waifu)
    vampytest.assert_eq(user_settings.notification_daily_reminder, notification_daily_reminder)
    vampytest.assert_eq(user_settings.notification_proposal, notification_proposal)
    vampytest.assert_eq(user_settings.notification_vote, notification_vote)
    vampytest.assert_eq(user_settings.preferred_client_id, preferred_client_id)
    vampytest.assert_eq(user_settings.preferred_image_source, preferred_image_source)


def test__UserSettings__from_entry():
    """
    Tests whether ``UserSettings.from_entry`` works as intended.
    """
    entry_id = 69
    user_id = 202309240001
    notification_daily_by_waifu = False
    notification_daily_reminder = True
    notification_proposal = False
    notification_vote = False
    preferred_client_id = 202402250006
    preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU
    
    entry = {
        'id': entry_id,
        'user_id': user_id,
        'notification_daily_by_waifu': notification_daily_by_waifu,
        'notification_daily_reminder': notification_daily_reminder,
        'notification_proposal': notification_proposal,
        'notification_vote': notification_vote,
        'preferred_client_id': preferred_client_id,
        'preferred_image_source': preferred_image_source,
    }
    
    user_settings = UserSettings.from_entry(entry)
    _assert_fields_set(user_settings)
    
    vampytest.assert_eq(user_settings.entry_id, entry_id)
    vampytest.assert_eq(user_settings.user_id, user_id)
    vampytest.assert_eq(user_settings.notification_daily_by_waifu, notification_daily_by_waifu)
    vampytest.assert_eq(user_settings.notification_daily_reminder, notification_daily_reminder)
    vampytest.assert_eq(user_settings.notification_proposal, notification_proposal)
    vampytest.assert_eq(user_settings.notification_vote, notification_vote)
    vampytest.assert_eq(user_settings.preferred_client_id, preferred_client_id)
    vampytest.assert_eq(user_settings.preferred_image_source, preferred_image_source)


def test__UserSettings__repr():
    """
    Tests whether ``UserSettings.__repr__`` works as intended.
    """
    entry_id = 69
    user_id = 202309240002
    notification_daily_by_waifu = False
    notification_daily_reminder = True
    notification_proposal = False
    notification_vote = False
    preferred_client_id = 202402250007
    preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU
    
    entry = {
        'id': entry_id,
        'user_id': user_id,
        'notification_daily_by_waifu': notification_daily_by_waifu,
        'notification_daily_reminder': notification_daily_reminder,
        'notification_proposal': notification_proposal,
        'notification_vote': notification_vote,
        'preferred_client_id': preferred_client_id,
        'preferred_image_source': preferred_image_source,
    }
    
    user_settings = UserSettings.from_entry(entry)
    vampytest.assert_instance(repr(user_settings), str)


def test__UserSettings__eq():
    """
    Tests whether ``UserSettings.__eq__`` works as intended.
    """
    user_id = 202309170036
    notification_daily_by_waifu = False
    notification_daily_reminder = True
    notification_proposal = False
    notification_vote = False
    preferred_client_id = 202402250007
    preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU
    
    user_settings = UserSettings(
        user_id,
        notification_daily_by_waifu = notification_daily_by_waifu,
        notification_daily_reminder = notification_daily_reminder,
        notification_proposal = notification_proposal,
        notification_vote = notification_vote,
        preferred_client_id = preferred_client_id,
        preferred_image_source = preferred_image_source,
    )
    vampytest.assert_eq(user_settings, user_settings)
    vampytest.assert_ne(user_settings, object())
    
    vampytest.assert_ne(user_settings, UserSettings(user_id))
    vampytest.assert_ne(user_settings, UserSettings(user_id, notification_daily_by_waifu = False))
    vampytest.assert_ne(user_settings, UserSettings(202309170037, notification_proposal = False))


def _iter_options__bool():
    yield UserSettings(202309170050), False
    yield UserSettings(202309170038, notification_daily_by_waifu = False), True
    yield UserSettings(202402250008, notification_daily_reminder = True), True
    yield UserSettings(202309170039, notification_proposal = False), True
    yield UserSettings(202411250000, notification_vote = False), True
    yield UserSettings(202402250009, preferred_client_id = 202402250010), True
    yield UserSettings(202402250009, preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU), True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
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
    notification_daily_by_waifu = False
    notification_daily_reminder = True
    notification_proposal = False
    notification_vote = False
    preferred_client_id = 202402250011
    preferred_image_source = PREFERRED_IMAGE_SOURCE_TOUHOU
    
    user_settings = UserSettings(
        user_id,
        notification_daily_by_waifu = notification_daily_by_waifu,
        notification_daily_reminder = notification_daily_reminder,
        notification_proposal = notification_proposal,
        notification_vote = notification_vote,
        preferred_client_id = preferred_client_id,
        preferred_image_source = preferred_image_source,
    )
    
    copy = user_settings.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(user_settings, copy)
    vampytest.assert_eq(user_settings, copy)
