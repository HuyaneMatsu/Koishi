# Market Place commands

This plugin adds the market place commands & handles their interactions.

The following commands are exposed by it:

- `market-place`
    - `sell(item : Autocomplete<string>, amount : expression, days : Choice<integer> = 5, starting-sell-price : null | expression = null)`
    - `own-offers`
    - `inbox`
    - `view(category : null | Choice<string> = null, item : null | Autocomplete<string> = null)`

You cannot sell / bid / claim while on adventure, so make sure you time everything well.

The inbox items are automatically discarded after 1 week by `market_place_core`,
so make sure you claim them before it is too late.

The system does no scheduling, everything is calculated on queries, so there are no notifications for winning an offer.

### Additional mechanics

- Upon bidding, the new bid has to be a specific % or flat amount higher than the previous one (if any).
    The higher of the two is picked.
- Upon bidding close to the finalisation of an offer, the finalisation time is delayed.
    This is to avoid campers sniping the offers.
