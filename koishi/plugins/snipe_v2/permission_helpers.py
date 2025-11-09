__all__ = ()


from hata import Emoji, SoundboardSound, Sticker

from .constants import PERMISSION_MASK_EXPRESSION_ADD, PERMISSION_MASK_EXPRESSION_EDIT_OR_DELETE


def _count_checker_none(entity, guild):
    return False


def _count_checker_emoji(emoji, guild):
    emoji_counts = guild.emoji_counts
    used_emoji_count = emoji_counts.normal_animated if emoji.animated else emoji_counts.normal_static
    
    return used_emoji_count < guild.boost_perks.emoji_limit


def _count_checker_emoji_any(emoji, guild):
    emoji_counts = guild.emoji_counts
    emoji_limit = guild.boost_perks.emoji_limit
    return min(emoji_counts.normal_animated, emoji_counts.normal_static) < emoji_limit


def _count_checker_sticker(sticker, guild):
    return len(guild.stickers) < guild.boost_perks.sticker_limit


def _count_checker_soundboard_sound(soundboard_sound, guild):
    soundboard_sounds = guild.soundboard_sounds
    if soundboard_sounds is None:
        soundboard_sounds_count = 0
    else:
        soundboard_sounds_count = len(soundboard_sounds)
    
    return soundboard_sounds_count < guild.boost_perks.sticker_limit


def has_user_required_permissions(guild, user, permission_mask):
    return (guild.permissions_for(user) & permission_mask == permission_mask)


def get_first_client_with_permissions(guild, permission_mask):
    for client in guild.iter_clients():
        if guild.cached_permissions_for(client) & permission_mask == permission_mask:
            return client


def has_user_and_any_client_permission(guild, user, permission_mask):
    if not has_user_required_permissions(guild, user, permission_mask):
        return False
    
    if get_first_client_with_permissions(guild, permission_mask) is None:
        return False
    
    return True


def has_free_entity_spot(entity_type, entity, guild):
    if entity_type is Emoji:
        if entity is None:
            count_checker = _count_checker_emoji_any
        else:
            count_checker = _count_checker_emoji
    
    elif entity_type is Sticker:
        count_checker = _count_checker_sticker
    elif entity_type is SoundboardSound:
        count_checker = _count_checker_soundboard_sound
    else:
        count_checker = _count_checker_none
    
    return count_checker(entity, guild)


def can_add_entity_into_guild(entity_type, entity, guild, user):
    if not has_user_and_any_client_permission(guild, user, PERMISSION_MASK_EXPRESSION_ADD):
        return False
    
    if not has_free_entity_spot(entity_type, entity, guild):
        return False
    
    return True


def can_edit_or_delete_entity_in_guild(guild, user):
    return has_user_and_any_client_permission(guild, user, PERMISSION_MASK_EXPRESSION_EDIT_OR_DELETE)



def can_add_anywhere(entity_type, entity, user):
    """
    Returns whether the entity can be added anywhere by the user.
    
    Parameters
    ----------
    entity_type : ``type<Entity |  Sticker | SoundboardSound>``
        The entity's type to check.
    
    entity : ``None | Emoji | Sticker | SoundboardSound``
        The entity to check.
    
    user : ``ClientUserBase``
        The user in context.
    
    Returns
    -------
    can : `bool`
    """ 
    for guild in user.iter_guilds():
        if can_add_entity_into_guild(entity_type, entity, guild, user):
            return True
    
    return False


def can_edit_or_delete_anywhere(entity, user):
    """
    Returns whether the entity can be edited or deleted by the user.
    
    Parameters
    ----------
    entity : ``Emoji | Sticker | SoundboardSound``
        The entity to check.
    
    user : ``ClientUserBase``
        The user in context.
    
    Returns
    -------
    can : `bool`
    """
    guild = entity.guild
    if guild is None:
        return False
    
    if not can_edit_or_delete_entity_in_guild(guild, user):
        return False
    
    return True


def get_add_guilds(user, entity_type, entity):
    """
    Gets all the guilds where an entity of the given type can be added to.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user invoking the addition.
    
    entity_type : ``type<Emoji | Sticker | SoundboardSound>``
        The entity's type.
    
    entity : ``None | Emoji | Sticker | SoundboardSound``
        The entity itself for more advanced check.
    
    Returns
    -------
    guilds : ``list<Guild>``
    """
    guilds = []
    
    for guild in user.iter_guilds():
        if can_add_entity_into_guild(entity_type, entity, guild, user):
            guilds.append(guild)
    
    return guilds
