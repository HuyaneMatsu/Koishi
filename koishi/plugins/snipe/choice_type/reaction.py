__all__ = ()

from hata import StringSelectOption
from scarletio import class_property, copy_docs

from .emoji import ChoiceTypeEmoji

from ..constants import BUTTON_SNIPE_DETAILS_REACTION


@copy_docs(ChoiceTypeEmoji)
class ChoiceTypeReaction(ChoiceTypeEmoji):
    __slots__ = ()
    
    @class_property
    def name(cls):
        return 'reaction'
    
    
    @class_property
    def prefix(cls):
        return 'r'
    
    
    @class_property
    def button_details_enabled(cls):
        return BUTTON_SNIPE_DETAILS_REACTION
    
    
    @classmethod
    def select_option_builder(cls, entity):
        return StringSelectOption(cls._create_emoji_option_value(entity), entity.name, entity)
