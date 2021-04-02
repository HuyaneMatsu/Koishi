# -*- coding: utf-8 -*-
import os
from math import floor
from functools import partial as partial_func

from hata import BUILTIN_EMOJIS, Client, Lock, KOKORO, alchemy_incendiary, Embed
from hata.discord.utils import to_json, from_json
from hata.ext.commands import wait_for_reaction
from hata.ext.slash import abort

from sqlalchemy.sql import select, update

from bot_utils.shared import GUILD__NEKO_DUNGEON, PATH__KOISHI, EMOJI__HEART_CURRENCY
from bot_utils.models import DB_ENGINE, currency_model, CURRENCY_TABLE, item_model, ITEM_TABLE

SLASH_CLIENT: Client

ITEMS = {}

MARKET_COST_FEE = 0.15
MARKET_COST_RESET = 0.05
MARKET_COST_MIN = 40

COST_FILE_LOCK = Lock(KOKORO)
COST_FILE_PATH = os.path.join(PATH__KOISHI, 'library', 'witch_craft_costs.json')

class CookingFactor:
    __slots__ = ('flavor', 'fruit', 'meat', 'monster', 'mushroom', 'vegetable')
    def __new__(cls, *, flavor=0, fruit=0, meat=0, monster=0, mushroom=0, vegetable=0):
        self = object.__new__(cls)
        
        self.flavor = flavor
        self.fruit = fruit
        self.meat = meat
        self.monster = monster
        self.vegetable = vegetable
        self.mushroom = mushroom
        
        return self
    
    def __repr__(self):
        result = ['<', self.__class__.__name__]
        
        flavor = self.flavor
        if flavor:
            result.append(' flavor=')
            result.append(repr(flavor))
            
            should_add_comma = True
        else:
            should_add_comma = False
        
        fruit = self.fruit
        if fruit:
            if should_add_comma:
                result.append(',')
            else:
                should_add_comma = True
            
            result.append(' fruit=')
            result.append(repr(fruit))
        
        meat = self.meat
        if meat:
            if should_add_comma:
                result.append(',')
            else:
                should_add_comma = True
            
            result.append(' meat=')
            result.append(repr(meat))
        
        monster = self.monster
        if monster:
            if should_add_comma:
                result.append(',')
            else:
                should_add_comma = True
            
            result.append(' monster=')
            result.append(repr(monster))
        
        mushroom = self.mushroom
        if mushroom:
            if should_add_comma:
                result.append(',')
            else:
                should_add_comma = True
            
            result.append(' mushroom=')
            result.append(repr(mushroom))
        
        vegetable = self.vegetable
        if vegetable:
            if should_add_comma:
                result.append(',')
            
            result.append(' vegetable=')
            result.append(repr(vegetable))
        
        result.append('>')
        
        return ''.join(result)
    
    def get_raw_cost(self):
        cost = 0.0
        
        flavor = self.flavor
        cost += (flavor*flavor)*0.4
        
        fruit = self.fruit
        cost += fruit*fruit
        
        meat = self.meat
        cost += meat*meat
        
        vegetable = self.vegetable
        cost += vegetable*vegetable
        
        mushroom = self.mushroom
        cost += (mushroom*mushroom)*2.0
        
        monster = self.monster
        cost += monster*monster
        
        return cost


class EdibilityFactor:
    __slots__ = ('health', 'hunger', 'sanity')
    def __new__(cls, *, health=0, hunger=0, sanity=0):
        self = object.__new__(cls)
        self.health = health
        self.hunger = hunger
        self.sanity = sanity
        return self
    
    def __repr__(self):
        result = ['<', self.__class__.__name__]
        
        health = self.health
        if health:
            result.append(' health=')
            result.append(repr(health))
            
            should_add_comma = True
        else:
            should_add_comma = False
        
        hunger = self.hunger
        if hunger:
            if should_add_comma:
                result.append(',')
            else:
                should_add_comma = True
            
            result.append(' hunger=')
            result.append(repr(hunger))
        
        sanity = self.sanity
        if sanity:
            if should_add_comma:
                result.append(',')
            
            result.append(' sanity=')
            result.append(repr(sanity))
        
        result.append('>')
        
        return ''.join(result)
    
    def get_raw_cost(self):
        cost = 0.0
        health = self.health
        cost += health*health
        
        hunger = self.hunger
        cost += hunger*hunger
        
        sanity = self.sanity
        cost += sanity*sanity
        
        return cost


class Item:
    __slots__ = ('cost', 'cooking', 'edibility', 'emoji', 'id', 'market_cost', 'name',)
    def __new__(cls, id_, name, emoji, *, cooking=None, edibility=None):
        cost = 0
        if (cooking is not None):
            cost += cooking.get_raw_cost()
        
        if (edibility is not None):
            cost += cooking.get_raw_cost()
        
        cost = int(cost**0.5)
        
        self = object.__new__(cls)
        self.id = id_
        self.name = name
        self.emoji = emoji
        self.cost = cost
        
        self.cooking = cooking
        self.edibility = edibility
        
        self.market_cost = cost
        
        ITEMS[id_] = self
        return self
    
    def __repr__(self):
        result = ['<', self.__class__.__name__]
        
        result.append(' id=')
        result.append(repr(self.id))
        
        result.append(', name=')
        result.append(repr(self.name))
        
        result.append(', emoji=')
        result.append(repr(self.emoji.name))
        
        result.append(', cost=')
        result.append(repr(self.cost))
        
        cooking = self.cooking
        if (cooking is not None):
            result.append(', cooking=')
            result.append(repr(cooking))
        
        edibility = self.edibility
        if (edibility is not None):
            result.append(', edibility=')
            result.append(repr(edibility))
        
        result.append('>')
        
        return ''.join(result)



ITEM_DUCK = Item(1, 'Duck', BUILTIN_EMOJIS['duck'],
    cooking=CookingFactor(flavor=100, meat=100, monster=20),
    edibility=EdibilityFactor(hunger=40, sanity=-20),
        )

ITEM_SALT = Item(2, 'Flavor crystal', BUILTIN_EMOJIS['salt'],
    cooking=CookingFactor(flavor=100),
    edibility=EdibilityFactor(health=-20, hunger=0, sanity=-20),
        )

ITEM_ONION = Item(3, 'Organic tear gas', BUILTIN_EMOJIS['onion'],
    cooking=CookingFactor(flavor=50, vegetable=40),
    edibility=EdibilityFactor(health=5, hunger=5, sanity=-10),
        )

ITEM_EGG = Item(4, 'Next generation (capsule)', BUILTIN_EMOJIS['egg'],
    cooking=CookingFactor(flavor=50, meat=50),
    edibility=EdibilityFactor(health=5, hunger=10),
        )

ITEM_RED_MUSHROOM = Item(5, 'Witch hallucinogen', BUILTIN_EMOJIS['mushroom'],
    cooking=CookingFactor(flavor=50, mushroom=100),
    edibility=EdibilityFactor(health=-20, hunger=10, sanity=-5),
        )

ITEM_GARLIC = Item(6, 'Anti-vampire grenade', BUILTIN_EMOJIS['garlic'],
    cooking=CookingFactor(flavor=100, vegetable=30),
    edibility=EdibilityFactor(health=10, hunger=5, sanity=-10),
        )

ITEM_OIL = Item(7, 'Pan slipper', BUILTIN_EMOJIS['oil'],
    cooking=CookingFactor(flavor=30, vegetable=20, fruit=20),
    edibility=EdibilityFactor(hunger=5, sanity=-10),
        )

ITEM_OLIVE = Item(8, 'Slipper fruit', BUILTIN_EMOJIS['olive'],
    cooking=CookingFactor(flavor=30, fruit=30),
    edibility=EdibilityFactor(health=10, hunger=10),
        )

BUYABLE = [
    ITEM_SALT,
    ITEM_ONION,
    ITEM_RED_MUSHROOM,
    ITEM_GARLIC,
    ITEM_OLIVE,
        ]

BUYABLE.sort(key=lambda item:item.name)

def load_file():
    if not os.exists(COST_FILE_PATH):
        return None
    
    with open(COST_FILE_PATH, 'r') as file:
        data = file.read()
    
    return data

def save_file(data):
    with open(COST_FILE_PATH, 'w') as file:
        data = file.write(data)


async def save_data():
    async with COST_FILE_LOCK:
        data = KOKORO.run_in_executor(load_file)
        
        if (data is None) or (not data):
            return
        
        for item_id, market_cost in data:
            try:
                item = ITEMS[item_id]
            except KeyError:
                continue
            
            item.market_cost = market_cost

async def load_data():
    async with COST_FILE_LOCK:
        data = []
        for item in ITEMS.values():
            market_cost = item.market_cost
            if market_cost != item.cost:
                data.append((item.id, market_cost))
        
        if data:
            data = to_json(data)
        else:
            data = ''
        
        KOKORO.run_in_executor(alchemy_incendiary(save_file, (data,)))

# ((x+n+1)*(x+n))/2 - ((x+1)*x)/2)
# Optimize!
# n*(2*x+n+1)/2
# Upgrade!
# n*(x<<1+n+1)>>1

def calculate_buy_cost(market_cost, n):
    return floor((n*((market_cost<<1)+n+1)>>1)*(1.0+MARKET_COST_FEE))

def calculate_sell_price(market_cost, n):
    market_cost_min = market_cost-n
    if market_cost_min < MARKET_COST_MIN:
        pass
        # TODO

def calculate_buyable_and_cost(market_cost, n, usable):
    if usable < market_cost:
        return 0, 0
    
    cost = calculate_buy_cost(market_cost, n)
    if cost <= usable:
        return n, cost
    
    bot = 0
    top = n
    
    while bot < top:
        half = (bot+top)>>1
        cost = calculate_buy_cost(market_cost, half)
        if cost > usable:
            top = half
        else:
            bot = half+1
    
    bot -= 1
    
    return bot, calculate_buy_cost(market_cost, bot)


SHOP = SLASH_CLIENT.interactions(None, 'shop', 'Witch shop ~ Nya!', guild=GUILD__NEKO_DUNGEON)

@SHOP.interactions
async def prices(client, event):
    """Lists the prices of the shop."""
    embed = Embed('Witch shop')
    for item in BUYABLE:
        embed_field_name = f'{item.emoji:e} {item.name}'
        market_cost = item.market_cost
        embed_field_value = f'Sell for: {floor(market_cost*(1.0-MARKET_COST_FEE))} {EMOJI__HEART_CURRENCY:e}\n' \
                            f'Buy for: {floor(market_cost*(1.0+MARKET_COST_FEE))} {EMOJI__HEART_CURRENCY:e}'
        
        embed.add_field(embed_field_name, embed_field_value, inline=True)
    
    return embed

CONFIRM_NAH = BUILTIN_EMOJIS['person_gesturing_no']

def check_confirm_emoji(event, confirm_emoji):
    emoji = event.emoji
    if (emoji is CONFIRM_NAH) or (emoji is confirm_emoji):
        return True
    
    return False


@SHOP.interactions
async def buy(client, event,
        item : ([(item.name, item.id) for item in BUYABLE], 'Select the item to buy nya!'),
        amount : (int, 'How much items would you want to buy?'),
            ):
    """Buy?"""
    try:
        item = ITEMS[item]
    except KeyError:
        abort('Item not available.')
    
    permissions = event.channel.cached_permissions_for(client)
    if (not permissions.can_send_messages) or (not permissions.can_add_reactions):
        abort('I need `send messages` and `add reactions` permissions to execute the command.')
    
    yield
    
    user = event.user
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select([currency_model.total_love]). \
                where(currency_model.user_id==user.id))
        
        results = await response.fetchall()
        if results:
            total_love = results[0]
        else:
            total_love = 0
    
    embed = Embed('Confirm buying',
        f'Selected item: {item.emoji:e} **{item.name}**\n'
        f'Amount: **{amount}**\n'
        f'\n'
        f'Price: {calculate_buy_cost(item.market_cost, amount)} {EMOJI__HEART_CURRENCY:e}\n'
        f'Budget: {total_love} {EMOJI__HEART_CURRENCY:e}'
            )
    
    embed.add_author(user.avaar_url, user.full_name)
    embed.add_footer('The prices of context of demand and supply.')
    
    message = await client.message_create(event.channel, embed=embed)
    await client.reaction_add(message, item.emoji)
    await client.reaction_add(message, CONFIRM_NAH)
    
    try:
        event = await wait_for_reaction(client, message, partial_func(check_confirm_emoji, item.emoji), 300.0)
    except TimeoutError:
        return
    
    if event.emoji is CONFIRM_NAH:
        embed.title = 'Buying cancelled'
    else:
        user = event.user
        async with DB_ENGINE.connect() as connector:
            response = await connector.execute(
                select([currency_model.total_love, currency_model.total_allocated]). \
                    where(currency_model.user_id==user.id))
            
            results = await response.fetchall()
            if results:
                total_love, total_allocated = results[0]
            else:
                total_love = total_allocated = 0
            
            if total_love == 0:
                amount = cost = 0
            else:
                amount, cost = calculate_buyable_and_cost(item.market_cost, amount, total_love-total_allocated)
                
                item.market_cost += amount
            
            if cost == 0:
                new_love = total_love
            else:
                new_love = total_love-cost
                await connector.execute(update(currency_model.user_id==user.id). \
                    values(total_love = new_love))
                
                response = await connector.execute(select([item_model.id, item_model.amount]). \
                    where(item_model.user_id==user.id).where(item_model.type==item.id))
                
                results = await response.fetchall()
                if results:
                    row_id, actual_amount = results[0]
                    new_amount = actual_amount+amount
                    to_execute = ITEM_TABLE.update().values(
                        amount=new_amount
                            ).where(item_model.id==row_id)
                else:
                    to_execute = ITEM_TABLE.insert().values(
                        user_id = user.id,
                        amount  = amount,
                        type    = item.id
                            )
                
                await connector.execute(to_execute)
        
        embed.title = 'Buying confirmed'
        embed.description = (
            f'Selected item: {item.emoji:e} **{item.name}**\n'
            f'Bought mount: **{amount}**\n'
            f'\n'
            f'Hearts: {total_love} {EMOJI__HEART_CURRENCY:e} -> {new_love} {EMOJI__HEART_CURRENCY:e}'
                )
    
    await client.message_edit(message, embed=embed)




