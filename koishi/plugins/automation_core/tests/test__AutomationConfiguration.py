import vampytest
from hata import BUILTIN_EMOJIS
from scarletio import skip_ready_cycle

from ....bot_utils.models import DB_ENGINE

from ..automation_configuration import AutomationConfiguration
from ..automation_configuration_saver import AutomationConfigurationSaver

from ..constants import (
    AUTOMATION_CONFIGURATIONS, COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT,
    COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT, COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT
)


def _assert_fields_set(automation_configuration):
    """
    Asserts whether every fields are set of the automation configuration.
    
    Parameters
    ----------
    automation_configuration : ``AutomationConfiguration``
        Automation configuration to test.
    """
    vampytest.assert_instance(automation_configuration, AutomationConfiguration)
    vampytest.assert_instance(automation_configuration.community_message_moderation_availability_duration, int)
    vampytest.assert_instance(automation_configuration.community_message_moderation_down_vote_emoji_id, int)
    vampytest.assert_instance(automation_configuration.community_message_moderation_enabled, int)
    vampytest.assert_instance(automation_configuration.community_message_moderation_log_enabled, bool)
    vampytest.assert_instance(automation_configuration.community_message_moderation_log_channel_id, int)
    vampytest.assert_instance(automation_configuration.community_message_moderation_up_vote_emoji_id, int)
    vampytest.assert_instance(automation_configuration.community_message_moderation_vote_threshold, int)
    vampytest.assert_instance(automation_configuration.entry_id, int)
    vampytest.assert_instance(automation_configuration.farewell_channel_id, int)
    vampytest.assert_instance(automation_configuration.farewell_enabled, bool)
    vampytest.assert_instance(automation_configuration.farewell_style_name, str, nullable = True)
    vampytest.assert_instance(automation_configuration.guild_id, int)
    vampytest.assert_instance(automation_configuration.log_emoji_channel_id, int)
    vampytest.assert_instance(automation_configuration.log_emoji_enabled, bool)
    vampytest.assert_instance(automation_configuration.log_mention_channel_id, int)
    vampytest.assert_instance(automation_configuration.log_mention_enabled, bool)
    vampytest.assert_instance(automation_configuration.log_satori_auto_start, bool)
    vampytest.assert_instance(automation_configuration.log_satori_channel_id, int)
    vampytest.assert_instance(automation_configuration.log_satori_enabled, bool)
    vampytest.assert_instance(automation_configuration.log_sticker_channel_id, int)
    vampytest.assert_instance(automation_configuration.log_sticker_enabled, bool)
    vampytest.assert_instance(automation_configuration.log_user_channel_id, int)
    vampytest.assert_instance(automation_configuration.log_user_enabled, bool)
    vampytest.assert_instance(automation_configuration.reaction_copy_enabled, int)
    vampytest.assert_instance(automation_configuration.reaction_copy_flags, int)
    vampytest.assert_instance(automation_configuration.reaction_copy_role_id, int)
    vampytest.assert_instance(automation_configuration.saver, AutomationConfigurationSaver, nullable = True)
    vampytest.assert_instance(automation_configuration.touhou_feed_enabled, bool)
    vampytest.assert_instance(automation_configuration.welcome_channel_id, int)
    vampytest.assert_instance(automation_configuration.welcome_enabled, bool)
    vampytest.assert_instance(automation_configuration.welcome_reply_buttons_enabled, bool)
    vampytest.assert_instance(automation_configuration.welcome_style_name, str, nullable = True)


def test__AutomationConfiguration__new():
    """
    Tests whether ``AutomationConfiguration.__new__`` works as intended.
    """
    guild_id = 202405280000
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        _assert_fields_set(automation_configuration)
        
        vampytest.assert_eq(automation_configuration.guild_id, guild_id)
        
        # Should not auto store in cache
        vampytest.assert_is(AUTOMATION_CONFIGURATIONS.get(guild_id, None), None)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


def test__AutomationConfiguration__repr():
    """
    Tests whether ``automation_configuration.__repr__`` works as intended.
    """
    guild_id = 202405280001
    
    try:
        community_message_moderation_availability_duration = 3605
        community_message_moderation_down_vote_emoji_id = BUILTIN_EMOJIS['red_heart'].id
        community_message_moderation_enabled = True
        community_message_moderation_log_enabled = True
        community_message_moderation_log_channel_id = 202405280002
        community_message_moderation_up_vote_emoji_id = BUILTIN_EMOJIS['green_heart'].id
        community_message_moderation_vote_threshold = 6
        entry_id = 1222222222222222
        farewell_channel_id = 202407140000
        farewell_enabled = True
        farewell_style_name = 'flandre'
        log_emoji_channel_id = 202405280003
        log_emoji_enabled = True
        log_mention_channel_id = 202405280004
        log_mention_enabled = True
        log_satori_auto_start = True
        log_satori_channel_id = 202405280005
        log_satori_enabled = True
        log_sticker_channel_id = 202405280006
        log_sticker_enabled = True
        log_user_channel_id = 202405280007
        log_user_enabled = True
        reaction_copy_enabled = True
        reaction_copy_flags = 12
        reaction_copy_role_id = 202405280008
        touhou_feed_enabled = True
        welcome_channel_id = 202405280009
        welcome_enabled = True
        welcome_reply_buttons_enabled = True
        welcome_style_name = 'yoshika'
        
        
        automation_configuration = AutomationConfiguration(guild_id)
        automation_configuration.community_message_moderation_availability_duration = community_message_moderation_availability_duration
        automation_configuration.community_message_moderation_down_vote_emoji_id = community_message_moderation_down_vote_emoji_id
        automation_configuration.community_message_moderation_enabled = community_message_moderation_enabled
        automation_configuration.community_message_moderation_log_enabled = community_message_moderation_log_enabled
        automation_configuration.community_message_moderation_log_channel_id = community_message_moderation_log_channel_id
        automation_configuration.community_message_moderation_up_vote_emoji_id = community_message_moderation_up_vote_emoji_id
        automation_configuration.community_message_moderation_vote_threshold = community_message_moderation_vote_threshold
        automation_configuration.entry_id = entry_id
        automation_configuration.farewell_channel_id = farewell_channel_id
        automation_configuration.farewell_enabled = farewell_enabled
        automation_configuration.farewell_style_name = farewell_style_name
        automation_configuration.log_emoji_channel_id = log_emoji_channel_id
        automation_configuration.log_emoji_enabled = log_emoji_enabled
        automation_configuration.log_mention_channel_id = log_mention_channel_id
        automation_configuration.log_mention_enabled = log_mention_enabled
        automation_configuration.log_satori_auto_start = log_satori_auto_start
        automation_configuration.log_satori_channel_id = log_satori_channel_id
        automation_configuration.log_satori_enabled = log_satori_enabled
        automation_configuration.log_sticker_channel_id = log_sticker_channel_id
        automation_configuration.log_sticker_enabled = log_sticker_enabled
        automation_configuration.log_user_channel_id = log_user_channel_id
        automation_configuration.log_user_enabled = log_user_enabled
        automation_configuration.reaction_copy_enabled = reaction_copy_enabled
        automation_configuration.reaction_copy_flags = 12
        automation_configuration.reaction_copy_role_id = reaction_copy_role_id
        automation_configuration.touhou_feed_enabled = touhou_feed_enabled
        automation_configuration.welcome_channel_id = welcome_channel_id
        automation_configuration.welcome_enabled = welcome_enabled
        automation_configuration.welcome_reply_buttons_enabled = welcome_reply_buttons_enabled
        automation_configuration.welcome_style_name = welcome_style_name
        
        output = repr(automation_configuration)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(AutomationConfiguration.__name__, output)
        vampytest.assert_in(f'guild_id = {guild_id!r}', output)
        vampytest.assert_in(f'community_message_moderation_availability_duration = {community_message_moderation_availability_duration!r}', output)
        vampytest.assert_in(f'community_message_moderation_down_vote_emoji_id = {community_message_moderation_down_vote_emoji_id!r}', output)
        vampytest.assert_in(f'community_message_moderation_enabled = {community_message_moderation_enabled!r}', output)
        vampytest.assert_in(f'community_message_moderation_log_enabled = {community_message_moderation_log_enabled!r}', output)
        vampytest.assert_in(f'community_message_moderation_log_channel_id = {community_message_moderation_log_channel_id!r}', output)
        vampytest.assert_in(f'community_message_moderation_up_vote_emoji_id = {community_message_moderation_up_vote_emoji_id!r}', output)
        vampytest.assert_in(f'community_message_moderation_vote_threshold = {community_message_moderation_vote_threshold!r}', output)
        vampytest.assert_in(f'entry_id = {entry_id!r}', output)
        vampytest.assert_in(f'farewell_channel_id = {farewell_channel_id!r}', output)
        vampytest.assert_in(f'farewell_enabled = {farewell_enabled!r}', output)
        vampytest.assert_in(f'farewell_style_name = {farewell_style_name!r}', output)
        vampytest.assert_in(f'log_emoji_channel_id = {log_emoji_channel_id!r}', output)
        vampytest.assert_in(f'log_emoji_enabled = {log_emoji_enabled!r}', output)
        vampytest.assert_in(f'log_mention_channel_id = {log_mention_channel_id!r}', output)
        vampytest.assert_in(f'log_mention_enabled = {log_mention_enabled!r}', output)
        vampytest.assert_in(f'log_satori_auto_start = {log_satori_auto_start!r}', output)
        vampytest.assert_in(f'log_satori_channel_id = {log_satori_channel_id!r}', output)
        vampytest.assert_in(f'log_satori_enabled = {log_satori_enabled!r}', output)
        vampytest.assert_in(f'log_sticker_channel_id = {log_sticker_channel_id!r}', output)
        vampytest.assert_in(f'log_sticker_enabled = {log_sticker_enabled!r}', output)
        vampytest.assert_in(f'log_user_channel_id = {log_user_channel_id!r}', output)
        vampytest.assert_in(f'log_user_enabled = {log_user_enabled!r}', output)
        vampytest.assert_in(f'reaction_copy_enabled = {reaction_copy_enabled!r}', output)
        vampytest.assert_in(f'reaction_copy_flags = {reaction_copy_flags!r}', output)
        vampytest.assert_in(f'reaction_copy_role_id = {reaction_copy_role_id!r}', output)
        vampytest.assert_in(f'touhou_feed_enabled = {touhou_feed_enabled!r}', output)
        vampytest.assert_in(f'welcome_channel_id = {welcome_channel_id!r}', output)
        vampytest.assert_in(f'welcome_enabled = {welcome_enabled!r}', output)
        vampytest.assert_in(f'welcome_reply_buttons_enabled = {welcome_reply_buttons_enabled!r}', output)
        vampytest.assert_in(f'welcome_style_name = {welcome_style_name!r}', output)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


def _iter_options__bool():
    guild_id = 202405280018
    
    community_message_moderation_availability_duration = 3605
    community_message_moderation_down_vote_emoji_id = BUILTIN_EMOJIS['red_heart'].id
    community_message_moderation_enabled = True
    community_message_moderation_log_enabled = True
    community_message_moderation_log_channel_id = 202405280010
    community_message_moderation_up_vote_emoji_id = BUILTIN_EMOJIS['green_heart'].id
    community_message_moderation_vote_threshold = 6
    entry_id = 1222222222222222
    farewell_channel_id = 202407140001
    farewell_enabled = True
    farewell_style_name = 'flandre'
    log_emoji_channel_id = 202405280011
    log_emoji_enabled = True
    log_mention_channel_id = 202405280012
    log_mention_enabled = True
    log_satori_auto_start = True
    log_satori_channel_id = 202405280013
    log_satori_enabled = True
    log_sticker_channel_id = 202405280014
    log_sticker_enabled = True
    log_user_channel_id = 202405280015
    log_user_enabled = True
    reaction_copy_enabled = True
    reaction_copy_flags = 12
    reaction_copy_role_id = 202405280016
    touhou_feed_enabled = True
    welcome_channel_id = 202405280017
    welcome_enabled = True
    welcome_reply_buttons_enabled = True
    welcome_style_name = 'yoshika'
    
    yield (
        {},
        False,
    )
    
    yield (
        {
            'community_message_moderation_availability_duration': community_message_moderation_availability_duration,
        },
        True,
    )
    
    yield (
        {
            'community_message_moderation_down_vote_emoji_id': community_message_moderation_down_vote_emoji_id,
        },
        True,
    )
    
    yield (
        {
            'community_message_moderation_enabled': community_message_moderation_enabled,
        },
        True,
    )
    
    yield (
        {
            'community_message_moderation_log_enabled': community_message_moderation_log_enabled,
        },
        True,
    )
    
    yield (
        {
            'community_message_moderation_log_channel_id': community_message_moderation_log_channel_id,
        },
        True,
    )
    
    yield (
        {
            'community_message_moderation_up_vote_emoji_id': community_message_moderation_up_vote_emoji_id,
        },
        True,
    )
    
    yield (
        {
            'community_message_moderation_vote_threshold': community_message_moderation_vote_threshold,
        },
        True,
    )
    
    yield (
        {
            'log_emoji_channel_id': log_emoji_channel_id,
        },
        True,
    )
    
    yield (
        {
            'entry_id': entry_id,
        },
        False,
    )
    
    yield (
        {
            'farewell_channel_id': farewell_channel_id,
        },
        True,
    )
    
    yield (
        {
            'farewell_enabled': farewell_enabled,
        },
        True,
    )
    
    yield (
        {
            'farewell_style_name': farewell_style_name,
        },
        True,
    )
    
    yield (
        {
            'guild_id': guild_id,
        },
        False,
    )
    
    yield (
        {
            'log_emoji_enabled': log_emoji_enabled,
        },
        True,
    )
    
    yield (
        {
            'log_emoji_channel_id': log_emoji_channel_id,
        },
        True,
    )
    
    yield (
        {
            'log_mention_channel_id': log_mention_channel_id,
        },
        True,
    )
    
    yield (
        {
            'log_mention_enabled': log_mention_enabled,
        },
        True,
    )
    
    yield (
        {
            'log_satori_auto_start': log_satori_auto_start,
        },
        True,
    )
    
    yield (
        {
            'log_satori_channel_id': log_satori_channel_id,
        },
        True,
    )
    
    yield (
        {
            'log_satori_enabled': log_satori_enabled,
        },
        True,
    )
    
    yield (
        {
            'log_sticker_channel_id': log_sticker_channel_id,
        },
        True,
    )
    
    yield (
        {
            'log_sticker_enabled': log_sticker_enabled,
        },
        True,
    )
    
    yield (
        {
            'log_user_channel_id': log_user_channel_id,
        },
        True,
    )
    
    yield (
        {
            'log_user_enabled': log_user_enabled,
        },
        True,
    )
    
    yield (
        {
            'reaction_copy_enabled': reaction_copy_enabled,
        },
        True,
    )
    
    yield (
        {
            'reaction_copy_flags': reaction_copy_flags,
        },
        True,
    )
    
    yield (
        {
            'reaction_copy_role_id': reaction_copy_role_id,
        },
        True,
    )
    
    yield (
        {
            'touhou_feed_enabled': touhou_feed_enabled,
        },
        True,
    )
    
    yield (
        {
            'welcome_channel_id': welcome_channel_id,
        },
        True,
    )
    
    yield (
        {
            'welcome_enabled': welcome_enabled,
        },
        True,
    )
    
    yield (
        {
            'welcome_reply_buttons_enabled': welcome_reply_buttons_enabled,
        },
        True,
    )
    
    yield (
        {
            'welcome_style_name': welcome_style_name,
        },
        True,
    )
    
    yield (
        {
            'community_message_moderation_down_vote_emoji_id': COMMUNITY_MESSAGE_MODERATION_DOWN_VOTE_EMOJI_ID_DEFAULT,
        },
        False,
    )
    
    yield (
        {
            'community_message_moderation_availability_duration': COMMUNITY_MESSAGE_MODERATION_AVAILABILITY_DURATION_DEFAULT,
        },
        False,
    )
    
    yield (
        {
            'community_message_moderation_vote_threshold': COMMUNITY_MESSAGE_MODERATION_VOTE_THRESHOLD_DEFAULT,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__AutomationConfiguration__bool(attributes):
    """
    Tests whether ``AutomationConfiguration.__bool__`` works as intended.
    
    Parameters
    ----------
    attributes : `dict<str, object>`
        Attributes to set.
    
    Returns
    -------
    output : `bool`
    """
    guild_id = 0
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        for item in attributes.items():
            setattr(automation_configuration, *item)
        
        output = bool(automation_configuration)
        vampytest.assert_instance(output, bool)
        return output

    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


def test__AutomationConfiguration__get_saver():
    """
    Tests whether ``AutomationConfiguration.get_saver`` works as intended.
    """
    guild_id = 202405280030
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        
        output = automation_configuration.get_saver()
        vampytest.assert_instance(output, AutomationConfigurationSaver)
        vampytest.assert_is(output.entry_proxy, automation_configuration)
        vampytest.assert_is(automation_configuration.saver, output)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


def test__AutomationConfiguration__get_saver__caching():
    """
    Tests whether ``AutomationConfiguration.get_saver`` works as intended.
    
    Case: caching.
    """
    guild_id = 202405280031
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        
        output_0 = automation_configuration.get_saver()
        output_1 = automation_configuration.get_saver()
        vampytest.assert_is(output_0, output_1)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


def test__AutomationConfiguration__from_entry():
    """
    Tests whether ``AutomationConfiguration.from_entry`` works as intended.
    """
    guild_id = 202405280032
    
    try:
        community_message_moderation_availability_duration = 3605
        community_message_moderation_down_vote_emoji_id = BUILTIN_EMOJIS['red_heart'].id
        community_message_moderation_enabled = True
        community_message_moderation_log_enabled = True
        community_message_moderation_log_channel_id = 202405280033
        community_message_moderation_up_vote_emoji_id = BUILTIN_EMOJIS['green_heart'].id
        community_message_moderation_vote_threshold = 6
        entry_id = 1222222222222222
        farewell_channel_id = 202407140002
        farewell_enabled = True
        farewell_style_name = 'flandre'
        log_emoji_channel_id = 202405280034
        log_emoji_enabled = True
        log_mention_channel_id = 202405280035
        log_mention_enabled = True
        log_satori_auto_start = True
        log_satori_channel_id = 202405280036
        log_satori_enabled = True
        log_sticker_channel_id = 202405280037
        log_sticker_enabled = True
        log_user_channel_id = 202405280038
        log_user_enabled = True
        reaction_copy_enabled = True
        reaction_copy_flags = 12
        reaction_copy_role_id = 202405280039
        touhou_feed_enabled = True
        welcome_channel_id = 202405280040
        welcome_enabled = True
        welcome_reply_buttons_enabled = True
        welcome_style_name = 'yoshika'
        
        entry = {
            'community_message_moderation_availability_duration': community_message_moderation_availability_duration,
            'community_message_moderation_down_vote_emoji_id': community_message_moderation_down_vote_emoji_id,
            'community_message_moderation_enabled': community_message_moderation_enabled,
            'community_message_moderation_log_enabled': community_message_moderation_log_enabled,
            'community_message_moderation_log_channel_id': community_message_moderation_log_channel_id,
            'community_message_moderation_up_vote_emoji_id': community_message_moderation_up_vote_emoji_id,
            'community_message_moderation_vote_threshold': community_message_moderation_vote_threshold,
            'id': entry_id,
            'farewell_channel_id': farewell_channel_id,
            'farewell_enabled': farewell_enabled,
            'farewell_style_name': farewell_style_name,
            'guild_id': guild_id,
            'log_emoji_channel_id': log_emoji_channel_id,
            'log_emoji_enabled': log_emoji_enabled,
            'log_mention_channel_id': log_mention_channel_id,
            'log_mention_enabled': log_mention_enabled,
            'log_satori_auto_start': log_satori_auto_start,
            'log_satori_channel_id': log_satori_channel_id,
            'log_satori_enabled': log_satori_enabled,
            'log_sticker_channel_id': log_sticker_channel_id,
            'log_sticker_enabled': log_sticker_enabled,
            'log_user_channel_id': log_user_channel_id,
            'log_user_enabled': log_user_enabled,
            'reaction_copy_enabled': reaction_copy_enabled,
            'reaction_copy_flags': reaction_copy_flags,
            'reaction_copy_role_id': reaction_copy_role_id,
            'touhou_feed_enabled': touhou_feed_enabled,
            'welcome_channel_id': welcome_channel_id,
            'welcome_enabled': welcome_enabled,
            'welcome_reply_buttons_enabled': welcome_reply_buttons_enabled,
            'welcome_style_name': welcome_style_name,
        }
        
        automation_configuration = AutomationConfiguration.from_entry(entry)
        _assert_fields_set(automation_configuration)
        
        # Should auto store in cache
        vampytest.assert_is(AUTOMATION_CONFIGURATIONS.get(guild_id, None), automation_configuration)
        
        vampytest.assert_eq(
            automation_configuration.community_message_moderation_availability_duration,
            community_message_moderation_availability_duration,
        )
        vampytest.assert_eq(
            automation_configuration.community_message_moderation_down_vote_emoji_id,
            community_message_moderation_down_vote_emoji_id,
        )
        vampytest.assert_eq(
            automation_configuration.community_message_moderation_enabled,
            community_message_moderation_enabled,
        )
        vampytest.assert_eq(
            automation_configuration.community_message_moderation_log_enabled,
            community_message_moderation_log_enabled,
        )
        vampytest.assert_eq(
            automation_configuration.community_message_moderation_log_channel_id,
            community_message_moderation_log_channel_id,
        )
        vampytest.assert_eq(
            automation_configuration.community_message_moderation_up_vote_emoji_id,
            community_message_moderation_up_vote_emoji_id,
        )
        vampytest.assert_eq(
            automation_configuration.community_message_moderation_vote_threshold,
            community_message_moderation_vote_threshold,
        )
        vampytest.assert_eq(automation_configuration.entry_id, entry_id)
        vampytest.assert_eq(automation_configuration.farewell_channel_id, farewell_channel_id)
        vampytest.assert_eq(automation_configuration.farewell_enabled, farewell_enabled)
        vampytest.assert_eq(automation_configuration.farewell_style_name, farewell_style_name)
        vampytest.assert_eq(automation_configuration.log_emoji_channel_id, log_emoji_channel_id)
        vampytest.assert_eq(automation_configuration.log_emoji_enabled, log_emoji_enabled)
        vampytest.assert_eq(automation_configuration.log_mention_channel_id, log_mention_channel_id)
        vampytest.assert_eq(automation_configuration.log_mention_enabled, log_mention_enabled)
        vampytest.assert_eq(automation_configuration.log_satori_auto_start, log_satori_auto_start)
        vampytest.assert_eq(automation_configuration.log_satori_channel_id, log_satori_channel_id)
        vampytest.assert_eq(automation_configuration.log_satori_enabled, log_satori_enabled)
        vampytest.assert_eq(automation_configuration.log_sticker_channel_id, log_sticker_channel_id)
        vampytest.assert_eq(automation_configuration.log_sticker_enabled, log_sticker_enabled)
        vampytest.assert_eq(automation_configuration.log_user_channel_id, log_user_channel_id)
        vampytest.assert_eq(automation_configuration.log_user_enabled, log_user_enabled)
        vampytest.assert_eq(automation_configuration.reaction_copy_enabled, reaction_copy_enabled)
        vampytest.assert_eq(automation_configuration.reaction_copy_flags, reaction_copy_flags)
        vampytest.assert_eq(automation_configuration.reaction_copy_role_id, reaction_copy_role_id)
        vampytest.assert_eq(automation_configuration.touhou_feed_enabled, touhou_feed_enabled)
        vampytest.assert_eq(automation_configuration.welcome_channel_id, welcome_channel_id)
        vampytest.assert_eq(automation_configuration.welcome_enabled, welcome_enabled)
        vampytest.assert_eq(automation_configuration.welcome_reply_buttons_enabled, welcome_reply_buttons_enabled)
        vampytest.assert_eq(automation_configuration.welcome_style_name, welcome_style_name)
        
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


def test__AutomationConfiguration__from_entry__cache():
    """
    Tests whether ``AutomationConfiguration.from_entry`` works as intended.
    
    Case: Caching.
    """
    guild_id = 202405290000
    
    try:
        community_message_moderation_availability_duration = 3605
        community_message_moderation_down_vote_emoji_id = BUILTIN_EMOJIS['red_heart'].id
        community_message_moderation_enabled = True
        community_message_moderation_log_enabled = True
        community_message_moderation_log_channel_id = 202405290001
        community_message_moderation_up_vote_emoji_id = BUILTIN_EMOJIS['green_heart'].id
        community_message_moderation_vote_threshold = 6
        entry_id = 1222222222222222
        farewell_channel_id = 202407140003
        farewell_enabled = True
        farewell_style_name = 'flandre'
        log_emoji_channel_id = 202405290002
        log_emoji_enabled = True
        log_mention_channel_id = 202405290003
        log_mention_enabled = True
        log_satori_auto_start = True
        log_satori_channel_id = 202405290004
        log_satori_enabled = True
        log_sticker_channel_id = 202405290005
        log_sticker_enabled = True
        log_user_channel_id = 202405290006
        log_user_enabled = True
        reaction_copy_enabled = True
        reaction_copy_flags = 12
        reaction_copy_role_id = 202405290007
        touhou_feed_enabled = True
        welcome_channel_id = 202405290008
        welcome_enabled = True
        welcome_reply_buttons_enabled = True
        welcome_style_name = 'yoshika'
        
        automation_configuration = AutomationConfiguration(guild_id)
        AUTOMATION_CONFIGURATIONS[guild_id] = automation_configuration
        
        entry = {
            'community_message_moderation_availability_duration': community_message_moderation_availability_duration,
            'community_message_moderation_down_vote_emoji_id': community_message_moderation_down_vote_emoji_id,
            'community_message_moderation_enabled': community_message_moderation_enabled,
            'community_message_moderation_log_enabled': community_message_moderation_log_enabled,
            'community_message_moderation_log_channel_id': community_message_moderation_log_channel_id,
            'community_message_moderation_up_vote_emoji_id': community_message_moderation_up_vote_emoji_id,
            'community_message_moderation_vote_threshold': community_message_moderation_vote_threshold,
            'id': entry_id,
            'farewell_channel_id': farewell_channel_id,
            'farewell_enabled': farewell_enabled,
            'farewell_style_name': farewell_style_name,
            'guild_id': guild_id,
            'log_emoji_channel_id': log_emoji_channel_id,
            'log_emoji_enabled': log_emoji_enabled,
            'log_mention_channel_id': log_mention_channel_id,
            'log_mention_enabled': log_mention_enabled,
            'log_satori_auto_start': log_satori_auto_start,
            'log_satori_channel_id': log_satori_channel_id,
            'log_satori_enabled': log_satori_enabled,
            'log_sticker_channel_id': log_sticker_channel_id,
            'log_sticker_enabled': log_sticker_enabled,
            'log_user_channel_id': log_user_channel_id,
            'log_user_enabled': log_user_enabled,
            'reaction_copy_enabled': reaction_copy_enabled,
            'reaction_copy_flags': reaction_copy_flags,
            'reaction_copy_role_id': reaction_copy_role_id,
            'touhou_feed_enabled': touhou_feed_enabled,
            'welcome_channel_id': welcome_channel_id,
            'welcome_enabled': welcome_enabled,
            'welcome_reply_buttons_enabled': welcome_reply_buttons_enabled,
            'welcome_style_name': welcome_style_name,
        }
        
        output = AutomationConfiguration.from_entry(entry)
        vampytest.assert_is(output, automation_configuration)
        
        vampytest.assert_eq(
            automation_configuration.community_message_moderation_availability_duration,
            community_message_moderation_availability_duration,
        )
        vampytest.assert_eq(
            automation_configuration.community_message_moderation_down_vote_emoji_id,
            community_message_moderation_down_vote_emoji_id,
        )
        vampytest.assert_eq(
            automation_configuration.community_message_moderation_enabled,
            community_message_moderation_enabled,
        )
        vampytest.assert_eq(
            automation_configuration.community_message_moderation_log_enabled,
            community_message_moderation_log_enabled,
        )
        vampytest.assert_eq(
            automation_configuration.community_message_moderation_log_channel_id,
            community_message_moderation_log_channel_id,
        )
        vampytest.assert_eq(
            automation_configuration.community_message_moderation_up_vote_emoji_id,
            community_message_moderation_up_vote_emoji_id,
        )
        vampytest.assert_eq(
            automation_configuration.community_message_moderation_vote_threshold,
            community_message_moderation_vote_threshold,
        )
        vampytest.assert_eq(automation_configuration.entry_id, entry_id)
        vampytest.assert_eq(automation_configuration.farewell_channel_id, farewell_channel_id)
        vampytest.assert_eq(automation_configuration.farewell_enabled, farewell_enabled)
        vampytest.assert_eq(automation_configuration.farewell_style_name, farewell_style_name)
        vampytest.assert_eq(automation_configuration.log_emoji_channel_id, log_emoji_channel_id)
        vampytest.assert_eq(automation_configuration.log_emoji_enabled, log_emoji_enabled)
        vampytest.assert_eq(automation_configuration.log_mention_channel_id, log_mention_channel_id)
        vampytest.assert_eq(automation_configuration.log_mention_enabled, log_mention_enabled)
        vampytest.assert_eq(automation_configuration.log_satori_auto_start, log_satori_auto_start)
        vampytest.assert_eq(automation_configuration.log_satori_channel_id, log_satori_channel_id)
        vampytest.assert_eq(automation_configuration.log_satori_enabled, log_satori_enabled)
        vampytest.assert_eq(automation_configuration.log_sticker_channel_id, log_sticker_channel_id)
        vampytest.assert_eq(automation_configuration.log_sticker_enabled, log_sticker_enabled)
        vampytest.assert_eq(automation_configuration.log_user_channel_id, log_user_channel_id)
        vampytest.assert_eq(automation_configuration.log_user_enabled, log_user_enabled)
        vampytest.assert_eq(automation_configuration.reaction_copy_enabled, reaction_copy_enabled)
        vampytest.assert_eq(automation_configuration.reaction_copy_flags, reaction_copy_flags)
        vampytest.assert_eq(automation_configuration.reaction_copy_role_id, reaction_copy_role_id)
        vampytest.assert_eq(automation_configuration.touhou_feed_enabled, touhou_feed_enabled)
        vampytest.assert_eq(automation_configuration.welcome_channel_id, welcome_channel_id)
        vampytest.assert_eq(automation_configuration.welcome_enabled, welcome_enabled)
        vampytest.assert_eq(automation_configuration.welcome_reply_buttons_enabled, welcome_reply_buttons_enabled)
        vampytest.assert_eq(automation_configuration.welcome_style_name, welcome_style_name)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


@vampytest.skip_if(DB_ENGINE is not None)
async def test__AutomationConfiguration__delete():
    """
    Tests whether ``AutomationConfiguration.delete`` works as intended.
    
    This function is a coroutine.
    """
    guild_id = 202405290010
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        AUTOMATION_CONFIGURATIONS[guild_id] = automation_configuration
        
        vampytest.assert_is(automation_configuration.saver, None)
        vampytest.assert_is_not(AUTOMATION_CONFIGURATIONS.get(guild_id, None), None)
        
        automation_configuration.delete()
        
        vampytest.assert_is_not(automation_configuration.saver, None)
        vampytest.assert_is(AUTOMATION_CONFIGURATIONS.get(guild_id, None), None)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_is(automation_configuration.saver, None)
        vampytest.assert_is(AUTOMATION_CONFIGURATIONS.get(guild_id, None), None)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


@vampytest.skip_if(DB_ENGINE is not None)
async def test__AutomationConfiguration__set__add_field():
    """
    Tests whether ``AutomationConfiguration.set`` works as intended.
    
    This function is a coroutine.
    
    Case: Add field.
    """
    guild_id = 202405290009
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        
        vampytest.assert_is(automation_configuration.saver, None)
        vampytest.assert_is(AUTOMATION_CONFIGURATIONS.get(guild_id, None), None)
        vampytest.assert_eq(automation_configuration.touhou_feed_enabled, False)
        
        automation_configuration.set('touhou_feed_enabled', True)
        
        vampytest.assert_eq(automation_configuration.touhou_feed_enabled, True)
        vampytest.assert_is_not(automation_configuration.saver, None)
        vampytest.assert_eq(automation_configuration.saver.modified_fields, {'touhou_feed_enabled': True})
        vampytest.assert_is(AUTOMATION_CONFIGURATIONS.get(guild_id, None), None)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_eq(automation_configuration.touhou_feed_enabled, True)
        vampytest.assert_is(automation_configuration.saver, None)
        vampytest.assert_is(AUTOMATION_CONFIGURATIONS.get(guild_id, None), None)
        
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass


@vampytest.skip_if(DB_ENGINE is not None)
async def test__AutomationConfiguration__set__add_field():
    """
    Tests whether ``AutomationConfiguration.set`` works as intended.
    
    This function is a coroutine.
    
    Case: remove field.
    """
    guild_id = 202405290012
    
    try:
        automation_configuration = AutomationConfiguration(guild_id)
        AUTOMATION_CONFIGURATIONS[guild_id] = automation_configuration
        automation_configuration.touhou_feed_enabled = True
        
        vampytest.assert_is(automation_configuration.saver, None)
        vampytest.assert_is_not(AUTOMATION_CONFIGURATIONS.get(guild_id, None), None)
        
        automation_configuration.set('touhou_feed_enabled', False)
        
        vampytest.assert_eq(automation_configuration.touhou_feed_enabled, False)
        vampytest.assert_is_not(automation_configuration.saver, None)
        vampytest.assert_is(AUTOMATION_CONFIGURATIONS.get(guild_id, None), None)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_is(automation_configuration.saver, None)
        vampytest.assert_is(AUTOMATION_CONFIGURATIONS.get(guild_id, None), None)
    
    finally:
        try:
            del AUTOMATION_CONFIGURATIONS[guild_id]
        except KeyError:
            pass
