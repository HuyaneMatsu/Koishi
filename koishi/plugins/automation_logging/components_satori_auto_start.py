__all__ = ()

import re

from hata import Emoji, create_button, create_row


EMOJI_DELETE_CHANNEL = Emoji.precreate(956250320382603274)
EMOJI_USER_KICK = Emoji.precreate(1109877398117302423)
EMOJI_USER_BAN = Emoji.precreate(852857889592836096)

SATORI_CUSTOM_ID_CHANNEL_DELETE = f'log.satori.channel.delete'
SATORI_CUSTOM_ID_USER_KICK_RP = re.compile('log\\.satori\\.user\\.([0-9a-f]{6,16})\\.kick')
SATORI_CUSTOM_ID_USER_BAN_RP = re.compile('log\\.satori\\.user\\.([0-9a-f]{6,16})\\.ban')

create_satori_custom_id_user_kick = lambda user: f'log.satori.user.{user.id:x}.kick'
create_satori_custom_id_user_ban = lambda user: f'log.satori.user.{user.id:x}.ban'


COMPONENT_DELETE_CHANNEL = create_button('Delete channel', EMOJI_DELETE_CHANNEL, custom_id = SATORI_CUSTOM_ID_CHANNEL_DELETE)


def build_satori_auto_start_component_row(user):
    """
    Creates satori auto start components.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The watched user.
    
    Returns
    -------
    component_row : ``Component``
    """
    return create_row(
        COMPONENT_DELETE_CHANNEL,
        create_button('Kick user', EMOJI_USER_KICK, custom_id = create_satori_custom_id_user_kick(user)),
        create_button('Ban user', EMOJI_USER_BAN, custom_id = create_satori_custom_id_user_ban(user)),
    )

