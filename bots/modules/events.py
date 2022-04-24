from datetime import datetime
from dateutil.relativedelta import relativedelta
from hata import elapsed_time, Embed, Client
from bot_utils.constants import ROLE__SUPPORT__VERIFIED, EMOJI__HEART_CURRENCY, COLOR__EVENT, \
    CHANNEL__SUPPORT__EVENT, ROLE__SUPPORT__EVENT_MANAGER, LINK__HATA_GIT, GUILD__SUPPORT

EVENT_TEST_CHECK = None # checks.has_any_role((ROLE__SUPPORT__MODERATOR, ROLE__SUPPORT__EVENT_MANAGER))

SLASH_CLIENT: Client
EVENTS = SLASH_CLIENT.interactions(
    None,
    name = 'events',
    description = f'{GUILD__SUPPORT.name} event information.',
    guild = GUILD__SUPPORT,
)

HATA_JAM_2_DESCRIPTION = Embed(
    'Hata jam 2',
    'Slashy jammy slash commands',
    color = COLOR__EVENT
).add_field(
    'Event theme: Cats & Nekogirls',
    'Make cat or nekogirl related slash commands.'
).add_field(
    'Event technology',
    '**Language**: Python3\n'
    f'**Library**: [Hata]({LINK__HATA_GIT})\n'
    '**Implementations**: Pypy, Cpython\n'
    '**Python version**: >=3.6'
).add_field(
    'Prize pool',
    f'1st place: 6 month of Discord Nitro + 24k {EMOJI__HEART_CURRENCY} + NEKOPARA Vol. 4 on Steam\n'
    f'2nd place: 4 month of Discord Nitro + 16k {EMOJI__HEART_CURRENCY} \n'
    f'3rd place: 2 month of Discord Nitro + 8k {EMOJI__HEART_CURRENCY}'
).add_field(
    'Event organizers',
    'HuyaneMatsu#2016\n'
    '\n'
    f'If you have any questions ping us specifically or by pinging the role {ROLE__SUPPORT__EVENT_MANAGER:m}, '
    'although try not to spam.'
).add_field(
    'Timeline',
    'Times are in UTC-0 24h hour format, start date means 00:01am while end date means by 23:59pm that day.\n'
    '\n'
    'Qualifier: January 14 - 26\n'
    'Codejam duration: January 29 - February 11\n'
    'Deciding winners: February 12 - 14'
).add_field(
    'Qualifier',
    'You need to complete the qualifier test shown by Koishi\'s `k!qualifier` command and submit it in '
    f'DM with the `k!submit` one. (You must have {ROLE__SUPPORT__VERIFIED:m} role to submit your solution.)'
).add_field(
    'Teams',
    'No teams now.'
).add_field(
    'Advertising',
    f'If you want to advertise you can should not. Really, ask {ROLE__SUPPORT__EVENT_MANAGER:m} and the '
    f'owner(s) of the other guild as well, whether they allow it.'
).add_field(
    'Codejam rating rules',
    'To get you approximate idea on what we rate on how will your submissions be scored we\'ve made the following '
    'table:\n'
    '\n'
    
    'Clean code: (25%)\n'
    'Idea: (40%)\n'
    'Functionality: (35%)'
).add_field(
    'Codejam submissions',
    f'Please open a git repo for your submission and send the link to an {ROLE__SUPPORT__EVENT_MANAGER:m}.\n'
    '\n'
    'Your project has to include documentation. At the very least, it should include instructions on how to set-up '
    'and run your projects, but keep in mind that a README is the first thing people typically see when they look '
    'at a project on GitHub. A good README includes a short description of the project, installation instructions, '
    'and often documents common usage of the application.\n'
    '\n'
    'Also use English or Engrish at least.'
)


HATA_JAM_2_QUALIFIER = (
    Embed(
        'Hata jam 2 qualifier',
        'Hata code jam 2 qualifier\n'
        'You have `n` amount of love between nekogirls. What are the most expensive nekogirls you can get?\n'
        '\n'
        'Each nekogirl has a type:\n'
        '\n'
        '```\n'
        'Horny Maine Coon nekogirl    [12400 nekolove]\n'
        'Horny Scottish Fold nekogirl [ 8800 nekolove]\n'
        'Horny American Curl nekogirl [ 8400 nekolove]\n'
        'Horny Munchkin nekogirl      [10600 nekolove]\n'
        '```\n'
        '\n'
        'Each nekogirl also can have any amount of extra traits:\n'
        '\n'
        '```\n'
        'Two tailed youkai [38950 nekolove]\n'
        'Thick tail(s)     [ 1300 nekolove]\n'
        'OwO ear tufts     [ 4400 nekolove]\n'
        'Heterochromia     [12035 nekolove]\n'
        'Hime-cut          [  675 nekolove]\n'
        'Boing-Boing       [ 2750 nekolove]\n'
        'Red eye(s)        [13070 nekolove]\n'
        'Lunatic           [19500 nekolove]\n'
        '```\n'
        '\n'
        'Write a `get_nekogirls` function what prints out `top` amount of the most expensive nekogirls for the given '
        '`n` amount of nekolove from expensive to less expensive order.\n'
        '\n'
        '```py\n'
        'def get_nekogirls(nekolove, top):\n'
        '    ...\n'
        '```\n'
        '\n'
        'Notes:\n'
        '- Each nekogirl should be on a separate line.\n'
        '- Each line should contain the nekogirl\'s cost, type and extra traits in this order.\n'
        '- Cost and type should be separated by a ` ` character.\n'
        '- Type and each extra trait should be separated by `, ` characters.\n'
        '- Extra traits should be sorted by name.',
        color = COLOR__EVENT
    ),
    
    Embed(
        None,
        'The following code:\n'
        '```py\n'
        'get_nekogirls(20000, 10)\n'
        'print()\n'
        'get_nekogirls(60000, 5)\n'
        '```\n'
        'Would output:\n'
        '```\n'
        '19725 Horny Munchkin nekogirl, Boing-Boing, Hime-cut, OwO ear tufts, Thick tail(s)\n'
        '19550 Horny Maine Coon nekogirl, Boing-Boing, OwO ear tufts\n'
        '19050 Horny Munchkin nekogirl, Boing-Boing, OwO ear tufts, Thick tail(s)\n'
        '18775 Horny Maine Coon nekogirl, Hime-cut, OwO ear tufts, Thick tail(s)\n'
        '18425 Horny Munchkin nekogirl, Boing-Boing, Hime-cut, OwO ear tufts\n'
        '18100 Horny Maine Coon nekogirl, OwO ear tufts, Thick tail(s)\n'
        '17925 Horny Scottish Fold nekogirl, Boing-Boing, Hime-cut, OwO ear tufts, Thick tail(s)\n'
        '17750 Horny Munchkin nekogirl, Boing-Boing, OwO ear tufts\n'
        '17525 Horny American Curl nekogirl, Boing-Boing, Hime-cut, OwO ear tufts, Thick tail(s)\n'
        '17475 Horny Maine Coon nekogirl, Hime-cut, OwO ear tufts\n'
        '\n'
        '59930 Horny Munchkin nekogirl, Boing-Boing, Heterochromia, Hime-cut, Lunatic, Red eye(s), Thick tail(s)\n'
        '59800 Horny Maine Coon nekogirl, Boing-Boing, OwO ear tufts, Thick tail(s), Two tailed youkai\n'
        '59785 Horny Scottish Fold nekogirl, Heterochromia, Two tailed youkai\n'
        '59780 Horny Scottish Fold nekogirl, Heterochromia, Hime-cut, Lunatic, OwO ear tufts, Red eye(s), Thick '
        'tail(s)\n'
        '59755 Horny Maine Coon nekogirl, Boing-Boing, Heterochromia, Lunatic, Red eye(s)\n'
        '```',
        color = COLOR__EVENT
        )
        
    )

@EVENTS.interactions
async def jam(client, event):
    """Hata jam 2 description."""
    return HATA_JAM_2_DESCRIPTION

@EVENTS.interactions
async def qualifier(client, event):
    """Hata jam 2's qualifier."""
    return HATA_JAM_2_QUALIFIER

QUALIFIER_DEADLINE = datetime(2021, 1, 27, 0, 0, 0)
JAM_START = datetime(2021, 1, 29, 0, 0, 0)
JAM_DEADLINE = datetime(2021, 2, 12, 0, 0, 0)


@EVENTS.interactions
async def submit(client, event,
        submission_reference_url: ('str', 'Please give a link to your submission'),
            ):
    """Submit your qualifier solution!"""
    if (event.guild is not None):
        return Embed('Error', 'Please use this channel in a private channel.')
    
    if not event.user.has_roole(ROLE__SUPPORT__VERIFIED):
        return Embed('Permission denied', f'You must have {ROLE__SUPPORT__VERIFIED.mention} role to invoke this '
            f'command.')
    
    if datetime.utcnow() >= QUALIFIER_DEADLINE:
        return Embed('Oh No!', 'Qualifier over', color=COLOR__EVENT)
    
    user = event.user
    await client.message_create(CHANNEL__SUPPORT__EVENT, f'{user:f}, [{user.id}] submitted:\n'
        f'`{submission_reference_url}`')
    
    return Embed('Success', 'Noice', color=COLOR__EVENT)

@EVENTS.interactions
async def countdown(client, event):
    """Countdown till the end of the event\'s next important date."""
    now = datetime.utcnow()
    for date in (QUALIFIER_DEADLINE, JAM_START, JAM_DEADLINE):
        if now < date:
            return elapsed_time(relativedelta(now, date))
    
    return 'Countdown over!'

