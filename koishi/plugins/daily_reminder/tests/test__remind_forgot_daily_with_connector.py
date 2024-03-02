import vampytest

from ..reminding import remind_forgot_daily_with_connector


async def test__remind_forgot_daily_with_connector__default():
    """
    Tests whether ``remind_forgot_daily_with_connector`` works as intended.
    
    Case: default.
    
    This function is a coroutine.
    """
    connector = object()
    entry_0 = (23, 202303020000, 202303020001)
    entry_1 = (23, 202303020002, 202303020003)
    entries = [entry_0, entry_1]
    get_entries_to_notify_with_connector_called = False
    notify_user_called = False
    
    async def get_entries_to_notify_with_connector(input_connector):
        nonlocal connector
        nonlocal entries
        nonlocal get_entries_to_notify_with_connector_called
        vampytest.assert_is(input_connector, connector)
        get_entries_to_notify_with_connector_called = True
        return entries
    
    
    async def notify_user(input_entry, input_connector):
        nonlocal connector
        nonlocal entries
        nonlocal notify_user_called
        vampytest.assert_is(input_connector, connector)
        vampytest.assert_in(input_entry, entries)
        notify_user_called = True
    
    mocked = vampytest.mock_globals(
        remind_forgot_daily_with_connector,
        get_entries_to_notify_with_connector = get_entries_to_notify_with_connector,
        notify_user = notify_user,
    )
    
    await mocked(connector)
    
    vampytest.assert_true(get_entries_to_notify_with_connector_called)
    vampytest.assert_true(notify_user_called)
