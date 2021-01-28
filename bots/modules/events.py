# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta

from hata import elapsed_time, Color, Embed, Client, ChannelText
from hata.ext.commands import Cooldown, checks

from bot_utils.tools import CooldownHandler
from bot_utils.shared import EVERYNYAN_ROLE, STAFF_ROLE, EVENT_CHANNEL, EVENT_LOLI_ROLE, HATA_GIT, CURRENCY_EMOJI

EVENT_COLOR = Color(2316923)

EVENT_TEST_CHECK = None # checks.has_any_role((STAFF_ROLE, EVENT_LOLI_ROLE))

Koishi: Client
Koishi.command_processer.create_category('EVENTS', checks=EVENT_TEST_CHECK)

HATA_JAM_2_DESCRIPTION = Embed('Hata jam 2', 'Slashy jammy slash commands', color=EVENT_COLOR). \
    add_field(
        'Event theme: Cats & Nekogirls',
        'Make cat or nekogirl related slash commands.'
            ). \
    add_field(
        'Event technology',
        '**Language**: Python3\n'
        f'**Library**: [Hata]({HATA_GIT})\n'
        '**Implementations**: Pypy, Cpython\n'
        '**Python version**: >=3.6'
            ). \
    add_field(
        'Prize pool',
        f'1st place: 6 month of Discord Nitro + 24k {CURRENCY_EMOJI:e} + NEKOPARA Vol. 4 on Steam\n'
        f'2nd place: 4 month of Discord Nitro + 16k {CURRENCY_EMOJI:e} \n'
        f'3rd place: 2 month of Discord Nitro + 8k {CURRENCY_EMOJI:e}'
            ). \
    add_field(
        'Event organizers',
        'HuyaneMatsu#2016\n'
        '\n'
        f'If you have any questions ping us specifically or by pinging the role {EVENT_LOLI_ROLE:m}, '
        'although try not to spam.'
            ). \
    add_field(
        'Timeline',
        'Times are in UTC-0 24h hour format, start date means 00:01am while end date means by 23:59pm that day.\n'
        '\n'
        'Qualifier: January 14 - 26\n'
        'Codejam duration: January 29 - February 11\n'
        'Deciding winners: February 12 - 14'
            ). \
    add_field(
        'Qualifier',
        'You need to complete the qualifier test shown by Koishi\'s `k!qualifier` command and submit it in '
        f'DM with the `k!submit` one. (You must have {EVERYNYAN_ROLE:m} role to submit your solution.)'
            ). \
    add_field(
        'Teams',
        'No teams now.'
            ). \
    add_field(
        'Advertising',
        f'If you want to advertise you can should not. Really, ask {EVENT_LOLI_ROLE:m} and the owner(s) of teh other '
        f'guild as well, whether they allow it.'
            ). \
    add_field(
        'Codejam rating rules',
        'To get you approximate idea on what we rate on how will your submissions be scored we\'ve made the following '
        'table:\n'
        '\n'
    
        'Clean code: (25%)\n'
        'Idea: (40%)\n'
        'Functionality: (35%)'
            ). \
    add_field(
        'Codejam submissions',
        f'Please open a git repo for your submission and send the link to an {EVENT_LOLI_ROLE:m}.\n'
        '\n'
        'Your project has to include documentation. At the very least, it should include instructions on how to set-up '
        'and run your projects, but keep in mind that a README is the first thing people typically see when they look '
        'at a project on GitHub. A good README includes a short description of the project, installation instructions, '
        'and often documents common usage of the application.\n'
        '\n'
        'Also use English or Engrish at least.'
            )


HATA_JAM_2_QUALIFIER = (
    Embed('Hata jam 2 qualifier',
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
        '- Extra traits should be sorted by name.'
        , color=EVENT_COLOR),
    
    Embed(None,
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
        '```'
        , color=EVENT_COLOR)
        
    )

@Koishi.commands(category='EVENTS')
async def jam(client, message):
    return HATA_JAM_2_DESCRIPTION

@Koishi.commands(category='EVENTS')
async def qualifier(client, message):
    """
    Shows you hata jam 2's qualifier.
    """
    for embed in HATA_JAM_2_QUALIFIER:
        yield embed

QUALIFIER_DEADLINE = datetime(2021, 1, 27, 0, 0, 0)
JAM_START = datetime(2021, 1, 29, 0, 0, 0)
JAM_DEADLINE = datetime(2021, 2, 12, 0, 0, 0)


@Koishi.commands(category='EVENTS', checks=[checks.private_only(), checks.has_role(EVERYNYAN_ROLE)])
@Cooldown('user', 7200., limit=2, handler=CooldownHandler())
async def submit(client, message):
    """
    Submit your qualifier solution!
    
    Please include your file as a `.py` file attachment.
    """
    if datetime.utcnow() >= QUALIFIER_DEADLINE:
        return Embed('Oh No!', 'Qualifier over', color=EVENT_COLOR)
    
    attachments = message.attachments
    if attachments is None:
        attachment = None
    else:
        for attachment in attachments:
            if attachment.name.endswith('.py'):
                break
        else:
            attachment = None
    
    if attachment is None:
        return Embed('Error', 'No attachment or no `.py` attachment found.', color=EVENT_COLOR)
    
    if attachment.size > 1048576:
        return Embed('Error', 'Size limit exceeded.', color=EVENT_COLOR)
    
    file = await client.download_attachment(attachment)
    await client.message_create(EVENT_CHANNEL, f'{message.author:f}, [{message.author.id}] submitted:',
        file=('submission.py', file))
    
    return Embed('Success', 'Noice', color=EVENT_COLOR)


async def countdown_description(client, message):
    now = datetime.utcnow()
    for description, date in (
            ('hata code jam 2 qualifier end', QUALIFIER_DEADLINE),
            ('hata code jam 2 start', JAM_START),
            ('hata code jam 2 end', JAM_DEADLINE),
                ):
        if now < date:
            result = f'there is {elapsed_time(relativedelta(now, date))} left'
            break
    else:
        result = 'the countdown is already over'
    
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('countdown', (
        f'Returns when the {description}s!\n'
        f'Usage: `{prefix}countdown`\n'
        '\n'
        f'Don\'t worry, we got you, {result}.'
            ), color=EVENT_COLOR)

@Koishi.commands(aliases=['deadline', 'event_deadline'], description=countdown_description, category='EVENTS')
async def countdown(client, message):
    now = datetime.utcnow()
    for date in (QUALIFIER_DEADLINE, JAM_START, JAM_DEADLINE):
        if now < date:
            result = elapsed_time(relativedelta(now, date))
            break
    else:
        result = 'Countdown over!'
    
    await client.message_create(message.channel, result)

