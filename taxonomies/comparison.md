## comparison: with_vs_without_referee
**description**: compares a metric when a referee is present vs absent
**structure**: baseline: without referee X, comparison: with referee X
**output**: absolute difference, percent difference
**notes**: default output is absolute difference

## comparison: referee_vs_league_average
**description**: compares referee conditioned metric to league wide baseline
**structure**: baseline: league average (same filters), comparison: referee conditioned value
**output**: delta/difference
**notes**: N/A

## comparison: home_vs_away_under_referee
**description**: compares home vs away outcomes officiated by some referee
**structure**: entity when home, entity when away, shared referee filter
**output**: absolute difference, ratio
**notes**:

## comparison: entity_vs_entity_under_referee
**description**: compares two entities when officiated by some referee
**structure**: entity A, entity B, shared referee filter
**output**: absolute difference, percent difference
**notes**:

## global constraints
- both sides must satisfy metric constraints
- both sides must share season, season type, referee condition