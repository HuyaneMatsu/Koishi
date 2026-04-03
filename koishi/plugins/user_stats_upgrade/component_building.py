__all__ = ()

from hata import InteractionForm, create_text_display

from .content_building import produce_stat_upgrade_confirmation_description
from .custom_ids import CUSTOM_ID_UPGRADE_STATS_CONFIRMATION_BUILDER


def build_confirmation_form(
    stat_housewife,
    stat_cuteness,
    stat_bedroom,
    stat_charm,
    stat_loyalty,
    modify_housewife_by,
    modify_cuteness_by,
    modify_bedroom_by,
    modify_charm_by,
    modify_loyalty_by,
    required_balance,
    target_user,
    guild_id,
):
    """
    Builds stat upgrade confirmation form.
    
    Parameters
    ----------
    stat_housewife : `int`
        The user's current housewife stat.
    
    stat_cuteness : `int`
        The user's current cuteness stat.
    
    stat_bedroom : `int`
        The user's current bedroom stat.
    
    stat_charm : `int`
        The user's current charm stat.
    
    stat_loyalty : `int`
        The user's current loyalty stat.
    
    modify_housewife_by : `int`
        The amount to modify the housewife stat by.
    
    modify_cuteness_by : `int`
        The amount to modify the cuteness stat by.
    
    modify_bedroom_by : `int`
        The amount to modify the bedroom stat by.
    
    modify_charm_by : `int`
        The amount to modify the charm stat by.
    
    modify_loyalty_by : `int`
        The amount to modify the loyalty stat by.
    
    required_balance : `int`
        The required balance for upgrading.
    
    target_user : ``None | ClientUserBase``
        The targeted user if any.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    interaction_form : ``InteractionForm``
    """
    return InteractionForm(
        'Confirm stat upgrading',
        [
            create_text_display(''.join([*produce_stat_upgrade_confirmation_description(
                stat_housewife,
                stat_cuteness,
                stat_bedroom,
                stat_charm,
                stat_loyalty,
                modify_housewife_by,
                modify_cuteness_by,
                modify_bedroom_by,
                modify_charm_by,
                modify_loyalty_by,
                required_balance,
                target_user,
                guild_id,
            )])),
        ],
        CUSTOM_ID_UPGRADE_STATS_CONFIRMATION_BUILDER(
            modify_housewife_by,
            modify_cuteness_by,
            modify_bedroom_by,
            modify_charm_by,
            modify_loyalty_by,
            (0 if target_user is None else target_user.id),
        ),
    )
