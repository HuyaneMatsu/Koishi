__all__ = (
    'build_component_question_stat_upgrade_purchase_other', 'build_component_question_stat_upgrade_purchase_self'
)

from hata.ext.slash import Button, Row

from .constants import (
    CUSTOM_ID_STAT_UPGRADE_PURCHASE_CANCEL_OTHER_BUILDER, CUSTOM_ID_STAT_UPGRADE_PURCHASE_CANCEL_SELF_BUILDER,
    CUSTOM_ID_STAT_UPGRADE_PURCHASE_CONFIRM_OTHER_BUILDER, CUSTOM_ID_STAT_UPGRADE_PURCHASE_CONFIRM_SELF_BUILDER,
    EMOJI_NO, EMOJI_YES
)


def build_component_question_stat_upgrade_purchase_self(stat_index):
    """
    Builds a (row) component to confirm stat upgrade for yourself.
    
    Parameters
    ----------
    stat_index : `int`
        The stat's index.
    
    Returns
    -------
    component : ``Component``
    """
    return Row(
        Button(
            'Yes',
            EMOJI_YES,
            custom_id = CUSTOM_ID_STAT_UPGRADE_PURCHASE_CONFIRM_SELF_BUILDER(stat_index),
        ),
        Button(
            'No',
            EMOJI_NO,
            custom_id = CUSTOM_ID_STAT_UPGRADE_PURCHASE_CANCEL_SELF_BUILDER(stat_index),
        ),
    )


def build_component_question_stat_upgrade_purchase_other(user_id, stat_index):
    """
    Builds a (row) component to confirm stat upgrade for someone else.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    stat_index : `int`
        The stat's index.
    
    Returns
    -------
    component : ``Component``
    """
    return Row(
        Button(
            'Yes',
            EMOJI_YES,
            custom_id = CUSTOM_ID_STAT_UPGRADE_PURCHASE_CONFIRM_OTHER_BUILDER(user_id, stat_index),
        ),
        Button(
            'No',
            EMOJI_NO,
            custom_id = CUSTOM_ID_STAT_UPGRADE_PURCHASE_CANCEL_OTHER_BUILDER(user_id, stat_index),
        ),
    )
