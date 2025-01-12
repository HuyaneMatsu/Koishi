__all__ = ()

from itertools import islice

from hata import Embed

from ...bot_utils.constants import EMOJI__HEART_CURRENCY, COLOR__GAMBLING

from .constants import BET_MIN, CARD_NUMBERS, CARD_TYPES, GAME_21_EMOJI_ENTER, PLAYERS_MAX
from .helpers import is_draw


def build_join_description(users, guild, amount, ask_to_join):
    """
    Builds join embed description.
    
    Parameters
    ----------
    users : `list<ClientUserBase>`
        The joined users.
    guild : `None | Guild`
        The respective guild where the game is.
    amount : `int`
        Bet amount.
    ask_to_join : `bool`
        Whether the embed should ask the users to join.
    
    Returns
    -------
    description : `str`
    """
    description_parts = [
        'Bet amount: ', str(amount), ' ', EMOJI__HEART_CURRENCY.as_emoji, '\n'
        'Creator: ', users[0].name_at(guild),
    ]
    
    if len(users) > 1:
        description_parts.append('\n\nJoined users:')
        for user in islice(users, 1, None):
            description_parts.append('\n')
            description_parts.append(user.name_at(guild))
    
    if ask_to_join:
        description_parts.append('\n\nClick on ')
        description_parts.append(GAME_21_EMOJI_ENTER.as_emoji)
        description_parts.append(' to join.')
    
    return ''.join(description_parts)


def build_join_embed_base(users, guild, amount, title, ask_to_join):
    """
    Builds join embed base called by other join embed builders..
    
    Parameters
    ----------
    users : `list<ClientUserBase>`
        The joined users.
    guild : `None | Guild`
        The respective guild where the game is.
    amount : `int`
        Bet amount.
    title : `str`
        Embed title.
    ask_to_join : `bool`
        Whether the embed should ask the users to join.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        title,
        build_join_description(users, guild, amount, ask_to_join),
        color = COLOR__GAMBLING,
    )


def build_join_embed(users, guild, amount):
    """
    Creates an embed that asks the users to join the game.
    
    Parameters
    ----------
    users : `list<ClientUserBase>`
        The joined users.
    guild : `None | Guild`
        The respective guild where the game is.
    amount : `int`
        Bet amount.
    
    Returns
    -------
    embed : ``Embed``
    """
    return build_join_embed_base(users, guild, amount, 'Game 21 multi-player', True).add_footer(
        f'Times out after 5 minutes. Max {PLAYERS_MAX!s} players allowed.',
    )


def build_join_embed_cancelled(users, guild, amount):
    """
    Creates a join embed for case when its cancelled.
    
    Parameters
    ----------
    users : `list<ClientUserBase>`
        The joined users.
    guild : `None | Guild`
        The respective guild where the game is.
    amount : `int`
        Bet amount.
    
    Returns
    -------
    embed : ``Embed``
    """
    return build_join_embed_base(users, guild, amount, 'Game 21 multi-player cancelled', False).add_footer(
        'Hearts have been refunded.',
    )


def build_join_embed_timed_out(users, guild, amount):
    """
    Creates a join embed for case when its timed out.
    
    Parameters
    ----------
    users : `list<ClientUserBase>`
        The joined users.
    guild : `None | Guild`
        The respective guild where the game is.
    amount : `int`
        Bet amount.
    
    Returns
    -------
    embed : ``Embed``
    """
    return build_join_embed_base(users, guild, amount, 'Game 21 multi-player timed out', False).add_footer(
        'Hearts have been refunded.',
    )


def build_join_embed_game_started(users, guild, amount):
    """
    Creates a join embed when the game started.
    
    Parameters
    ----------
    users : `list<ClientUserBase>`
        The joined users.
    guild : `None | Guild`
        The respective guild where the game is.
    amount : `int`
        Bet amount.
    
    Returns
    -------
    embed : ``Embed``
    """
    return build_join_embed_base(users, guild, amount, 'Game 21 multi-player started', False).add_footer(
        'The results will show up here when everyone is finished.',
    )


def add_hand_fields(embed, hand):
    """
    Adds hand fields to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    hand : ``Hand``
        The hand to add.
    
    Returns
    -------
    embed : ``Embed``
    """
    for round, card in enumerate(hand.cards, 1):
        type_index, number_index = divmod(card, len(CARD_NUMBERS))
        embed.add_field(
            f'Round {round}',
            f'You pulled {CARD_TYPES[type_index]} {CARD_NUMBERS[number_index]}',
        )
    
    return embed


def build_gamble_embed_base(hand, title):
    """
    Builds a gamble embed.
    
    Parameters
    ----------
    hand : ``Hand``
        The hand to build with.
    title : `str`
        The title to add.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        title,
        f'You have cards equal to {hand.total!s} weight at your hand.',
        color = COLOR__GAMBLING,
    )
    return add_hand_fields(embed, hand)


def build_gamble_embed(hand, amount):
    """
    Builds a gamble embed.
    
    Parameters
    ----------
    hand : ``Hand``
        The hand to build with.
    amount : `int`
        The gambled amount.
    
    Returns
    -------
    embed : ``Embed``
    """
    return build_gamble_embed_base(hand, f'How to gamble {amount!s} {EMOJI__HEART_CURRENCY}')


def build_gamble_after_embed(hand, amount):
    """
    Builds a gamble after embed which is shown after a multiplayer game is finished.
    
    Parameters
    ----------
    hand : ``Hand``
        The hand to build with.
    amount : `int`
        The gambled amount.
    
    Returns
    -------
    embed : ``Embed``
    """
    return build_gamble_embed_base(hand, f'Gambled {amount!s} {EMOJI__HEART_CURRENCY}').add_footer(
        'Wait till all the player finishes the game and the winner will be announced!',
    )


def build_gamble_timeout_embed(hand, amount):
    """
    Builds a gamble timeout embed which is shown after a user timed out.
    
    Parameters
    ----------
    hand : ``Hand``
        The hand to build with.
    amount : `int`
        The gambled amount.
    
    Returns
    -------
    embed : ``Embed``
    """
    return build_gamble_embed_base(hand, f'Gambled {amount!s} {EMOJI__HEART_CURRENCY} and timed out')


def build_done_field_description(hand):
    """
    Builds a done description.
    
    Parameters
    ----------
    hand : ``Hand``
        The hand to create done description for.
    
    Returns
    -------
    description : `str`
    """
    cards = hand.cards
    card_count = len(cards)
    
    # should not happen
    if not card_count:
        return '_ _'
    
    description_parts = []
    
    index = 0
    while True:
        card = cards[index]
        index += 1
        
        type_index, number_index = divmod(card, len(CARD_NUMBERS))
        description_parts.append('Round ')
        description_parts.append(str(index))
        description_parts.append(': ')
        description_parts.append(CARD_TYPES[type_index])
        description_parts.append(' ')
        description_parts.append(CARD_NUMBERS[number_index])
        
        if index == card_count:
            break
        
        description_parts.append('\n')
    
    return ''.join(description_parts)


def add_done_field(embed, user, guild, hand):
    """
    Adds a done field to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    user : ``ClientUserBase``
        The user who owns the hand.
    guild : `None | Guild`
        The respective guild where the game is.
    hand : ``Hand``
        The hand to add its done field for.
    
    Returns
    -------
    embed : ``Embed``
    """
    return embed.add_field(
        f'{user.name_at(guild)!s}\'s\ncards\' weight: {hand.total!s}',
        build_done_field_description(hand),
        inline = True,
    )


def build_join_succeeded_embed():
    """
    Builds a game join embed.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        '21 multi-player game joined.',
        color = COLOR__GAMBLING,
    )


def build_join_failed_embed_max_players():
    """
    Builds a failed to join game embed for the case when the game is full.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Ohoho',
        f'Max {PLAYERS_MAX!s} players are allowed.',
        color = COLOR__GAMBLING,
    )


def build_join_failed_embed_not_enough_hearts(expected, available, me):
    """
    Builds a failed to join game embed for the case when the user does not have enough hearts.
    
    Parameters
    ----------
    expected : `int`
        The expected hearts to have.
    
    available : `int`
        The available hearts of a user.
    
    me : `bool`
        Whether the client is checking itself.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        ('Oh snap!' if me else 'Ohoho'),
        (
            f'{"I" if me else "You"} must have at least {expected!s} available {EMOJI__HEART_CURRENCY} to join.\n'
            f'{"I" if me else "You"} have {available!s} {EMOJI__HEART_CURRENCY}.'
        ),
        color = COLOR__GAMBLING,
    )


def build_join_failed_embed_already_in_game():
    """
    Builds a failed to join game embed for the case when the user is already in a game.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Ohoho',
        'You are already in a game.',
        color = COLOR__GAMBLING,
    )


def build_join_failed_embed_bet_too_low():
    """
    Builds a failed to join game embed for the case when the bet is too low.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Ohoho',
        f'You must bet at least {BET_MIN!s} {EMOJI__HEART_CURRENCY}',
        color = COLOR__GAMBLING,
    )


def build_join_failed_embed_not_enough_users_to_start():
    """
    Builds a join game embed for the case when there are not enough joined users to start it.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Ohoho',
        'There must be at least 1 other user in game to start it.',
        color = COLOR__GAMBLING,
    )


def build_leave_succeeded_embed():
    """
    Builds a game leave embed.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        '21 multi-player game left.',
        color = COLOR__GAMBLING,
    )


def build_end_embed_single_player_title(player_win, amount):
    """
    Builds end embed title for single player.
    
    Parameters
    ----------
    player_win : `int`
        Whether the player won.
    amount : `int`
        The amount lost or won.
    
    Returns
    -------
    title : `str`
    """
    title_parts = ['How to ']
    
    if player_win == 0:
        part = 'draw'
    elif player_win > 0:
        part = 'win'
    else:
        part = 'lose'
    
    title_parts.append(part)
    
    if player_win:
        title_parts.append(' ')
        title_parts.append(str(amount))
        title_parts.append(' ')
        title_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
    
    return ''.join(title_parts)


def build_end_embed_single_player(session, player_user, player_bot, player_win):
    """
    Builds end embed for single player.
    
    Parameters
    ----------
    session : ``Session``
        Game session.
    player_user : ``Player``
        The user's player.
    player_bot : ``Player``
        Bot player.
    player_win : `int`
        Whether the player won.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        build_end_embed_single_player_title(player_win, session.amount),
        color = COLOR__GAMBLING,
    )
    add_done_field(embed, player_user.user, session.guild, player_user.hand)
    add_done_field(embed, player_bot.user, session.guild, player_bot.hand)
    
    return embed


def build_user_listing_description(users, guild):
    """
    Builds a user listing description.
    
    Parameters
    ----------
    users : `list<ClientUserBase>`
        The users to list.
    guild : `None | Guild`
        The respective guild.
    
    Returns
    -------
    description : `str`
    """
    # Should not happen
    if not users:
        return '_ _'
    
    return '\n'.join(user.name_at(guild) for user in users)


def build_end_embed_multi_player(session, players, winners, losers):
    """
    Builds end embed for multi player.
    
    Parameters
    ----------
    session : ``Session``
        Game session.
    players : `list<Player>`
        All player.
    winners : `None | list<Player>`
        Winning players.
    losers : `None | list<Player>`
        Losing players.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        'Game ended',
        f'Total bet amount: {session.amount * len(players)} {EMOJI__HEART_CURRENCY}',
        color = COLOR__GAMBLING,
    )
    
    if is_draw(winners, losers):
        embed.add_field(
            'Draw',
            build_user_listing_description([player.user for player in players], session.guild),
        )
    
    else:
        embed.add_field(
            'Winners',
            build_user_listing_description([player.user for player in winners], session.guild),
        )
        
        embed.add_field(
            'Losers',
            build_user_listing_description([player.user for player in losers], session.guild),
        )
    
    for player in players:
        embed = add_done_field(embed, player.user, session.guild, player.hand)
    
    return embed
