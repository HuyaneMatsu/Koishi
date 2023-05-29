__all__ = ()

from hata import Embed
from scarletio import RichAttributeErrorBaseType, class_property
from ..constants import BUTTON_SNIPE_ADD_DISABLED, BUTTON_SNIPE_EDIT_DISABLED, BUTTON_SNIPE_REMOVE_DISABLED
from ..embed_builder_base import add_embed_author, add_embed_footer, copy_extra_fields, create_base_embed
from ..helpers import are_actions_allowed_for_entity


class ChoiceTypeBase(RichAttributeErrorBaseType):
    """
    Choice type.
    """
    __slots__ = ()
    
    def __new__(cls):
        raise RuntimeError(f'{cls.__name__} is not instantiable.')
    
    
    @class_property
    def name(cls):
        """
        The choice's name.
        
        Returns
        -------
        name : `str`
        """
        raise NotImplemented
    
    
    @class_property
    def button_actions_enabled(cls):
        """
        Enabled `actions` button.
        
        Returns
        -------
        button_actions_enabled : ``Component``
        """
        raise NotImplemented
    
    
    @class_property
    def button_details_enabled(cls):
        """
        Enabled `details` button.
        
        Returns
        -------
        button_details_enabled : ``Component``
        """
        raise NotImplemented
    
    
    @class_property
    def button_action_add(cls):
        """
        Component triggering adding the entity.
        
        Returns
        -------
        button_action_add : ``Component``
        """
        raise NotImplemented
    
    
    @class_property
    def button_action_edit(cls):
        """
        Component triggering editing the entity.
        
        Returns
        -------
        button_action_edit : ``Component``
        """
        raise NotImplemented
    
    
    @class_property
    def button_action_remove(cls):
        """
        Component triggering removing the entity.
        
        Returns
        -------
        button_action_remove : ``Component``
        """
        raise NotImplemented
    
    
    @class_property
    def select_table_disabled(cls):
        """
        Component translation table used if the respective entity is inside of the guild.
        
        Returns
        -------
        select_table_disabled : `dict` of (`str`, ``Component``) items
        """
        raise NotImplemented
    
    
    @class_property
    def select_table_inside(cls):
        """
        Component translation table used if the respective entity is inside of the guild.
        
        Returns
        -------
        select_table_inside : `dict` of (`str`, ``Component``) items
        """
        raise NotImplemented
    
    
    @class_property
    def select_table_outside(cls):
        """
        Component translation table used if the respective entity is outside of the guild.
        
        Returns
        -------
        select_table_outside : `dict` of (`str`, ``Component``) items
        """
        raise NotImplemented
    
    
    @classmethod
    async def build_embed(cls, entity, client, event, message_jump_url, detailed):
        """
        Builds a generic embed.
        
        This function is a coroutine.
        
        Parameters
        ----------
        entity : ``Emoji``, ``Sticker``
            The entity to build the embed for.
        client : ``Client``
            The client who received the interaction event.
        event : ``InteractionEvent``
            The received interaction event.
        message_jump_url : `None`, `str`
            Jump url to the source message.
        detailed : `bool`
            Whether detailed response should be shown.
        
        Returns
        -------
        embed : ``Embed``
        """
        if detailed:
            await cls.update_entity_details(entity, client)
            embed = cls.build_embed_detailed(entity)
            extra_fields_set = copy_extra_fields(embed, event)
            if extra_fields_set:
                return embed
        
        else:
            embed = create_base_embed(entity, None if entity.url is None else 'Click to open')
            
        add_embed_footer(embed, entity)
        add_embed_author(embed, event, cls.name, message_jump_url)
        return embed
    
    
    @classmethod
    def _create_select_option_value(cls, entity_id, name, animated):
        """
        Creates an option value. Helper method of ``.select_option_builder``.
        
        Parameters
        ----------
        entity_id : `int`
            The entity's identifier. Can differ if the entity is a unicode emoji.
        name : `str`
            The entity's name. Can differ if the entity is a unicode emoji.
            Passed as empty string if the entity is a sticker.
        animated : `str`
            Whether the entity is animated. Emoji only.
            Passed as empty string if the entity is a sticker.
        """
        return f'{cls.name[0]}:{entity_id}:{name}:{animated}'
    
    
    @classmethod
    def select_option_builder(entity):
        """
        Builds a select option for the given emoji.
        
        Parameters
        ----------
        entity : ``Emoji``, ``Sticker`` 
            The entity to create option for.
        
        Returns
        -------
        option : ``StringSelectOption``
        """
        raise NotImplemented
    
    
    @classmethod
    async def update_entity_details(cls, entity, client):
        """
        Updates the entity's details.
        
        This function is a coroutine.
        
        Parameters
        ----------
        entity : ``Emoji``, ``Sticker`` 
            The entity to update for.
        client : ``Client``
            Client to update the entity with.
        """
        raise NotImplemented
    
    
    @classmethod
    def build_embed_detailed(cls, entity):
        """
        Builds a detailed embed.
        
        Parameters
        ----------
        entity : ``Emoji``, ``Sticker`` 
            The entity to build the detailed embed for.
        
        Returns
        -------
        embed : ``Embed``
        """
        raise NotImplemented
    
    
    @classmethod
    def iter_action_components(cls, entity, event):
        """
        Iterates over the action components for the given entity.
        
        Parameters
        ----------
        entity : ``Emoji``, ``Sticker``
            The entity in context.
        event : ``InteractionEvent``
            The received interaction event.
        
        Yields
        ------
        component : ``Component``
        """
        guild_id = event.guild_id
        if (guild_id == 0) or (not are_actions_allowed_for_entity(entity)):
            yield BUTTON_SNIPE_ADD_DISABLED
            yield BUTTON_SNIPE_EDIT_DISABLED
            yield BUTTON_SNIPE_REMOVE_DISABLED
        
        elif (guild_id == entity.guild_id):
            yield BUTTON_SNIPE_ADD_DISABLED
            yield cls.button_action_edit
            yield cls.button_action_remove
        
        else:
            yield cls.button_action_add
            yield BUTTON_SNIPE_EDIT_DISABLED
            yield BUTTON_SNIPE_REMOVE_DISABLED
    
    
    @classmethod
    async def parse_and_get_entity_id_and_entity(cls, client, event):
        """
        Parses the emoji from the event's message and returns it.
        
        This function is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the interaction event.
        event : ``InteractionEvent``
            The received interaction event.
        
        Returns
        -------
        entity_id : `int`
            The entity's identifier. Can be used to remove the entity's choice from select if the entity was not found.
        entity : `None`, ``Emoji``, ``Sticker``
            The back-parsed entity.
        """
        raise NotImplemented
