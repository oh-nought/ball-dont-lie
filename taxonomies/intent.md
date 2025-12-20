## intent: lookup
**description**: for single metric, specific referee-entity context
**required**: metric
**optional**: entity (player, team, referee), filters (season, w/wo referee, home/away)
**output**: single value or small fixed set of data
**planner template**: resolve entity -> apply filters -> compute metric
**examples**: "scott foster fouls per game this season", "lakers free throw differential with Tony Brothers"

## intent: leaderboard
**description**: rank a set of entities by a metric under filters if used
**required**: metric
**optional**: entity, filters, ranking (top X, bottom X)
**output**: ordered list of entities with metric values
**planner template**: group by entity -> aggregate metric -> apply filters -> sort -> limit
**examples**: "which refs call the most fouls on the Heat?", "top 5 refs by home point differential"

## intent: comparison
**description**: compare the same metric for two or more conditions/entities
**required**: metric, comparison
**optional**: entity, filters
**output**: metric value per condition or relative comparison (kinda vague)
**planner template**: compute metric for condition A -> compute metric for condition B -> compute difference or ratio
**examples**: "Chris Paul win rate under Scott Foster vs Tony Brothers", "celtics with john goble vs without"

## intent: trend
**description**: show how a metric changes over time
**required**: metric
**optional**: entity, time (game, season), filters
**output**: ordered time series of metric values
**planner template**: group by time -> aggregate metric -> sort by time
**examples**: "scott foster foul rate by season", "has jacyn goble gotten stricter this season?"

## intent: filter
**description**: return entities that satisfy metric constraint(s)
**required**: metric, threshold/condition
**optional**: entity, (extra) filters
**output**: list of entities meeting criteria
**planner template**: group by entity -> aggregate metric -> apply filters/constraints

