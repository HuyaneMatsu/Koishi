__all__ = (
    'add_modification_embed_field', 'add_other_balance_modification_embed_field',
    'add_self_balance_modification_embed_field'
)

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from .constants import COLOR_CODE_GREEN, COLOR_CODE_RED, COLOR_CODE_RESET


def add_self_balance_modification_embed_field(embed, balance, modification):
    """
    Adds a self balance modification filed to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        Embed to add field to.
    
    balance : `int`
        The balance before the action.
    
    modification : `int`
        Balance modification.
    
    Returns
    -------
    embed : ``Embed``
    """
    return add_modification_embed_field(embed, f'Your {EMOJI__HEART_CURRENCY}', balance, modification)


def add_other_balance_modification_embed_field(embed, balance, modification):
    """
    Adds an other balance modification filed to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        Embed to add field to.
    
    balance : `int`
        The balance before the action.
    
    modification : `int`
        Balance modification.
    
    Returns
    -------
    embed : ``Embed``
    """
    return add_modification_embed_field(embed, f'Their {EMOJI__HEART_CURRENCY}', balance, modification)


def add_modification_embed_field(embed, title, balance, modification):
    """
    Adds a balance modification filed to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        Embed to add field to.
    
    title : `str`
        Title to use.
    
    balance : `int`
        The balance before the action.
    
    modification : `int`
        Balance modification.
    
    Returns
    -------
    embed : ``Embed``
    """
    description_parts = ['```ansi\n']
    description_parts.append(str(balance))
    description_parts.append(' ')
    
    if modification > 0:
        highlight = COLOR_CODE_GREEN
    elif modification < 0:
        highlight = COLOR_CODE_RED
    else:
        highlight = None
    
    if (highlight is not None):
        description_parts.append(highlight)
    
    description_parts.append('->')
    
    if (highlight is not None):
        description_parts.append(COLOR_CODE_RESET)
    
    description_parts.append(' ')
    description_parts.append(str(balance + modification))
    description_parts.append('\n```')
    
    return embed.add_field(title, ''.join(description_parts), True)
