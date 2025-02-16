__all__ = ()

from hata import Embed

from ...bot_utils.constants import COLOR__KOISHI_HELP, GUILD__SUPPORT

from .listing import RULES


def _build_single_rule_into(rule_index, title, description_builder, into):
    """
    Builds the description of single single rule.
    
    Parameters
    ----------
    rule_index : `int`
        The rule's index.
    
    title : `str`
        The rule's title.
    
    description_builder : `FunctionType`
        Function that creates the description of the rule.
    
    into : `list<str>`
        List to build into.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append('**')
    into.append(str(rule_index))
    into.append('\\.')
    into.append(title)
    into.append('**\n')
    into.append(description_builder())
    return into


def build_embed_rules_all():
    """
    Builds an embed showing all the rules.
    
    Returns
    -------
    embed : ``Embed``
    """
    description_parts = []
    for rule_index, (title, description_builder) in enumerate(RULES):
        description_parts = _build_single_rule_into(rule_index, title, description_builder, description_parts)
        description_parts.append('\n\n')
    
    description_parts.append(
        'If ever in doubt about rules, follow [Discord\'s guidelines](https://discord.com/guidelines).'
    )
    
    description = ''.join(description_parts)
    description_parts = None
    
    return Embed(
        f'Rules of {GUILD__SUPPORT.name}:',
        description,
        color = COLOR__KOISHI_HELP,
    )


def build_embed_rules_single(rule_index):
    """
    Builds an embed showing a single rule.
    
    Parameters
    ----------
    rule_index : `int`
        The index of the rule.
    
    Returns
    -------
    embed : ``Embed``
    """
    try:
        title, description_builder = RULES[rule_index]
    except LookupError:
        description = 'There is no such a rule.'
    else:
        description = ''.join(_build_single_rule_into(rule_index, title, description_builder, []))
    
    return Embed(
        f'Rule {rule_index} of {GUILD__SUPPORT.name}:',
        description,
        color = COLOR__KOISHI_HELP,
    )
