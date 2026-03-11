# Market-place-core

Provides core logic for market place management, mainly including the `MarketPlaceItem` type.

### Queries

- `insert_market_place_item`
- `update_market_place_item`
- `delete_market_place_item`
- `get_market_place_item`
- `get_market_place_item_listing_active`
- `get_market_place_item_listing_inbox`
- `get_market_place_item_listing_own_offers`

The insert only inserts the initial fields, so the rest should be correctly defaulted by the database.
The update only modifies the fields that are expected to be modified, so the flags & the purchaser fields.

### Flags

- `MARKET_PLACE_ITEM_FLAG_BUYER_RETRIEVED`
- `MARKET_PLACE_ITEM_FLAG_SELLER_RETRIEVED`

These should be used to mark whether the buyer / retrieved their reward.

### Custom id-s

- `CUSTOM_ID_MARKET_PLACE_OFFER_BUILDER`
- `CUSTOM_ID_MARKET_PLACE_OFFER_RP`

The builder one can be used from externally reference the market place offer.
While the regex pattern is used to handle it by the `market_place_command` plugin.
