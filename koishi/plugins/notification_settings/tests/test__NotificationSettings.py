import vampytest

from ..notification_settings import NotificationSettings


def _assert_fields_set(notification_settings):
    """
    Assets whether every field is set of the given notification settings.
    
    Parameters
    ----------
    notification_settings : ``NotificationSettings``
        Notification settings to check.
    """
    vampytest.assert_instance(notification_settings, NotificationSettings)
    
    vampytest.assert_instance(notification_settings, NotificationSettings)
    vampytest.assert_instance(notification_settings.entry_id, int)
    vampytest.assert_instance(notification_settings.user_id, int)
    vampytest.assert_instance(notification_settings.daily_by_waifu, bool)
    vampytest.assert_instance(notification_settings.proposal, bool)
    vampytest.assert_instance(notification_settings.daily_reminder, bool)
    vampytest.assert_instance(notification_settings.notifier_client_id, int)
    

def test__NotificationSettings__new():
    """
    Tests whether ``NotificationSettings.__new__`` works as intended.
    """
    user_id = 202309240000
    daily_by_waifu = False
    proposal = False
    daily_reminder = True
    notifier_client_id = 202402250005
    
    notification_settings = NotificationSettings(
        user_id,
        daily_by_waifu = daily_by_waifu,
        proposal = proposal,
        daily_reminder = daily_reminder,
        notifier_client_id = notifier_client_id,
    )
    _assert_fields_set(notification_settings)
    
    vampytest.assert_eq(notification_settings.entry_id, -1)
    vampytest.assert_eq(notification_settings.user_id, user_id)
    vampytest.assert_eq(notification_settings.daily_by_waifu, daily_by_waifu)
    vampytest.assert_eq(notification_settings.proposal, proposal)
    vampytest.assert_eq(notification_settings.daily_reminder, daily_reminder)
    vampytest.assert_eq(notification_settings.notifier_client_id, notifier_client_id)


def test__NotificationSettings__from_entry():
    """
    Tests whether ``NotificationSettings.from_entry`` works as intended.
    """
    entry_id = 69
    user_id = 202309240001
    daily_by_waifu = False
    proposal = False
    daily_reminder = True
    notifier_client_id = 202402250006
    
    entry = {
        'id': entry_id,
        'user_id': user_id,
        'daily_by_waifu': daily_by_waifu,
        'proposal': proposal,
        'daily_reminder': daily_reminder,
        'notifier_client_id': notifier_client_id,
    }
    
    notification_settings = NotificationSettings.from_entry(entry)
    _assert_fields_set(notification_settings)
    
    vampytest.assert_eq(notification_settings.entry_id, entry_id)
    vampytest.assert_eq(notification_settings.user_id, user_id)
    vampytest.assert_eq(notification_settings.daily_by_waifu, daily_by_waifu)
    vampytest.assert_eq(notification_settings.proposal, proposal)
    vampytest.assert_eq(notification_settings.daily_reminder, daily_reminder)
    vampytest.assert_eq(notification_settings.notifier_client_id, notifier_client_id)


def test__NotificationSettings__repr():
    """
    Tests whether ``NotificationSettings.__repr__`` works as intended.
    """
    entry_id = 69
    user_id = 202309240002
    daily_by_waifu = False
    proposal = False
    daily_reminder = True
    notifier_client_id = 202402250007
    
    entry = {
        'id': entry_id,
        'user_id': user_id,
        'daily_by_waifu': daily_by_waifu,
        'proposal': proposal,
        'daily_reminder': daily_reminder,
        'notifier_client_id': notifier_client_id,
    }
    
    notification_settings = NotificationSettings.from_entry(entry)
    vampytest.assert_instance(repr(notification_settings), str)


def test__NotificationSettings__eq():
    """
    Tests whether ``NotificationSettings.__eq__`` works as intended.
    """
    user_id = 202309170036
    daily_by_waifu = False
    proposal = False
    daily_reminder = True
    notifier_client_id = 202402250007
    
    notification_settings = NotificationSettings(
        user_id,
        daily_by_waifu = daily_by_waifu,
        proposal = proposal,
        daily_reminder = daily_reminder,
        notifier_client_id = notifier_client_id,
    )
    vampytest.assert_eq(notification_settings, notification_settings)
    vampytest.assert_ne(notification_settings, object())
    
    vampytest.assert_ne(notification_settings, NotificationSettings(user_id))
    vampytest.assert_ne(notification_settings, NotificationSettings(user_id, daily_by_waifu = False))
    vampytest.assert_ne(notification_settings, NotificationSettings(202309170037, proposal = False))


def _iter_options__bool():
    yield NotificationSettings(202309170050), False
    yield NotificationSettings(202309170038, daily_by_waifu = False), True
    yield NotificationSettings(202309170039, proposal = False), True
    yield NotificationSettings(202402250008, daily_reminder = True), True
    yield NotificationSettings(202402250009, notifier_client_id = 202402250010), True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__NotificationSettings__bool(notification_settings):
    """
    Tests whether ``NotificationSettings.__bool__`` works as intended.
    
    Parameters
    ----------
    notification_settings : ``NotificationSettings``
        Notification settings to get their boolean value of.
    
    Returns
    -------
    output : `bool`
    """
    output = bool(notification_settings)
    vampytest.assert_instance(output, bool)
    return output


def test__NotificationSettings__copy():
    """
    Tests whether ``NotificationSettings.copy`` works as intended.
    """
    user_id = 20230926004
    daily_by_waifu = False
    proposal = False
    daily_reminder = True
    notifier_client_id = 202402250011
    
    notification_settings = NotificationSettings(
        user_id,
        daily_by_waifu = daily_by_waifu,
        proposal = proposal,
        daily_reminder = daily_reminder,
        notifier_client_id = notifier_client_id,
    )
    
    copy = notification_settings.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(notification_settings, copy)
    vampytest.assert_eq(notification_settings, copy)
