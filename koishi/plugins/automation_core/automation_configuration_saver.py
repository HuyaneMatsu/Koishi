__all__ = ()

from scarletio import copy_docs

from ...bot_utils.entry_proxy import EntryProxySaver
from ...bot_utils.models import AUTOMATION_CONFIGURATION_TABLE, automation_configuration_model


class AutomationConfigurationSaver(EntryProxySaver):
    """
    Used to save automation configuration.
    
    Attributes
    ----------
    entry_proxy : ``AutomationConfiguration``
        The automation configuration to save.
    
    ensured_for_deletion : `bool`
        Whether the entry should be deleted.
    
    modified_fields : `None | dict<str, object>`
        The fields to modify.
    
    run_task : `None | Task<.run>`
        Whether the saver is already running.
    """
    __slots__ = ()
    
    @copy_docs(EntryProxySaver._delete_entry)
    async def _delete_entry(self, connector, entry_id):
        await connector.execute(
            AUTOMATION_CONFIGURATION_TABLE.delete().where(
                automation_configuration_model.id == entry_id,
            )
        )
    
    
    @copy_docs(EntryProxySaver._insert_entry)
    async def _insert_entry(self, connector, entry_proxy):
        response = await connector.execute(
            AUTOMATION_CONFIGURATION_TABLE.insert().values(
                guild_id = entry_proxy.guild_id,
                
                community_message_moderation_availability_duration = (
                    entry_proxy.community_message_moderation_availability_duration
                ),
                community_message_moderation_down_vote_emoji_id = (
                    entry_proxy.community_message_moderation_down_vote_emoji_id
                ),
                community_message_moderation_enabled = (
                    entry_proxy.community_message_moderation_enabled
                ),
                community_message_moderation_log_enabled = (
                    entry_proxy.community_message_moderation_log_enabled
                ),
                community_message_moderation_log_channel_id = (
                    entry_proxy.community_message_moderation_log_channel_id
                ),
                community_message_moderation_up_vote_emoji_id = (
                    entry_proxy.community_message_moderation_up_vote_emoji_id
                ),
                community_message_moderation_vote_threshold = (
                    entry_proxy.community_message_moderation_vote_threshold
                ),
                
                farewell_channel_id = entry_proxy.farewell_channel_id,
                farewell_enabled = entry_proxy.farewell_enabled,
                farewell_style_name = entry_proxy.farewell_style_name,
                
                log_emoji_channel_id = entry_proxy.log_emoji_channel_id,
                log_emoji_enabled = entry_proxy.log_emoji_enabled,
                log_mention_channel_id = entry_proxy.log_mention_channel_id,
                log_mention_enabled = entry_proxy.log_mention_enabled,
                log_sticker_channel_id = entry_proxy.log_sticker_channel_id,
                log_sticker_enabled = entry_proxy.log_sticker_enabled,
                log_user_channel_id = entry_proxy.log_user_channel_id,
                log_user_enabled = entry_proxy.log_user_enabled,
                
                log_satori_channel_id = entry_proxy.log_satori_channel_id,
                log_satori_auto_start = entry_proxy.log_satori_auto_start,
                log_satori_enabled = entry_proxy.log_satori_enabled,
                
                reaction_copy_enabled = entry_proxy.reaction_copy_enabled,
                reaction_copy_flags = entry_proxy.reaction_copy_flags,
                reaction_copy_role_id = entry_proxy.reaction_copy_role_id,
                
                touhou_feed_enabled = entry_proxy.touhou_feed_enabled,
                
                welcome_channel_id = entry_proxy.welcome_channel_id,
                welcome_enabled = entry_proxy.welcome_enabled,
                welcome_reply_buttons_enabled = (
                    entry_proxy.welcome_reply_buttons_enabled
                ),
                welcome_style_name = entry_proxy.welcome_style_name,
            ).returning(
                automation_configuration_model.id,
            )
        )
        
        result = await response.fetchone()
        return result[0]
    
    
    @copy_docs(EntryProxySaver._update_entry)
    async def _update_entry(self, connector, entry_id, modified_fields):
        await connector.execute(
            AUTOMATION_CONFIGURATION_TABLE.update(
                automation_configuration_model.id == entry_id,
            ).values(
                **modified_fields
            )
        )
