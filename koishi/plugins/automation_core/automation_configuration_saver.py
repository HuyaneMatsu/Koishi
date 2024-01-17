__all__ = ()

from scarletio import Task, copy_docs
from hata import KOKORO

from ...bot_utils.models import DB_ENGINE, AUTOMATION_CONFIGURATION_TABLE, automation_configuration_model


class AutomationConfigurationSaver:
    """
    Used to save automation configuration.
    
    Attributes
    ----------
    automation_configuration : ``AutomationConfiguration``
        The automation configuration to save.
    
    ensured_for_deletion : `bool`
        Whether the entry should be deleted.
    
    modified_fields : `None`, `dict` of (`str`, `object`) items
        The fields to modify.
    
    running : `bool`
        Whether the saver is already running.
    """
    __slots__ = ('automation_configuration', 'ensured_for_deletion', 'modified_fields', 'running')
    
    def __new__(cls, automation_configuration):
        """
        Creates a new automation configuration saver.
        
        Parameters
        ----------
        automation_configuration : ``AutomationConfiguration``
            The automation configuration to save.
        """
        self = object.__new__(cls)
        self.automation_configuration = automation_configuration
        self.ensured_for_deletion = False
        self.modified_fields = None
        self.running = False
        return self
    
    
    def __repr__(self):
        """Returns the representation of the automation configuration saver."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' automation_configuration = ')
        repr_parts.append(repr(self.automation_configuration))
        
        running = self.running
        if running:
            repr_parts.append(', running = ')
            repr_parts.append(repr(running))
        
        ensured_for_deletion = self.ensured_for_deletion
        if ensured_for_deletion:
            repr_parts.append(', ensured_for_deletion = ')
            repr_parts.append(repr(ensured_for_deletion))
        
        modified_fields = self.modified_fields
        if (modified_fields is not None):
            repr_parts.append(', modified_fields = ')
            repr_parts.append(repr(modified_fields))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def add_modification(self, field_name, field_value):
        """
        Adds a new modification.
        
        Parameters
        ----------
        field_name : `str`
            The modified field.
        field_value : `object`
            The field's new value.
        """
        modified_fields = self.modified_fields
        if (modified_fields is None):
            modified_fields = {}
            self.modified_fields = modified_fields
        
        modified_fields[field_name] = field_value
    
    
    def ensure_deletion(self):
        """
        Ensures to delete the entry.
        """
        self.ensured_for_deletion = True
    
    
    def begin(self):
        """
        Begins saving.
        """
        if self.running:
            return
        
        self.running = True
        Task(KOKORO, self.run())
    
    
    def is_modified(self):
        """
        Returns whether the saver was modified.
        """
        return self.ensured_for_deletion or (self.modified_fields is not None)
    
    
    async def run(self):
        """
        Runs the automation configuration saver.
        
        This method is a coroutine.
        """
        automation_configuration = self.automation_configuration
        try:
            async with DB_ENGINE.connect() as connector:
                
                entry_id = automation_configuration.entry_id
                    
                while self.is_modified():
                    
                    if self.ensured_for_deletion:
                        if entry_id != -1:
                            await connector.execute(
                                AUTOMATION_CONFIGURATION_TABLE.delete().where(
                                    automation_configuration_model.id == entry_id,
                                )
                            )
                            
                            automation_configuration.entry_id = -1
                        
                        # We done!
                        return
                    
                    
                    modified_fields = self.modified_fields
                    if (modified_fields is not None):
                        self.modified_fields = None
                        
                        if entry_id == -1:
                            response = await connector.execute(
                                AUTOMATION_CONFIGURATION_TABLE.insert().values(
                                    guild_id = automation_configuration.guild_id,
                                    
                                    community_message_moderation_availability_duration = (
                                        automation_configuration.community_message_moderation_availability_duration
                                    ),
                                    community_message_moderation_down_vote_emoji_id = (
                                        automation_configuration.community_message_moderation_down_vote_emoji_id
                                    ),
                                    community_message_moderation_enabled = (
                                        automation_configuration.community_message_moderation_enabled
                                    ),
                                    community_message_moderation_up_vote_emoji_id = (
                                        automation_configuration.community_message_moderation_up_vote_emoji_id
                                    ),
                                    community_message_moderation_vote_threshold = (
                                        automation_configuration.community_message_moderation_vote_threshold
                                    ),
                                    
                                    log_emoji_channel_id = automation_configuration.log_emoji_channel_id,
                                    log_mention_channel_id = automation_configuration.log_mention_channel_id,
                                    log_sticker_channel_id = automation_configuration.log_sticker_channel_id,
                                    log_user_channel_id = automation_configuration.log_user_channel_id,
                                    
                                    log_satori_channel_id = automation_configuration.log_satori_channel_id,
                                    log_satori_auto_start = automation_configuration.log_satori_auto_start,
                                    
                                    reaction_copy_enabled = automation_configuration.reaction_copy_enabled,
                                    reaction_copy_role_id = automation_configuration.reaction_copy_role_id,
                                    
                                    touhou_feed_enabled = automation_configuration.touhou_feed_enabled,
                                    
                                    welcome_channel_id = automation_configuration.welcome_channel_id,
                                    welcome_reply_buttons_enabled = (
                                        automation_configuration.welcome_reply_buttons_enabled
                                    ),
                                    welcome_style_name = automation_configuration.welcome_style_name,
                                ).returning(
                                    automation_configuration_model.id,
                                )
                            )
                            
                            result = await response.fetchone()
                            entry_id = result[0]
                            automation_configuration.entry_id = entry_id
                        
                        else:
                            await connector.execute(
                                AUTOMATION_CONFIGURATION_TABLE.update(
                                    automation_configuration_model.id == entry_id,
                                ).values(
                                    **modified_fields
                                )
                            )
                        
                        continue
                    
                    # No more cases
                    continue
        finally:
            self.running = False
            automation_configuration.saver = None
    
    
    # Do nothing if we do not have DB
    if DB_ENGINE is None:
        @copy_docs(run)
        async def run(self):
            self.running = False
            self.automation_configuration.saver = None
