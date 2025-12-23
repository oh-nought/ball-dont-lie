## rule: referee_required
**description**: all queries must conditino on at least one referee. enforces the app's defining constraint and prevents generic stat queries.
**applies_to**: all intents
**logic**: query must include a referee entity or referee_condition dimension
**error**: "Please specify a referee."

## rule: metric_entity_compatibility
**description**: requested metric must support the requested entity
**applies_to**: lookup, comparison, trend
**logic**: valid entities of some metric must be real entities
**error**: "Metric cannot be evaluated for the specified entity."

## rule: grain_alignment
**description**: aggregations must respect metric grain
**applies_to**: all intents
**logic**: planner can aggregate up, not down from grain. comparisons must operate on compatible grains
**error**: "Specified aggregation is not compatible with this metric's grain."

## rule: minimum_sample_size (unsure yet)
**description**: metric-specific constraints must be satisfied
**applies_to**: all intents
**logic**: enforce metric constraints before execution. comparisons require both sides to satisfy constraints independently
**error**: "Sample size is too small to compute this metric reliably."

## rule: comparison_baseline_alignment
**description**: both sides of a comparison must share core filters
**applies_to**: comparison intents
**required alignment**: season, season_type, referee_condition, entity role
**error**: "Comparison baseline doesn't match the context of the query."