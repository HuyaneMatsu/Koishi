__all__ = ()

from hata import GuildProfileFlag

ONBOARDING_MASK_STARTED = GuildProfileFlag().update_by_keys(onboarding_started = True)
ONBOARDING_MASK_COMPLETED = GuildProfileFlag().update_by_keys(onboarding_completed = True)
ONBOARDING_MASK_ALL = ONBOARDING_MASK_STARTED | ONBOARDING_MASK_COMPLETED

WELCOME_MESSAGES = (
    lambda user: f'Roses are red, also blue, {user.mention} joined this server with Mr. Hat too',
    lambda user: f'Koooosh. {user.mention} just landed.',
    lambda user: f'{user.mention} just joined. Everyone, watch your back!',
    lambda user: f'Welcome, {user.mention}. We hope you brought shrimp fry.',
    lambda user: f'Where’s {user.mention}? RIGHT BEHIND YOU!',
    lambda user: f'Heart throbbing {user.mention} showed up!',
    lambda user: f'It\'s a youkai! It\'s a fairy! Nevermind, it\'s just {user.mention}.',
    lambda user: f'We\'ve been already behind you {user.mention}',
    lambda user: f'It\'s {user.mention}! Praise Mr. Unconsciousness! [T]/',
    lambda user: f'Always gonna love {user.mention}. Always gonna remember {user.mention}.',
    lambda user: f'{user.mention} is here to stab and eat shrimp fry. And {user.mention} is all out of shrimp fry.',
    lambda user: f'{user.mention} is behind me... or are they?',
    lambda user: f'{user.mention} just showed up. Hold my fishing rod.',
    lambda user: f'A lovely {user.mention} chan appeared.',
    lambda user: f'{user.mention} just joined. Can I get a croissant?',
    lambda user: f'Mr. Hat owner {user.mention}',
    lambda user: f'{user.mention} is here, as the Mr. Hat foretold.',
    lambda user: f'{user.mention} just arrived. Seems adorable - please love.',
    lambda user: f'Moshi Moshi?. Is it {user.mention} you\'re calling?',
    lambda user: f'The creature {user.mention} showed up!',
    lambda user: f'Ready to stop thinking, {user.mention}?',
    lambda user: f'{user.mention} has joined the server! It\'s a fumo!',
    lambda user: f'{user.mention} just joined the server - *staaaare*',
    lambda user: f'{user.mention} just joined. Everyone, stop thinking!',
    lambda user: f'Welcome, {user.mention}. Bring shrimp fry and croissant.',
    lambda user: f'Satoooori, {user.mention} is here!',
    lambda user: f'{user.mention} has arrived. The dinner just started.',
    lambda user: f'Welcome, {user.mention}. Stay awhile and fish with us.',
    lambda user: f'Welcome {user.mention}. Leave your Mr. Knife by the door.',
    lambda user: f'{user.mention} joined. Mr. Hat helps them relax.',
    lambda user: f'{user.mention} just arrived. Seems conscious - please nerf.',
    lambda user: f'{user.mention} has joined the Extra stage.',
    lambda user: f'Hey! Listen! {user.mention} has called!',
    lambda user: f'{user.mention} hopped into the server. My face is butter!!',
    lambda user: f'{user.mention} just flew into the server.',
    lambda user: f'Yay! {user.mention} just landed.',
    lambda user: f'{user.mention} joined. You must collect additional **P**ower items.',
)
