import re

from hata import Client, Embed
from hata.ext.plugin_loader import require
from hata.ext.slash import abort, Button, InteractionResponse
from random import choice, randint, random
from math import sqrt, ceil

from ..bot_utils.constants import GUILD__SUPPORT
from ..bots import SLASH_CLIENT


require(Marisa = Client)


DETAILS_BY_CATEGORY = {}

OBJECTS_BY_CATEGORY = {}

ACTIVE_GAMES = {}

QUESTION_COUNT = 3


QUESTION_TYPE_NONE = 0
QUESTION_TYPE_IS = 1
QUESTION_TYPE_CAN = 2

QUESTION_TYPE_NAMES = {
    QUESTION_TYPE_NONE: 'null',
    QUESTION_TYPE_IS: 'is',
    QUESTION_TYPE_CAN: 'can',
}

DEFAULT_QUESTION_TYPE_NAME = 'unknown'

def get_question_type():
    if random() < 0.5:
        question_type = QUESTION_TYPE_CAN
    else:
        question_type = QUESTION_TYPE_IS
    
    return question_type

def get_question_type_name(question_type):
    return QUESTION_TYPE_NAMES.get(question_type, DEFAULT_QUESTION_TYPE_NAME)


class Detail:
    """
    Detail about an object.
    
    Parameters
    ----------
    category : `str`
        The categories within the object is.
    name : `str`
        The object's name.
    mutually_exclusive_with : `None`, `frozenset` of ``Detail``
        A frozenset of mutually exclusive details.
    value_by_question_type : `None` or `dict` of (`int`, `str`) items
        Question type value overwrites.
    sort_value : `int`
        Sort value of the detail.
    """
    __slots__ = ('name', 'category', 'mutually_exclusive_with', 'value_by_question_type', 'sort_value')
    
    def __new__(cls, category, name, *, value_by_question_type = None):
        self = object.__new__(cls)
        self.category = category
        self.name = name
        self.mutually_exclusive_with = None
        self.value_by_question_type = value_by_question_type
        self.sort_value = 0
        
        try:
            details = DETAILS_BY_CATEGORY[category]
        except KeyError:
            details = []
            DETAILS_BY_CATEGORY[category] = details
        
        details.append(self)
        
        return self
    
    
    def __repr__(self):
        return f'<{self.__class__.__name__} name = {self.name!r}>'
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.sort_value != other.sort_value:
            return False
        
        if self.category != other.category:
            return False
        
        if self.name != other.name:
            return False
        
        return True
    
    def __gt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.sort_value > other.sort_value:
            return True
        
        if self.name > other.name:
            return True
        
        return False
    
    
    def __lt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.sort_value < other.sort_value:
            return True
        
        if self.name < other.name:
            return True
        
        return False
    
    
    def __hash__(self):
        hash_value = 0
        hash_value ^= hash(self.category)
        hash_value ^= hash(self.name)
        return hash_value
    
    
    def increase_sort_value(self, by):
        self.sort_value += by
    
    
    def get_question_for(self, question_type):
        value_by_question_type = self.value_by_question_type
        
        while True:
            if (value_by_question_type is not None):
                try:
                    value = value_by_question_type[question_type]
                except KeyError:
                    pass
                else:
                    if question_type == QUESTION_TYPE_IS:
                        question_word = 'Is it'
                    elif question_type == QUESTION_TYPE_CAN:
                        question_word = 'Can it'
                    else:
                        question_word = 'Hmmm'
                        
                    break
            
            value = self.name
            
            if question_type == QUESTION_TYPE_IS:
                question_word = 'Is it'
            elif question_type == QUESTION_TYPE_CAN:
                question_word = 'Can it be'
            else:
                question_word = 'Hmmm'
                
            break
        
        return f'{question_word} {value}?'


def create_mutually_exclusive_detail_group(*details):
    details = frozenset(details)
    if len(details) > 1:
        for detail in details:
            detail.mutually_exclusive_with = details


class DescribedObject:
    """
    Creates a new described object. Described objects already have set details, not like regular objects.
    
    Attributes
    ----------
    details : `frozenset` of ``Detail``
        The details of the object.
    object : ``Object``
        The described object.
    """
    __slots__ = ('details', 'object')
    
    def __new__(cls, object_):
        selected_details = []
        choice_details = [*object_.true_details, *object_.true_details, *object_.optional_details]
        
        while choice_details:
            chosen_detail = choice(choice_details)
            selected_details.append(chosen_detail)
            
            mutually_exclusive_with = chosen_detail.mutually_exclusive_with
            if mutually_exclusive_with is None:
                choice_details = [detail for detail in choice_details if detail is not chosen_detail]
            else:
                choice_details = [detail for detail in choice_details if detail not in mutually_exclusive_with]
        
        self = object.__new__(cls)
        self.details = frozenset(selected_details)
        self.object = object_
        return self
    
    
    def __repr__(self):
        return f'<{self.__class__.__name__} name = {self.object.name}, details = {self.details!r}>'


class Object:
    """
    An object which can be guessed. Helps to auto generate questions depending on excluded details.
    
    Parameters
    ----------
    category : `str`
        The categories within the object is.
    optional_details : `frozenset` of ``Detail``
        Details which can be true.
    true_details : `frozenset` of ``Detail``
        Details about the object.
    name : `str`
        The object's name.
    """
    __slots__ = ('category', 'optional_details', 'true_details', 'name')
    
    def __new__(cls, category, name, true_details, optional_details):
        true_details = frozenset(true_details)
        optional_details = frozenset(optional_details)
        
        for detail in true_details:
            detail.increase_sort_value(2)
        
        for detail in optional_details:
            detail.increase_sort_value(1)
        
        self = object.__new__(cls)
        self.category = category
        self.name = name
        self.true_details = true_details
        self.optional_details = optional_details
        
        try:
            objects = OBJECTS_BY_CATEGORY[category]
        except KeyError:
            objects = []
            OBJECTS_BY_CATEGORY[category] = objects
        
        objects.append(self)
        
        return self
    
    
    def __repr__(self):
        return f'<{self.__class__.__name__} name = {self.name!r}>'
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.category != other.category:
            return False
        
        if self.optional_details != other.optional_details:
            return False
        
        if self.true_details != other.true_details:
            return False
        
        if self.name != other.name:
            return False
        
        return True
    
    
    def __gt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.name > other.name:
            return True
        
        return False
    
    
    def __lt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.name < other.name:
            return True
        
        return False
    
    
    def __hash__(self):
        hash_value = 0
        hash_value ^= hash(self.category)
        hash_value ^= hash(self.optional_details)
        hash_value ^= hash(self.true_details)
        hash_value ^= hash(self.name)
        return hash_value


CATEGORY_FRUIT = 'fruit'


DETAIL_FRUIT_HARD_OUTSIDE = Detail(CATEGORY_FRUIT, 'hard outside')
DETAIL_FRUIT_HARD_INSIDE = Detail(CATEGORY_FRUIT, 'hard inside')

DETAIL_FRUIT_SOFT_OUTSIDE = Detail(CATEGORY_FRUIT, 'soft outside')
DETAIL_FRUIT_SOFT_INSIDE = Detail(CATEGORY_FRUIT, 'soft inside')

DETAIL_FRUIT_RED_OUTSIDE = Detail(CATEGORY_FRUIT, 'red outside')
DETAIL_FRUIT_RED_INSIDE = Detail(CATEGORY_FRUIT, 'red inside')

DETAIL_FRUIT_GREEN_OUTSIDE = Detail(CATEGORY_FRUIT, 'green outside')
DETAIL_FRUIT_GREEN_INSIDE = Detail(CATEGORY_FRUIT, 'green inside')

DETAIL_FRUIT_YELLOW_OUTSIDE = Detail(CATEGORY_FRUIT, 'yellow outside')
DETAIL_FRUIT_YELLOW_INSIDE = Detail(CATEGORY_FRUIT, 'yellow inside')

DETAIL_FRUIT_WHITE_OUTSIDE = Detail(CATEGORY_FRUIT, 'white outside')
DETAIL_FRUIT_WHITE_INSIDE = Detail(CATEGORY_FRUIT, 'white inside')

DETAIL_FRUIT_SWEET = Detail(CATEGORY_FRUIT, 'sweet')
DETAIL_FRUIT_SOUR = Detail(CATEGORY_FRUIT, 'sour')

DETAIL_FRUIT_GROWS_ON_TREES = Detail(
    CATEGORY_FRUIT,
    'grows on trees',
    value_by_question_type = {
        QUESTION_TYPE_IS: 'growing on trees',
        QUESTION_TYPE_CAN: 'grow on trees',
    },
)
DETAIL_FRUIT_GROWS_ON_BUSHES = Detail(
    CATEGORY_FRUIT,
    'grows on bushes',
    value_by_question_type = {
        QUESTION_TYPE_IS: 'growing on bushes',
        QUESTION_TYPE_CAN: 'grow on bushes',
    },
)

DETAIL_FRUIT_BROWN_OUTSIDE = Detail(CATEGORY_FRUIT, 'brown outside')
DETAIL_FRUIT_BROWN_INSIDE = Detail(CATEGORY_FRUIT, 'brown inside')

DETAIL_FRUIT_PINK_OUTSIDE = Detail(CATEGORY_FRUIT, 'pink outside')
DETAIL_FRUIT_PINK_INSIDE = Detail(CATEGORY_FRUIT, 'pink inside')

DETAIL_FRUIT_ORANGE_OUTSIDE = Detail(CATEGORY_FRUIT, 'orange outside')
DETAIL_FRUIT_ORANGE_INSIDE = Detail(CATEGORY_FRUIT, 'orange inside')

DETAIL_FRUIT_GROWS_ON_VINE_LIKE_PLANTS = Detail(
    CATEGORY_FRUIT,
    'grows on vine-like plants',
    value_by_question_type = {
        QUESTION_TYPE_IS: 'growing on vine-like plants',
        QUESTION_TYPE_CAN: 'grow on vine-like plants',
    },
)
DETAIL_FRUIT_GROWS_ON_HERBACEOUS_PLANTS = Detail(
    CATEGORY_FRUIT,
    'grows on herbaceous plants',
    value_by_question_type = {
        QUESTION_TYPE_IS: 'growing on herbaceous plants',
        QUESTION_TYPE_CAN: 'grow on herbaceous plants',
    },
)

create_mutually_exclusive_detail_group(
    DETAIL_FRUIT_HARD_OUTSIDE,
    DETAIL_FRUIT_SOFT_OUTSIDE,
)

create_mutually_exclusive_detail_group(
    DETAIL_FRUIT_HARD_INSIDE,
    DETAIL_FRUIT_SOFT_INSIDE,
)


create_mutually_exclusive_detail_group(
    DETAIL_FRUIT_SWEET,
    DETAIL_FRUIT_SOUR,
)

create_mutually_exclusive_detail_group(
    DETAIL_FRUIT_RED_OUTSIDE,
    DETAIL_FRUIT_GREEN_OUTSIDE,
    DETAIL_FRUIT_YELLOW_OUTSIDE,
    DETAIL_FRUIT_WHITE_OUTSIDE,
    DETAIL_FRUIT_BROWN_OUTSIDE,
    DETAIL_FRUIT_PINK_OUTSIDE,
    DETAIL_FRUIT_ORANGE_OUTSIDE,
)

create_mutually_exclusive_detail_group(
    DETAIL_FRUIT_RED_INSIDE,
    DETAIL_FRUIT_GREEN_INSIDE,
    DETAIL_FRUIT_YELLOW_INSIDE,
    DETAIL_FRUIT_WHITE_INSIDE,
    DETAIL_FRUIT_BROWN_INSIDE,
    DETAIL_FRUIT_PINK_INSIDE,
    DETAIL_FRUIT_ORANGE_INSIDE,
)

create_mutually_exclusive_detail_group(
    DETAIL_FRUIT_GROWS_ON_TREES,
    DETAIL_FRUIT_GROWS_ON_BUSHES,
    DETAIL_FRUIT_GROWS_ON_VINE_LIKE_PLANTS,
    DETAIL_FRUIT_GROWS_ON_HERBACEOUS_PLANTS,
)


OBJECT_FRUIT_APPLE = Object(
    CATEGORY_FRUIT,
    'apple',
    [
        DETAIL_FRUIT_HARD_OUTSIDE,
        DETAIL_FRUIT_HARD_INSIDE,
        DETAIL_FRUIT_WHITE_INSIDE,
        DETAIL_FRUIT_SWEET,
        DETAIL_FRUIT_GROWS_ON_TREES,
    ],
    [
        DETAIL_FRUIT_RED_OUTSIDE,
        DETAIL_FRUIT_GREEN_OUTSIDE,
        DETAIL_FRUIT_YELLOW_OUTSIDE,
        DETAIL_FRUIT_SOUR,
    ],
)

OBJECT_FRUIT_PEAR = Object(
    CATEGORY_FRUIT,
    'pear',
    [
        DETAIL_FRUIT_HARD_OUTSIDE,
        DETAIL_FRUIT_HARD_INSIDE,
        DETAIL_FRUIT_WHITE_INSIDE,
        DETAIL_FRUIT_SWEET,
        DETAIL_FRUIT_GROWS_ON_TREES,
    ],
    [
        DETAIL_FRUIT_GREEN_OUTSIDE,
        DETAIL_FRUIT_YELLOW_OUTSIDE,
        DETAIL_FRUIT_BROWN_OUTSIDE,
    ],
)

OBJECT_FRUIT_PEACH = Object(
    CATEGORY_FRUIT,
    'peach',
    [
        DETAIL_FRUIT_SWEET,
        DETAIL_FRUIT_GROWS_ON_TREES,
    ],
    [
        DETAIL_FRUIT_HARD_OUTSIDE,
        DETAIL_FRUIT_HARD_INSIDE,
        DETAIL_FRUIT_SOFT_OUTSIDE,
        DETAIL_FRUIT_SOFT_INSIDE,
        DETAIL_FRUIT_RED_OUTSIDE,
        DETAIL_FRUIT_YELLOW_OUTSIDE,
        DETAIL_FRUIT_PINK_OUTSIDE,
    ],
)

OBJECT_FRUIT_WATERMELON = Object(
    CATEGORY_FRUIT,
    'watermelon',
    [
        DETAIL_FRUIT_HARD_OUTSIDE,
        DETAIL_FRUIT_SOFT_INSIDE,
        DETAIL_FRUIT_RED_INSIDE,
        DETAIL_FRUIT_GREEN_OUTSIDE,
        DETAIL_FRUIT_SWEET,
    ],
    [
        DETAIL_FRUIT_GROWS_ON_VINE_LIKE_PLANTS,
    ],
)

OBJECT_FRUIT_STRAWBERRY = Object(
    CATEGORY_FRUIT,
    'strawberry',
    [
        DETAIL_FRUIT_SOFT_OUTSIDE,
        DETAIL_FRUIT_SOFT_INSIDE,
        DETAIL_FRUIT_SWEET,
    ],
    [
        DETAIL_FRUIT_RED_OUTSIDE,
        DETAIL_FRUIT_RED_INSIDE,
        DETAIL_FRUIT_WHITE_OUTSIDE,
        DETAIL_FRUIT_WHITE_INSIDE,
        DETAIL_FRUIT_PINK_OUTSIDE,
    ],
)

OBJECT_FRUIT_BANANA = Object(
    CATEGORY_FRUIT,
    'banana',
    [
        DETAIL_FRUIT_SOFT_OUTSIDE,
        DETAIL_FRUIT_SOFT_INSIDE,
        DETAIL_FRUIT_YELLOW_OUTSIDE,
        DETAIL_FRUIT_YELLOW_INSIDE,
        DETAIL_FRUIT_GROWS_ON_HERBACEOUS_PLANTS,
        DETAIL_FRUIT_SWEET,
    ],
    [
        DETAIL_FRUIT_GREEN_OUTSIDE,
        DETAIL_FRUIT_RED_OUTSIDE,
    ],
)

OBJECT_FRUIT_ORANGE = Object(
    CATEGORY_FRUIT,
    'orange',
    [
        DETAIL_FRUIT_ORANGE_OUTSIDE,
        DETAIL_FRUIT_ORANGE_INSIDE,
        DETAIL_FRUIT_SOFT_OUTSIDE,
        DETAIL_FRUIT_SOFT_INSIDE,
        DETAIL_FRUIT_GROWS_ON_TREES,
        DETAIL_FRUIT_SWEET,
    ],
    [
        DETAIL_FRUIT_SOUR,
    ],
)


def get_details_sorted_no_filter(category):
    try:
        details = DETAILS_BY_CATEGORY[category]
    except KeyError:
        return []
    
    return sorted(details)


class AllowedDetailQuestion:
    """
    """
    __slots__ = ('detail', 'allowed_question_types')
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.detail != other.detail:
            return False
        
        if self.allowed_question_types != other.allowed_question_types:
            return False
        
        return True



def get_details_sorted_filter(category, answers):
    try:
        details = DETAILS_BY_CATEGORY[category]
    except KeyError:
        return []
    
    disallowed_details = set()
    
    for answer in answers:
        if answer.result:
            detail = answer.detail
            mutually_exclusive_with = detail.mutually_exclusive_with
            if mutually_exclusive_with is None:
                disallowed_details.add(detail)
            else:
                disallowed_details.update(mutually_exclusive_with)
        else:
            disallowed_details.add(detail)
    
    return sorted(set(details) - disallowed_details)


def get_random_object(category):
    try:
        objects = OBJECTS_BY_CATEGORY[category]
    except KeyError:
        return None
    
    return choice(objects)


class Question:
    """
    A question asked from the user.
    
    Attributes
    ----------
    type : `int`
        The question's type.
    detail : ``Detail``
        The detail to ask about.
    """
    __slots__ = ('type', 'detail')
    
    def __new__(cls, type_, detail):
        self = object.__new__(cls)
        self.type = type_
        self.detail = detail
        return self
    
    def __repr__(self):
        return f'<{self.__class__.__name__} type={get_question_type_name(self.type)}, detail={self.detail!r}>'
    
    def ask(self):
        return self.detail.get_question_for(self.type)
    


class Answer(Question):
    """
    A question asked from the user.
    
    Attributes
    ----------
    type : `int`
        The question's type.
    detail : ``Detail``
        The detail to ask about.
    response : `bool`
        The response on the question.
    """
    def __new__(cls, question, response):
        self = object.__new__(cls)
        self.type = question.type
        self.detail = question.detail
        self.response = response
    
    def __repr__(self):
        return (
            f'<{self.__class__.__name__} '
                f'type={get_question_type_name(self.type)}, '
                f'detail={self.detail!r}, '
                f'response={self.response!r}'
            f'>'
        )
    
    def answer(self):
        return 'Yes.' if self.response else 'No.'


class GameState:
    """
    Attributes
    ----------
    described_object : ``DescribedObject``
        The target object what we are trying to guess.
    options : `list` of ``Detail``
        The options allowed for the users to select from.
    event : ``InteractionEvent``
        The user who invoked the game.
    message : `None`, ``Message``
        The message with what the game is operating with.
    client : ``Client``
        The client with who the event operates with.
    questions : `list` of ``Question``
        Questions proposed to the user.
    answers : `list` of ``Answer``
        A list of answers submitted.
    """
    __slots__ = ('client', 'described_object', 'event', 'message', 'questions', 'answers')
    
    async def __new__(cls, client, event, category):
        described_object = DescribedObject(get_random_object(category))
        
        self = object.__new__(cls)
        self.described_object = described_object
        self.client = client
        self.event = event
        self.message = None
        self.questions = self.get_questions()
        self.answers = []
        
        ACTIVE_GAMES[event.user.id] = self
        
        try:
            embed, components = self.render()
            
            await client.interaction_response_message_create(event, embed = embed, components = components)
            message = await client.interaction_response_message_get(event)
        except:
            try:
                del ACTIVE_GAMES[event.user.id]
            except KeyError:
                pass
            
            raise
        
        self.message = message
        
        return self
    
    
    def get_questions(self):
        details = get_details_sorted_no_filter(self.described_object.object.category)
        questions = []
        
        questions_left = QUESTION_COUNT
        while details and questions_left:
            index = ceil(sqrt(randint(0, (len(details) - 1) ** 2)))
            
            type_ = get_question_type()
            detail = details.pop(index)
            
            questions.append(Question(type_, detail))
            
            questions_left -= 1
        
        return questions
    
    
    def render(self):
        embed = Embed()
        user = self.event.user
        embed.add_footer(user.full_name, user.avatar_url)
        
        
        for answer in self.answers:
            embed.add_field(answer.ask(), answer.answer())
        
        components = [
            Button(question.ask(), custom_id = f'{CUSTOM_ID_QUESTION_BASE}.{index}')
            for index, question in enumerate(self.questions)
        ]
        
        return embed, components
    
    
    def get_question_answer(self, question):
        question_type = question.type
        detail = question.detail
        if question_type == QUESTION_TYPE_IS:
            response = detail in self.described_object
        
        elif question_type == QUESTION_TYPE_IS:
            object_ = self.described_object.object
            response = (detail in object_.true_details) or (detail in object_.optional_details)
        
        else:
            response = False
        
        answer = Answer(question, response)
        self.answers.append(answer)
    
    
    async def select_question(self, event, index):
        questions = self.questions
        if index >= questions:
            return
        
        question = questions[index]
        self.get_question_answer(question)
        

        


CATEGORIES = [
    CATEGORY_FRUIT,
]



@SLASH_CLIENT.interactions(guild = GUILD__SUPPORT)
async def rember_preview(
    client,
    event,
    category: (CATEGORIES, 'Select a category'),
):
    try:
        active_game = ACTIVE_GAMES[event.user.id]
    except KeyError:
        pass
    else:
        message = active_game.message
        if message is None:
            components = None
        else:
            components = Button('Go there', url = message.url)
            
        abort('You are already in a game', components = components)
        return
    
    await GameState(client, event, category)


CUSTOM_ID_QUESTION_BASE = 'help_me_rember.question'


@SLASH_CLIENT.interactions(custom_id = re.compile(f'{re.escape(CUSTOM_ID_QUESTION_BASE)}\.(\d+)'))
async def select_question(event, index):
    user = event.user
    if event.message.interaction.user is not user:
        return
    
    try:
        active_game = ACTIVE_GAMES[event.user.id]
    except KeyError:
        return InteractionResponse(components = None) # KEKW
    
    await active_game.select_question(event, index)
