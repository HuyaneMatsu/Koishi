# Adventure - Core

Adventure operations on 2 types: adventure, adventure action.
The adventure represents the general information about an adventure, while each adventure action bound to it represent
different steps of it.
There are 2 steps that are not represented: Depart and Return. These can be calculated from when the a adventure was
created and last updated if it is finalized.

An adventure flow is the following:

- depart
    - arrival -> action stepping
    - cancellation -> return

- action stepping
    - cancellation -> return
    - action stepping
    - return

The adventure is stepped till:

- The adventure is cancelled.
- Time limit is hit.
- Health is less or equal to 0. (Battles are not implemented yet, so this is not added.)
- Cancellation condition says so.


# Adventure drop rarity tears

The user goes to an adventure to collect items. These items come in different tiers:

- Certain : guaranteed 100%
- Basic : under 100 - 40%
- Common : under 40 - 20%
- Uncommon : under 20 - 4%
- Rare : under 4 - 0.8%
- Epic : under 0.8 - 0.1%
- Mythical : Under 0.1%

# Adventure locations

In adventures the user can select different locations to adventure to. These locations offer different "target"-s.
Interpret them as tasks to do. These targets have their own possible actions to be chosen on each step.
Each action offers their own cost, battles and loot.

- Human village outskirts (level 0)
    - Gardening (Scarlet onions)
        - Gardening
            - Scarlet onion (certain)
            - Scarlet onion (rare)
            - Frog (epic)
            - Straw hat (mythical)
    - Gardening (Carrots)
        - Gardening
            - Carrot (certain)
            - Carrot (rare)
            - Frog (epic)
            - Straw hat (mythical)
    - Gardening (Garlic)
        - Gardening
            - Garlic (certain)
            - Garlic (rare)
            - Frog (epic)
            - Straw hat (mythical)

- Bamboo Forest (level 0)
    - Foraging
        - Foraging (bamboo)
            - Bamboo shoot (certain)
            - Bishophat (uncommon)
            - Scissors (epic)
        - Foraging (mushroom)
            - Devilcart oyster (basic)
            - Flykiller amanita (uncommon)
            - Bishophat (uncommon)
            - Scissors (mythical)
        - Trapped

- Human village vineyards (level 0)
    - Vine growing
        - Gardening
            - Bluefrankish (certain)
            - Bluefrankish (rare)
            - Straw hat (epic)
            - Scissors (mythical)
        - Gardening
            - Twigs (certain)
            - Bough (rare)

- Ruins (level 1)
    - Foraging
        - Foraging
            - Strawberry (basic)
            - Bishophat (rare)
            - Ribbon bow (mythical)
            - Plushie bear (mythical)
            - Gothic attire (mythical)

- Eientei mansion (level 1)
    - Gardening
        - Gardening
            - Carrot (certain)
            - Frog (epic)
            - Kimono (mythical)
        - Trapped

- Magic forest (level 1)
    - Foraging
        - Foraging
            - Devilcart oyster (basic)
            - Flykiller amanita (common)
            - Bishophat (uncommon)
            - Ruler (epic)
            - Scissors (mythical)
    - Collect firewood
        - Foraging
            - Twigs (basic)
            - Bough (basic)
            - Ruler (mythical)
            - Scissors (mythical)
        - Foraging
            - Devilcart oyster (basic)
            - Flykiller amanita (common)
            - Bishophat (uncommon)
            - Ruler (mythical)
            - Scissors (mythical)

- Hakugyokurou mansion (level 2)
    - Gardening
        - Gardening
            - Peach (basic)
            - Peach (rare)
            - Hand fan (mythical)
            - Parasol (mythical)
        - Gardening
            - Twigs (basic)
            - Bough (uncommon)

- Moriya shrine (level 2)
    - Foraging
        - Foraging
            - BlueBerry (basic)
            - Kitchen knife (mythical)
            - Poking knife (mythical)
            - Broom (mythical)

- Misty lake (level 2)
    - Foraging
        - Foraging
            - Frog (basic)
            - Angelroot (basic)
            - Fishing rod (rare)
            - Hiking set (mythical)
