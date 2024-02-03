import vampytest
from hata import (
    Channel, ChannelType, Client, DiscordApiClient, Emoji, Guild, GuildProfile, Message, ReactionMapping, Role, User
)

from ..helpers import PERMISSION_MASK_MESSAGING_DEFAULT, get_voters


class TestDiscordApiClient(DiscordApiClient):
    __slots__ = ()
    
    async def request(self, handler, method, url, data = None, params = None, headers = None, reason = None):
        raise RuntimeError('Should not make any requests')


async def test__get_voters():
    """
    Tests whether ``get_voters`` works as intended.
    """
    client = Client(
        'token_202401160015',
        client_id = 202401160016,
        api = TestDiscordApiClient(True, 'token_202401160015'),
        
    )
    try:
        guild = Guild.precreate(202401160017)
        channel = Channel.precreate(202401160018, guild_id = guild.id, channel_type = ChannelType.guild_text)
        user_0 = User.precreate(202401160019, bot = False)
        user_0.guild_profiles[guild.id] = GuildProfile()
        user_1 = User.precreate(202401160022)
        guild.users[user_0.id] = user_0
        role = Role.precreate(
            guild.id,
            guild_id = guild.id,
            permissions = PERMISSION_MASK_MESSAGING_DEFAULT.update_by_keys(view_channel = True),
        )
        guild.roles[role.id] = role
        guild.channels[channel.id] = channel
        
        emoji = Emoji.precreate(202401160020)
        
        message = Message.precreate(
            202401160021,
            reactions = ReactionMapping({emoji: [user_0, user_1]}),
            channel_id = channel.id,
        )
        
        def is_user_id_in_blacklist_mock(user_id):
            nonlocal user_0
            nonlocal user_1
            vampytest.assert_in(user_id, (user_0.id, user_1.id))
            return False
        
        mocked = vampytest.mock_globals(
            get_voters,
            2,
            is_user_id_in_blacklist = is_user_id_in_blacklist_mock,
        )
        
        
        output = await mocked(client, message, emoji.id)
        vampytest.assert_instance(output, set)
        vampytest.assert_eq(output, {user_0})
    
    finally:
        client._delete()
        client = None
