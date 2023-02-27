__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .component_builder_select_option import (
    select_option_builder_emoji, select_option_builder_reaction, select_option_builder_sticker
)
from .component_translate_tables import (
    SELECT_EMOJI_DISABLED, SELECT_EMOJI_INSIDE, SELECT_EMOJI_OUTSIDE, SELECT_STICKER_DISABLED, SELECT_STICKER_INSIDE,
    SELECT_STICKER_OUTSIDE
)
from .constants import (
    BUTTON_SNIPE_ACTIONS_EMOJI, BUTTON_SNIPE_ACTIONS_STICKER, BUTTON_SNIPE_DETAILS_EMOJI, BUTTON_SNIPE_DETAILS_REACTION,
    BUTTON_SNIPE_DETAILS_STICKER
)
from .embed_builder_common import embed_builder_emoji, embed_builder_reaction, embed_builder_sticker


class ChoiceType(RichAttributeErrorBaseType):
    """
    Represents a ``Choice``'s type.
    
    Attributes
    ----------
    button_actions_enabled : ``Component``
        Enabled `actions` button.
    
    button_details_enabled : ``Component``
        Enabled `details` button.
    
    embed_builder : `CoroutineFunctionType`
        An embed builder to build the response with.
        
        The accepted implementations are:
        - `(Client, InteractionEvent, Emoji, None | str, bool) -> Coroutine<Embed>`
        - `(Client, InteractionEvent, Sticker, None | str, bool) -> Coroutine<Embed>`
        
        Actual implementations:
        - ``embed_builder_emoji``
        - ``embed_builder_reaction``
        - ``embed_builder_sticker``
    
    select_option_builder : `FunctionType`
        Select option builder used when displaying multiple choices.
        
        The accepted implementations are:
        - `(Emoji) -> StringSelectOption`
        - `(Sticker) -> StringSelectOption`
        
        Actual implementations:
        - ``select_option_builder_emoji``
        - ``select_option_builder_reaction``
        - ``select_option_builder_sticker``
        
    name : `str`
        The choice's name.
    
    select_option_builder : `str`
        Custom id used for the select as required.
    
    select_table_disabled : `dict` of (`str`, ``Component``) items
        Component translation table used if cannot execute actions on the entity.
    
    select_table_inside : `dict` of (`str`, ``Component``) items
        Component translation table used if the respective entity is inside of the guild.
    
    select_table_outside : `dict` of (`str`, ``Component``) items
        Component translation table used if the respective entity is outside of the guild.
    """
    __slots__ = (
        'name', 'embed_builder', 'button_details_enabled', 'button_actions_enabled', 'select_option_builder',
        'select_table_disabled', 'select_table_inside', 'select_table_outside',
    )
    
    def __init__(
        self,
        name,
        embed_builder,
        select_option_builder,
        button_details_enabled,
        button_actions_enabled,
        select_table_inside,
        select_table_outside,
        select_table_disabled,
    ):
        """
        Creates a new choice type.
        
        Parameters
        ----------
        name : `str`
            The choice's name.
        
        embed_builder : `CoroutineFunctionType`
            An embed builder to build the response with.
        
        select_option_builder : `FunctionType`
            Select option builder used when displaying multiple choices.
        
        button_details_enabled : ``Component``
            Enabled `details` button.
        
        button_actions_enabled : ``Component``
            Enabled `actions` button.
        
        select_table_inside : `dict` of (`str`, ``Component``) items
            Component translation table used if the respective entity is inside of the guild.
        
        select_table_outside : `dict` of (`str`, ``Component``) items
            Component translation table used if the respective entity is outside of the guild.
        
        select_table_disabled : `dict` of (`str`, ``Component``) items
            Component translation table used if cannot execute actions on the entity.
        """
        self.button_actions_enabled = button_actions_enabled
        self.button_details_enabled = button_details_enabled
        self.embed_builder = embed_builder
        self.name = name
        self.select_option_builder = select_option_builder
        self.select_table_disabled = select_table_disabled
        self.select_table_inside = select_table_inside
        self.select_table_outside = select_table_outside
    
    
    def __repr__(self):
        """Returns the choice type's representation"""
        return f'<{self.__class__.__name__} {self.name}>'


CHOICE_TYPE_EMOJI = ChoiceType(
    'emoji',
    embed_builder_emoji,
    select_option_builder_emoji,
    BUTTON_SNIPE_DETAILS_EMOJI,
    BUTTON_SNIPE_ACTIONS_EMOJI,
    SELECT_EMOJI_INSIDE,
    SELECT_EMOJI_OUTSIDE,
    SELECT_EMOJI_DISABLED,
)
CHOICE_TYPE_REACTION = ChoiceType(
    'reaction',
    embed_builder_reaction,
    select_option_builder_reaction,
    BUTTON_SNIPE_DETAILS_REACTION,
    BUTTON_SNIPE_ACTIONS_EMOJI,
    SELECT_EMOJI_INSIDE,
    SELECT_EMOJI_OUTSIDE,
    SELECT_EMOJI_DISABLED,
)
CHOICE_TYPE_STICKER = ChoiceType(
    'sticker',
    embed_builder_sticker,
    select_option_builder_sticker,
    BUTTON_SNIPE_DETAILS_STICKER,
    BUTTON_SNIPE_ACTIONS_STICKER,
    SELECT_STICKER_INSIDE,
    SELECT_STICKER_OUTSIDE,
    SELECT_STICKER_DISABLED,
)


class Choice(RichAttributeErrorBaseType):
    """
    Represents a choice.
    
    Attributes
    ----------
    entity : ``Emoji``, ``Sticker``
        The entity's type.
    type : ``ChoiceType``
        The choice's type.
    """
    __slots__ = ('entity', 'type')
    
    def __init__(self, choice_type, entity):
        """
        Parameters
        ----------
        choice_type : ``ChoiceType``
            The choice's type.
        entity : ``Emoji``, ``Sticker``
            The entity's type.
        """
        self.type = choice_type
        self.entity = entity
    
    
    def __repr__(self):
        """Returns the choice's representation"""
        return f'<{self.__class__.__name__} ({self.type.name}) entity = {self.entity!r}>'
    
    
    def __len__(self):
        """Returns the choice's length. Helper for unpacking."""
        return 2
    
    
    def __iter__(self):
        """
        Unpacks the choice.
        
        This method is an iterable generator.
        
        Yields
        ------
        choice_type / entity : ``ChoiceType`` / ``Emoji``, ``Sticker``
        """
        yield self.type
        yield self.entity
