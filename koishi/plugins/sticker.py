__all__ = ()

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import Color, Embed, STICKERS, USERS
from hata.ext.slash import abort
from scarletio import to_json
from scarletio.web_common import quote
from sqlalchemy import and_, func as alchemy_function
from sqlalchemy.sql import desc, select

from ..bot_utils.constants import GUILD__SUPPORT
from ..bot_utils.models import DB_ENGINE, sticker_counter_model
from ..bots import MAIN_CLIENT


RELATIVE_MONTH = RelativeDelta(months = 1)
MONTH = TimeDelta(days = 367, hours = 6) / 12
MOST_USED_PER_PAGE = 30


STICKER_COMMANDS = MAIN_CLIENT.interactions(
    None,
    name = 'sticker',
    description = 'Sticker counter commands.',
    guild = GUILD__SUPPORT,
)

ORDER_DECREASING = 1
ORDER_INCREASING = 0
ORDERS = [
    ('decreasing', ORDER_DECREASING),
    ('increasing', ORDER_INCREASING),
    
]

def item_sort_key(item):
    return item[1]


@STICKER_COMMANDS.interactions
async def user_top(
    event,
    user: ('user', 'By who?') = None,
    count: (range(10, 61, 10), 'The maximal amount of emojis to show') = 30,
    months: (range(1, 13), 'The months to get') = 1,
):
    """List the most used stickers at KW by you or by the selected user."""
    if user is None:
        user = event.user
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    sticker_counter_model.sticker_id,
                    alchemy_function.count(sticker_counter_model.sticker_id).label('total'),
                ],
            ).where(
                and_(
                    sticker_counter_model.user_id == user.id,
                    sticker_counter_model.timestamp > DateTime.now(TimeZone.utc) - RELATIVE_MONTH * months,
                ),
            ).limit(
                count,
            ).group_by(
                sticker_counter_model.sticker_id,
            ).order_by(
                desc('total'),
            )
        )
        
        results = await response.fetchall()
    
    
    embed = Embed(
        f'Most used stickers by {user.full_name}',
        color = user.color_at(GUILD__SUPPORT),
    ).add_thumbnail(
        user.avatar_url,
    )
    
    
    if results:
        description_parts = []
        limit = len(results)
        index = 0
        start = 1
        
        while True:
            sticker_id, count = results[index]
            
            index += 1
            
            try:
                sticker = STICKERS[sticker_id]
            except KeyError:
                continue
            
            description_parts.append(str(index))
            description_parts.append('.: **')
            description_parts.append(str(count))
            description_parts.append('** x ')
            description_parts.append(sticker.name)
            
            if (not index % 10) or (index == limit):
                description = ''.join(description_parts)
                description_parts.clear()
                embed.add_field(f'{start} - {index}', description, inline = True)
                
                if (index == limit):
                    break
                
                start = index + 1
                continue
            
            description_parts.append('\n')
            continue
    else:
        embed.description = '*No recorded data.*'
    
    return embed



@STICKER_COMMANDS.interactions
async def sticker_top(
    raw_sticker: ('str', 'Pick an sticker', 'sticker'),
    months: (range(1, 13), 'The months to get') = 1,
):
    """List the users using the given sticker the most."""
    sticker = GUILD__SUPPORT.get_sticker_like(raw_sticker)
    if sticker is None:
        abort(f'There is not sticker with name `{raw_sticker}` in the guild.')
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    sticker_counter_model.user_id,
                    alchemy_function.count(sticker_counter_model.user_id).label('total'),
                ],
            ).where(
                and_(
                    sticker_counter_model.sticker_id == sticker.id,
                    sticker_counter_model.timestamp > DateTime.now(TimeZone.utc) - RELATIVE_MONTH * months,
                )
            ).limit(
                30,
            ).group_by(
                sticker_counter_model.user_id,
            ).order_by(
                desc('total')
            )
        )
        
        results = await response.fetchall()
    
    
    if results:
        index = 0
        limit = len(results)
        description_parts = []
        
        while True:
            user_id, count = results[index]
            
            index += 1
            
            try:
                user = USERS[user_id]
            except KeyError:
                continue
            
            guild_profile = user.get_guild_profile_for(GUILD__SUPPORT)
            if guild_profile is None:
                nick = None
            else:
                nick = guild_profile.nick
            
            description_parts.append(str(index))
            description_parts.append('.: **')
            description_parts.append(str(count))
            description_parts.append('** x ')
            description_parts.append(user.full_name)
            if (nick is not None):
                description_parts.append(' *[')
                description_parts.append(nick)
                description_parts.append(']*')
            
            if index == limit:
                break
            
            description_parts.append('\n')
            continue
        
        description = ''.join(description_parts)
    else:
        description = '*No usages recorded*'
    
    
    return Embed(
        f'Top sticker users of {sticker.name}',
        description,
    ).add_thumbnail(sticker.url)


def assert_user_permissions(event):
    if not event.user_permissions.manage_guild_expressions:
        abort(f'You must have manage emojis & stickers permissions to invoke this command.')


@STICKER_COMMANDS.interactions
async def most_used(
    months: (range(1, 13), 'The months to get') = 1,
    page: ('int', 'Select a page') = 1,
    order: (ORDERS, 'Ordering?') = ORDER_DECREASING,
):
    """Shows the most used stickers."""
    if page < 1:
        abort('Page value can be only positive')
    
    low_date_limit = DateTime.now(TimeZone.utc) - RELATIVE_MONTH * months
    is_new_limit = DateTime.now(TimeZone.utc) - MONTH
    
    async with DB_ENGINE.connect() as connector:
        
        response = await connector.execute(
            select(
                [
                    sticker_counter_model.sticker_id,
                    alchemy_function.count(sticker_counter_model.user_id).label('total'),
                ],
            ).where(
                sticker_counter_model.timestamp > low_date_limit,
            ).group_by(
                sticker_counter_model.sticker_id,
            )
        )
        
        results = await response.fetchall()
    
    items = []
    
    guild_stickers = set(GUILD__SUPPORT.stickers.values())
    
    for sticker_id, count in results:
        try:
            sticker = STICKERS[sticker_id]
        except KeyError:
            continue
        
        guild_stickers.discard(sticker)
        
        is_new = (sticker.created_at >= is_new_limit)
        items.append((sticker, count, is_new))
    
    for sticker in guild_stickers:
        is_new = (sticker.created_at >= is_new_limit)
        items.append((sticker, 0, is_new))
    
    items.sort(key = item_sort_key, reverse = order)
    
    page_shift = (page - 1) * MOST_USED_PER_PAGE
    
    index = page_shift
    limit = min(len(items), index + MOST_USED_PER_PAGE)
    
    description_parts = []
    
    if index < limit:
        while True:
            sticker, count, is_new = items[index]
            index += 1
            
            description_parts.append(str(index))
            description_parts.append('.: **')
            description_parts.append(str(count))
            description_parts.append('** x ')
            description_parts.append(sticker.name)
            
            if is_new:
                description_parts.append(' *[New!]*')
            
            if index == limit:
                break
            
            description_parts.append('\n')
            continue
        
        description = ''.join(description_parts)
    else:
        description = '*No recorded data*'
    
    return Embed(
        'Most used stickers:',
        description,
    ).add_footer(
        f'Page {page} / {(len(items) // MOST_USED_PER_PAGE) + 1}',
    )


def get_month_keys():
    now = DateTime.now(TimeZone.utc)
    year = now.year
    month = now.month
    
    month_keys = [(year, month)]
    for _ in range(11):
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        
        month_keys.append((year, month))
    
    month_keys.reverse()
    return month_keys


MONTHS = {
    1: 'jan',
    2: 'feb',
    3: 'mar',
    4: 'apr',
    5: 'may',
    6: 'jun',
    7: 'jul',
    8: 'aug',
    9: 'sep',
    10: 'oct',
    11: 'nov',
    12: 'dec',
}

def create_sticker_graph_line_data_set(sticker, results_by_month, month_keys):
    color = Color((sticker.id >> 22) & 0xffffff).as_html
    return {
        'label': sticker.name,
        'data': [results_by_month.get(month, 0) for month in month_keys],
        'borderColor': color,
        'backgroundColor': color,
        'fill': False,
    }


@STICKER_COMMANDS.interactions
async def user_sticker_compare(
    raw_sticker_1: ('str', 'Pick a sticker', 'sticker-1'),
    raw_sticker_2: ('str', 'Pick a sticker', 'sticker-2') = None,
    raw_sticker_3: ('str', 'Pick a sticker', 'sticker-3') = None,
    raw_sticker_4: ('str', 'Pick a sticker', 'sticker-4') = None,
    raw_sticker_5: ('str', 'Pick a sticker', 'sticker-5') = None,
    raw_sticker_6: ('str', 'Pick a sticker', 'sticker-6') = None,
    raw_sticker_7: ('str', 'Pick a sticker', 'sticker-7') = None,
    raw_sticker_8: ('str', 'Pick a sticker', 'sticker-8') = None,
    raw_sticker_9: ('str', 'Pick a sticker', 'sticker-9') = None,
    raw_sticker_10: ('str', 'Pick a sticker', 'sticker-10') = None,
):
    """Compares the two stickers or something, smh smh."""
    stickers = set()
    
    for raw_sticker in (
        raw_sticker_1, raw_sticker_2, raw_sticker_3, raw_sticker_4, raw_sticker_5, raw_sticker_6, raw_sticker_7,
        raw_sticker_8, raw_sticker_9, raw_sticker_10,
    ):
        if raw_sticker is None:
            continue
        
        sticker = GUILD__SUPPORT.get_sticker_like(raw_sticker)
        if sticker is None:
            
            # Slash command parameters have no length limit
            if len(raw_sticker) > 100:
                raw_sticker = raw_sticker[:100]
            
            abort(f'There is not sticker with name `{raw_sticker}` in the guild.')
            return # this makes the linters stop crying
        
        stickers.add(sticker)
    
    stickers = sorted(stickers)
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    sticker_counter_model.sticker_id,
                    alchemy_function.count(sticker_counter_model.sticker_id),
                    alchemy_function.date_part('year', sticker_counter_model.timestamp).label('year'),
                    alchemy_function.date_part('month', sticker_counter_model.timestamp).label('month'),
                ],
            ).where(
                and_(
                    sticker_counter_model.sticker_id.in_([sticker.id for sticker in stickers]),
                    sticker_counter_model.timestamp > DateTime.now(TimeZone.utc) - RELATIVE_MONTH * 12,
                )
            ).group_by(
                sticker_counter_model.sticker_id,
                'month',
                'year',
            )
        )
        
        results = await response.fetchall()
    
    sticker_id_to_results_by_month = {sticker.id: {} for sticker in stickers}
    
    for sticker_id, count, year, month in results:
        sticker_id_to_results_by_month[sticker_id][(int(year), int(month))] = count
    
    month_keys = get_month_keys()
    
    data = to_json({
        'type': 'line',
        'data': {
            'labels': [f'{year} {MONTHS[month]}' for year, month in month_keys],
            'datasets': [
                create_sticker_graph_line_data_set(sticker, sticker_id_to_results_by_month[sticker.id], month_keys)
                for sticker in stickers
            ],
        },
        'options': {
            'legend': {
                'labels': {
                    'fontColor': 'white',
                },
            },
            'scales': {
                'yAxes': [
                    {
                        'ticks': {
                            'beginAtZero': 'true',
                            'fontColor': 'white',
                            'fontStyle': 'bold',
                        },
                        'gridLines': {
                            'color': 'white',
                        },
                    },
                ],
                'xAxes': [
                    {
                        'ticks': {
                            'fontColor': 'white',
                            'fontStyle': 'bold',
                        },
                        'gridLines': {
                            'color': 'white',
                        },
                    },
                ],
            },
        },
    })
    
    chart_url = f'https://quickchart.io/chart?width=500&height=300&c={quote(data)}'
    
    return Embed(
        'Sticker comparison'
    ).add_image(
        chart_url,
    )

@STICKER_COMMANDS.autocomplete('sticker_name', 'sticker')
async def autocomplete_sticker_name(value):
    if value is None:
        return sorted(
            sticker.name for sticker in GUILD__SUPPORT.stickers.values()
        )
    
    value = value.casefold()
    
    return sorted(
        sticker.name for sticker in GUILD__SUPPORT.stickers.values()
        if value in sticker.name.casefold()
    )


@user_sticker_compare.autocomplete(
    'sticker-1', 'sticker-2', 'sticker-3', 'sticker-4', 'sticker-5', 'sticker-6', 'sticker-7', 'sticker-8',
    'sticker-9', 'sticker-10'
)
async def get_autocomplete_sticker_names_except(event, actual_value):
    stickers_except = set()
    
    for value in event.get_non_focused_values().values():
        if value is not None:
            sticker = GUILD__SUPPORT.get_sticker_like(value)
            if (sticker is not None):
                stickers_except.add(sticker)
    
    guild_stickers = GUILD__SUPPORT.stickers
    
    if actual_value is None:
        return sorted(
            sticker.name for sticker in guild_stickers.values()
            if (sticker not in stickers_except)
        )
    
    
    actual_value = actual_value.casefold()
    
    return sorted(
        sticker.name for sticker in guild_stickers.values()
        if (
            (sticker not in stickers_except) and
            (actual_value in sticker.name.casefold())
        )
    )
