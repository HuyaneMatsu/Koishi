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

- Human village outskirts
    - Gardening (Scarlet onions)
        - Gardening
            - Scarlet onion (certain)
            - Scarlet onion (rare)
            - Frog (epic)
    - Gardening (Carrots)
        - Gardening
            - Carrot (certain)
            - Carrot (rare)
            - Frog (epic)
    - Gardening (Garlic)
        - Gardening
            - Garlic (certain)
            - Garlic (rare)
            - Frog (epic)

- Human village vineyards
    - Vine growing
        - Gardening
            - Bluefrankish (certain)
            - Bluefrankish (rare)

- Ruins
    - Foraging
        - Foraging
            - Strawberry (basic)
            - Bishophat (rare)

- Eientei mansion
    - Gardening
        - Gardening
            - Carrot (certain)
            - Frog (epic)
        - Trapped

- Bamboo Forest
    - Foraging
        - Foraging
            - Devilcart oyster (basic)
            - Flykiller amanita (uncommon)
            - Bishophat (rare)
            - Scissors (epic)
        - Trapped

- Hakugyokurou mansion
    - Gardening
        - Gardening
            - Peach (basic)
            - Peach (rare)

- Moriya shrine
    - Foraging
        - Foraging
            - BlueBerry (basic)

- Misty lake
    - Foraging
        - Foraging
            - Frog (basic)
            - Angelroot (basic)
            - Fishing rod (rare)
