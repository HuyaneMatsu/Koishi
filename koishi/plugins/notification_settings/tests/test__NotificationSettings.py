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
    vampytest.assert_instance(notification_settings.daily, bool)
    vampytest.assert_instance(notification_settings.proposal, bool)
    

def test__NotificationSettings__new():
    """
    Tests whether ``NotificationSettings.__new__`` works as intended.
    """
    user_id = 202309240000
    daily = False
    proposal = False
    
    notification_settings = NotificationSettings(user_id, daily = daily, proposal = proposal)
    _assert_fields_set(notification_settings)
    
    vampytest.assert_eq(notification_settings.entry_id, -1)
    vampytest.assert_eq(notification_settings.user_id, user_id)
    vampytest.assert_eq(notification_settings.daily, daily)
    vampytest.assert_eq(notification_settings.proposal, proposal)


def test__NotificationSettings__from_entry():
    """
    Tests whether ``NotificationSettings.from_entry`` works as intended.
    """
    entry_id = 69
    user_id = 202309240001
    daily = False
    proposal = False
    
    entry = {
        'id': entry_id,
        'user_id': user_id,
        'daily': daily,
        'proposal': proposal,
    }
    
    notification_settings = NotificationSettings.from_entry(entry)
    _assert_fields_set(notification_settings)
    
    vampytest.assert_eq(notification_settings.entry_id, entry_id)
    vampytest.assert_eq(notification_settings.user_id, user_id)
    vampytest.assert_eq(notification_settings.daily, daily)
    vampytest.assert_eq(notification_settings.proposal, proposal)


def test__NotificationSettings__repr():
    """
    Tests whether ``NotificationSettings.__repr__`` works as intended.
    """
    entry_id = 69
    user_id = 202309240002
    daily = False
    proposal = False
    
    entry = {
        'id': entry_id,
        'user_id': user_id,
        'daily': daily,
        'proposal': proposal,
    }
    
    notification_settings = NotificationSettings.from_entry(entry)
    vampytest.assert_instance(repr(notification_settings), str)


def test__NotificationSettings__eq():
    """
    Tests whether ``NotificationSettings.__eq__`` works as intended.
    """
    user_id = 202309170036
    daily = False
    proposal = False
    
    notification_settings = NotificationSettings(user_id, daily = daily, proposal = proposal)
    vampytest.assert_eq(notification_settings, notification_settings)
    vampytest.assert_ne(notification_settings, object())
    
    vampytest.assert_ne(notification_settings, NotificationSettings(user_id))
    vampytest.assert_ne(notification_settings, NotificationSettings(user_id, daily = False))
    vampytest.assert_ne(notification_settings, NotificationSettings(202309170037, proposal = False))


def _iter_options__bool():
    yield NotificationSettings(202309170050), False
    yield NotificationSettings(202309170038, daily = False), True
    yield NotificationSettings(202309170039, proposal = False), True


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
    daily = False
    proposal = False
    
    notification_settings = NotificationSettings(user_id, daily = daily, proposal = proposal)
    
    copy = notification_settings.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(notification_settings, copy)
    vampytest.assert_eq(notification_settings, copy)
