import vampytest

from ....touhou_core import CHEN, YAKUMO_RAN, YAKUMO_YUKARI

from ..action import ImageDetailAction
from ..provided import ImageDetailProvided


def _assert_fields_set(image_detail):
    """
    Asserts whether every fields of the image detail are set.
    
    Parameters
    ----------
    image_detail : ``ImageDetailProvided``
        The image detail to test.
    """
    vampytest.assert_instance(image_detail, ImageDetailProvided)
    vampytest.assert_instance(image_detail.url, str)
    vampytest.assert_instance(image_detail.provider, str, nullable = True)
    vampytest.assert_instance(image_detail.tags, frozenset, nullable = True)


def test__ImageDetailProvided__new():
    """
    Tests whether ``ImageDetailProvided.__new__`` works as intended.
    """
    url = 'https://www.orindance.party/'
    
    image_detail = ImageDetailProvided(url)
    _assert_fields_set(image_detail)
    vampytest.assert_eq(image_detail.url, url)


def test__ImageDetailProvided__provider():
    """
    Tests whether ``ImageDetailProvided.provider`` works as intended.
    """
    url = 'https://www.orindance.party/'
    
    image_detail = ImageDetailProvided(url)
    
    vampytest.assert_is(image_detail.provider, None)


def test__ImageDetailProvided__tags():
    """
    Tests whether ``ImageDetailProvided.tags`` works as intended.
    """
    url = 'https://www.orindance.party/'
    
    image_detail = ImageDetailProvided(url)
    
    vampytest.assert_is(image_detail.tags, None)


def test__ImageDetailProvided__with_provider():
    """
    Tests whether ``ImageDetailProvided.with_provider`` works as intended.
    """
    url = 'https://www.orindance.party/'
    provider = 'hey mister'
    
    image_detail = ImageDetailProvided(url)
    output = image_detail.with_provider(provider)
    vampytest.assert_is(image_detail, output)
    
    
    vampytest.assert_is(image_detail.provider, provider)


def test__ImageDetailProvided__with_tags():
    """
    Tests whether ``ImageDetailProvided.with_tags`` works as intended.
    """
    url = 'https://www.orindance.party/'
    tags = frozenset(('hey', 'mister'))
    
    image_detail = ImageDetailProvided(url)
    output = image_detail.with_tags(tags)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_is(image_detail.tags, tags)


def test__ImageDetailProvided__repr():
    """
    Tests whether ``ImageDetailProvided.__repr__`` works as intended.
    """
    url = 'https://www.orindance.party/'
    provider = 'hey mister'
    tags = frozenset(('hey', 'mister'))
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_provider(provider)
    image_detail.with_tags(tags)
    
    output = repr(image_detail)
    vampytest.assert_instance(output, str)


def test__ImageDetailProvided__hash():
    """
    Tests whether ``ImageDetailProvided.__hash__`` works as intended.
    """
    url = 'https://www.orindance.party/'
    
    image_detail = ImageDetailProvided(url)
    
    output = hash(image_detail)
    vampytest.assert_instance(output, int)


def _iter_options__eq__same_type():
    url_0 = 'https://www.orindance.party/'
    url_1 = 'https://www.orindance.party/?ehy=mister'
    
    yield url_0, url_0, True
    yield url_0, url_1, False


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__ImageDetailProvided__eq__same_type(url_0, url_1):
    """
    Tests whether ``ImageDetailProvided__eq__`` works as intended.
    
    Case: Same type.
    
    Parameters
    ----------
    url_0 : `str`
        Url to create instance with.
    url_1 : `str`
        Url to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    image_detail_0 = ImageDetailProvided(url_0)
    image_detail_1 = ImageDetailProvided(url_1)
    
    output = image_detail_0 == image_detail_1
    vampytest.assert_instance(output, bool)
    return output


def test__ImageDetailProvided__eq__different_type():
    """
    Tests whether ``ImageDetailProvided.__eq__`` works as intended.
    
    Case: Different type.
    """
    url = 'https://www.orindance.party/'
    
    image_detail = ImageDetailProvided(url)
    
    output = image_detail == object()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__ImageDetailProvided__characters():
    """
    Tests whether ``ImageDetailProvided.characters`` works as intended.
    """
    url = 'https://www.orindance.party/'
    
    image_detail = ImageDetailProvided(url)
    
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__with_character__none():
    """
    Tests whether ``ImageDetailProvided.with_character`` works as intended.
    
    Case: no characters yet.
    """
    url = 'https://www.orindance.party/'
    character = YAKUMO_RAN
    
    image_detail = ImageDetailProvided(url)
    output = image_detail.with_character(character)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__with_character__with_character():
    """
    Tests whether ``ImageDetailProvided.with_character`` works as intended.
    
    Case: with characters.
    """
    url = 'https://www.orindance.party/'
    character = YAKUMO_RAN
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_character(YAKUMO_YUKARI)
    output = image_detail.with_character(character)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__with_character__with_overlapping_characters():
    """
    Tests whether ``ImageDetailProvided.with_character`` works as intended.
    
    Case: with overlapping characters.
    """
    url = 'https://www.orindance.party/'
    character = YAKUMO_RAN
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_character(YAKUMO_RAN)
    image_detail.with_character(YAKUMO_YUKARI)
    output = image_detail.with_character(character)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__with_characters__none():
    """
    Tests whether ``ImageDetailProvided.with_characters`` works as intended.
    
    Case: no characters yet.
    """
    url = 'https://www.orindance.party/'
    characters = (CHEN, YAKUMO_YUKARI)
    
    image_detail = ImageDetailProvided(url)
    output = image_detail.with_characters(*characters)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__with_characters__with_character():
    """
    Tests whether ``ImageDetailProvided.with_characters`` works as intended.
    
    Case: with character.
    """
    url = 'https://www.orindance.party/'
    characters = (CHEN, YAKUMO_RAN)
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_character(YAKUMO_YUKARI)
    output = image_detail.with_characters(*characters)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__with_characters__with_overlapping_characters():
    """
    Tests whether ``ImageDetailProvided.with_characters`` works as intended.
    
    Case: with overlapping characters.
    """
    url = 'https://www.orindance.party/'
    characters = (CHEN, YAKUMO_RAN)
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_character(YAKUMO_RAN)
    image_detail.with_character(YAKUMO_YUKARI)
    output = image_detail.with_characters(*characters)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__with_action__none():
    """
    Tests whether ``ImageDetailProvided.with_action`` works as intended.
    
    Case: No actions yet.
    """
    url = 'https://www.orindance.party/'
    action = ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI)
    
    image_detail = ImageDetailProvided(url)
    output = image_detail.with_action(*action)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.actions, None)
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__with_action__tuple():
    """
    Tests whether ``ImageDetailProvided.with_action`` works as intended.
    
    Case: Using tuple.
    """
    url = 'https://www.orindance.party/'
    action = ('kiss', YAKUMO_RAN, YAKUMO_YUKARI)
    
    image_detail = ImageDetailProvided(url)
    output = image_detail.with_action(*action)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.actions, None)
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__with_action__with_action():
    """
    Tests whether ``ImageDetailProvided.with_action`` works as intended.
    
    Case: with actions.
    """
    url = 'https://www.orindance.party/'
    action = ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI)
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_action(*ImageDetailAction('lick', YAKUMO_RAN, YAKUMO_YUKARI))
    output = image_detail.with_action(*action)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.actions, None)
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__with_action__with_overlapping_actions():
    """
    Tests whether ``ImageDetailProvided.with_action`` works as intended.
    
    Case: with overlapping actions.
    """
    url = 'https://www.orindance.party/'
    action = ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI)
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_action(*ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI))
    image_detail.with_action(*ImageDetailAction('lick', YAKUMO_RAN, YAKUMO_YUKARI))
    output = image_detail.with_action(*action)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.actions, None)
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__with_actions__none():
    """
    Tests whether ``ImageDetailProvided.with_actions`` works as intended.
    
    Case: no actions yet.
    """
    url = 'https://www.orindance.party/'
    actions = (
        ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI),
        ImageDetailAction('lick', YAKUMO_RAN, YAKUMO_YUKARI),
    )
    
    image_detail = ImageDetailProvided(url)
    output = image_detail.with_actions(*actions)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.actions, None)
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__with_actions__tuple():
    """
    Tests whether ``ImageDetailProvided.with_actions`` works as intended.
    
    Case: using tuple.
    """
    url = 'https://www.orindance.party/'
    actions = (
        ('kiss', YAKUMO_RAN, YAKUMO_YUKARI),
        ('lick', YAKUMO_RAN, YAKUMO_YUKARI),
    )
    
    image_detail = ImageDetailProvided(url)
    output = image_detail.with_actions(*actions)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.actions, None)
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__with_actions__with_action():
    """
    Tests whether ``ImageDetailProvided.with_actions`` works as intended.
    
    Case: with action.
    """
    url = 'https://www.orindance.party/'
    actions = (
        ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI),
        ImageDetailAction('lick', YAKUMO_RAN, YAKUMO_YUKARI),
    )
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_action(*ImageDetailAction('fluff', CHEN, YAKUMO_YUKARI))
    output = image_detail.with_actions(*actions)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.actions, None)
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__with_actions__with_overlapping_actions():
    """
    Tests whether ``ImageDetailProvided.with_actions`` works as intended.
    
    Case: with overlapping actions.
    """
    url = 'https://www.orindance.party/'
    actions = (
        ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI),
        ImageDetailAction('lick', YAKUMO_RAN, YAKUMO_YUKARI),
    )
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_action(*ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI))
    image_detail.with_action(*ImageDetailAction('fluff', CHEN, YAKUMO_YUKARI))
    output = image_detail.with_actions(*actions)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.actions, None)
    vampytest.assert_eq(image_detail.characters, None)


def test__ImageDetailProvided__creators():
    """
    Tests whether ``ImageDetailProvided.creators`` works as intended.
    """
    url = 'https://www.orindance.party/'
    
    image_detail = ImageDetailProvided(url)
    
    vampytest.assert_eq(image_detail.creators, None)


def test__ImageDetailProvided__with_creator__none():
    """
    Tests whether ``ImageDetailProvided.with_creator`` works as intended.
    
    Case: no creators yet.
    """
    url = 'https://www.orindance.party/'
    creator = 'pudding'
    
    image_detail = ImageDetailProvided(url)
    output = image_detail.with_creator(creator)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.creators, None)


def test__ImageDetailProvided__with_creator__with_creator():
    """
    Tests whether ``ImageDetailProvided.with_creator`` works as intended.
    
    Case: with creators.
    """
    url = 'https://www.orindance.party/'
    creator = 'pudding'
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_creator('lord')
    output = image_detail.with_creator(creator)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.creators, None)


def test__ImageDetailProvided__with_creator__with_overlapping_creators():
    """
    Tests whether ``ImageDetailProvided.with_creator`` works as intended.
    
    Case: with overlapping creators.
    """
    url = 'https://www.orindance.party/'
    creator = 'pudding'
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_creator('pudding')
    image_detail.with_creator('lord')
    output = image_detail.with_creator(creator)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.creators, None)


def test__ImageDetailProvided__with_creators__none():
    """
    Tests whether ``ImageDetailProvided.with_creators`` works as intended.
    
    Case: no creators yet.
    """
    url = 'https://www.orindance.party/'
    creators = ('frog', 'lord')
    
    image_detail = ImageDetailProvided(url)
    output = image_detail.with_creators(*creators)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.creators, None)


def test__ImageDetailProvided__with_creators__with_creator():
    """
    Tests whether ``ImageDetailProvided.with_creators`` works as intended.
    
    Case: with creator.
    """
    url = 'https://www.orindance.party/'
    creators = ('frog', 'pudding')
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_creator('lord')
    output = image_detail.with_creators(*creators)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.creators, None)


def test__ImageDetailProvided__with_creators__with_overlapping_creators():
    """
    Tests whether ``ImageDetailProvided.with_creators`` works as intended.
    
    Case: with overlapping creators.
    """
    url = 'https://www.orindance.party/'
    creators = ('frog', 'pudding')
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_creator('pudding')
    image_detail.with_creator('lord')
    output = image_detail.with_creators(*creators)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.creators, None)


def test__ImageDetailProvided__editors():
    """
    Tests whether ``ImageDetailProvided.editors`` works as intended.
    """
    url = 'https://www.orindance.party/'
    
    image_detail = ImageDetailProvided(url)
    
    vampytest.assert_eq(image_detail.editors, None)


def test__ImageDetailProvided__with_editor__none():
    """
    Tests whether ``ImageDetailProvided.with_editor`` works as intended.
    
    Case: no editors yet.
    """
    url = 'https://www.orindance.party/'
    editor = 'pudding'
    
    image_detail = ImageDetailProvided(url)
    output = image_detail.with_editor(editor)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.editors, None)


def test__ImageDetailProvided__with_editor__with_editor():
    """
    Tests whether ``ImageDetailProvided.with_editor`` works as intended.
    
    Case: with editors.
    """
    url = 'https://www.orindance.party/'
    editor = 'pudding'
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_editor('lord')
    output = image_detail.with_editor(editor)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.editors, None)


def test__ImageDetailProvided__with_editor__with_overlapping_editors():
    """
    Tests whether ``ImageDetailProvided.with_editor`` works as intended.
    
    Case: with overlapping editors.
    """
    url = 'https://www.orindance.party/'
    editor = 'pudding'
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_editor('pudding')
    image_detail.with_editor('lord')
    output = image_detail.with_editor(editor)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.editors, None)


def test__ImageDetailProvided__with_editors__none():
    """
    Tests whether ``ImageDetailProvided.with_editors`` works as intended.
    
    Case: no editors yet.
    """
    url = 'https://www.orindance.party/'
    editors = ('frog', 'lord')
    
    image_detail = ImageDetailProvided(url)
    output = image_detail.with_editors(*editors)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.editors, None)


def test__ImageDetailProvided__with_editors__with_editor():
    """
    Tests whether ``ImageDetailProvided.with_editors`` works as intended.
    
    Case: with editor.
    """
    url = 'https://www.orindance.party/'
    editors = ('frog', 'pudding')
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_editor('lord')
    output = image_detail.with_editors(*editors)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.editors, None)


def test__ImageDetailProvided__with_editors__with_overlapping_editors():
    """
    Tests whether ``ImageDetailProvided.with_editors`` works as intended.
    
    Case: with overlapping editors.
    """
    url = 'https://www.orindance.party/'
    editors = ('frog', 'pudding')
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_editor('pudding')
    image_detail.with_editor('lord')
    output = image_detail.with_editors(*editors)
    vampytest.assert_is(image_detail, output)
    
    vampytest.assert_eq(image_detail.editors, None)


def _iter_options__iter_actions():
    yield (
        [],
        [],
    )
    
    yield (
        [
            ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI),
            ImageDetailAction('lick', YAKUMO_RAN, YAKUMO_YUKARI),
        ],
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_actions()).returning_last())
def test__ImageDetailProvided__iter_actions(actions):
    """
    Tests whether ``ImageDetailProvided.iter_actions`` works as intended.
    
    Parameters
    ----------
    actions : `list<ImageDetailAction>`
        Actions to create the image detail with.
    
    Returns
    -------
    output : `list<ImageDetailAction>`
    """
    url = 'https://www.orindance.party/'
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_actions(*actions)
    
    return [*image_detail.iter_actions()]



def _iter_options__has_action_tag():
    yield (
        [],
        'lick',
        False
    )
    
    yield (
        [
            ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI),
            ImageDetailAction('lick', YAKUMO_RAN, YAKUMO_YUKARI),
        ],
        'lick',
        False,
    )
    
    yield (
        [
            ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI),
            ImageDetailAction('lick', YAKUMO_RAN, YAKUMO_YUKARI),
        ],
        'hug',
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__has_action_tag()).returning_last())
def test__ImageDetailProvided__has_action_tag(actions, action_tag):
    """
    Tests whether ``ImageDetailProvided.has_action_tag`` works as intended.
    
    Parameters
    ----------
    actions : `list<ImageDetailAction>`
        Actions to create the image detail with.
    action_tag : `str`
        Action tag to check for.
    
    Returns
    -------
    output : `list<ImageDetailAction>`
    """
    url = 'https://www.orindance.party/'
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_actions(*actions)
    
    output = image_detail.has_action_tag(action_tag)
    vampytest.assert_instance(output, bool)
    return output


def test__ImageDetailProvided__copy():
    """
    Tests whether ``ImageDetailProvided.copy`` works as intended.
    """
    url = 'https://www.orindance.party/'
    provider = 'mister'
    tags = frozenset(('its', 'sister'))
    characters = (CHEN, YAKUMO_RAN)
    actions = (
        ImageDetailAction('hug', CHEN, YAKUMO_YUKARI),
        ImageDetailAction('kiss', CHEN, YAKUMO_YUKARI),
    )
    creators = ('hey', 'sister')
    editors = ('to', 'be')
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_provider(provider)
    image_detail.with_tags(tags)
    image_detail.with_characters(*characters)
    image_detail.with_actions(*actions)
    image_detail.with_creators(*creators)
    image_detail.with_editors(*editors)
    
    
    copy = image_detail.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(image_detail, copy)
    
    vampytest.assert_eq(copy.url, image_detail.url)
    vampytest.assert_eq(copy.provider, image_detail.provider)
    vampytest.assert_eq(copy.tags, image_detail.tags)
    vampytest.assert_eq(copy.characters, image_detail.characters)
    vampytest.assert_eq(copy.actions, image_detail.actions)
    vampytest.assert_eq(copy.creators, image_detail.creators)
    vampytest.assert_eq(copy.editors, image_detail.editors)


def test__ImageDetailProvided__create_action_subset__no_matching_actions():
    """
    Tests whether ``ImageDetailProvided.create_action_subset`` works as intended.
    
    Case: No matching actions.
    """
    url = 'https://www.orindance.party/'
    
    actions = (
        ImageDetailAction('hug', CHEN, YAKUMO_YUKARI),
        ImageDetailAction('kiss', CHEN, YAKUMO_YUKARI),
        ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI),
    )
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_actions(*actions)
    
    subset = image_detail.create_action_subset('lick')
    vampytest.assert_is(subset, None)


def test__ImageDetailProvided__create_action_subset__matching_actions():
    """
    Tests whether ``ImageDetailProvided.create_action_subset`` works as intended.
    
    Case: Matching actions.
    """
    url = 'https://www.orindance.party/'
    
    actions = (
        ImageDetailAction('hug', CHEN, YAKUMO_YUKARI),
        ImageDetailAction('kiss', CHEN, YAKUMO_YUKARI),
        ImageDetailAction('kiss', YAKUMO_RAN, YAKUMO_YUKARI),
    )
    
    image_detail = ImageDetailProvided(url)
    image_detail.with_actions(*actions)
    
    subset = image_detail.create_action_subset('kiss')
    vampytest.assert_is(subset, None)


def _iter_options__name():
    yield 'https://www.orindance.party/', ''
    yield 'https://www.orindance.party/koishi.png', 'koishi'
    yield 'https://www.orindance.party/koishi-pocky-0000.png', 'koishi-pocky-0000'


@vampytest._(vampytest.call_from(_iter_options__name()).returning_last())
def test__ImageDetailProvided__name(url):
    """
    Tests whether ``ImageDetailProvided.name`` works as intended.
    
    Parameters
    ----------
    url : `str`
        Url to create the image detail with.
    
    Returns
    -------
    output : `list<ImageDetailAction>`
    """
    image_detail = ImageDetailProvided(url)
    
    output = image_detail.name
    vampytest.assert_instance(output, str)
    return output
