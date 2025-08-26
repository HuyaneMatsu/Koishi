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


# Adventure locations

In adventures the user can select different locations to adventure to. These locations offer different "target"-s.
Interpret them as tasks to do. These targets have their own possible actions to be chosen on each step.
Each action offers their own cost, battles and loot.

- Human village outskirts
    - Gardening (Scarlet onions)
        - Gardening
            - Scarlet onion (guaranteed)
            - Scarlet onion (rare)
    - Gardening (Carrots)
        - Gardening
            - Carrot (guaranteed)
            - Carrot (rare)
    - Gardening (Garlic)
        - Gardening
            - Garlic (guaranteed)
            - Garlic (rare)

- Human village vineyards
    - Vine growing
        - Gardening
            - Bluefrankish (guaranteed)
            - Bluefrankish (rare)

- Ruins
    - Foraging
        - Foraging
            - Strawberry (common)

- Eientei mansion
    - Gardening
        - Gardening
            - Carrot (guaranteed)
        - Trapped

- Bamboo Forest
    - Foraging
        - Foraging
            - Devilcart oyster (common)
            - Flykiller amanata (common)
        - Trapped

- Hakugyokurou mansion
    - Gardening
        - Gardening
            - Peach (common)
            - Peach (rare)

- Moriya shrine
    - Foraging
        - Foraging
            - BlueBerry (common)
