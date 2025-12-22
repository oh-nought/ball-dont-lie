## filter: season
**description**: restricts analysis to a specific NBA season
**type**: time
**values**: single seasno, multiple seasons, all-time
**applies to**: all metrics
**default**: current season
**required**: no
**notes**: all-time is an aggregation over seasons from 2003 to now, playoffs are excluded unless specified

## filter: season_type
**description**: restricts analysis to a specific season type
**type**: category
**values**: regular season, playoffs
**applies to**: all metrics
**default**: regular season
**required**: no
**notes**: some analyses might require bigger sample sizes for playoff metrics

## filter: referee_condition
**description**: conditions 
**type**: relation
**values**: with referee X, without referee X
**applies to**: all metrics
**default**: N/A
**required**: yes
**notes**: "with" means referee is part of the officiating crew (1/3)

## filter: home_away
**description**: restricts analysis based on home or away status
**type**: category
**values**: home, away, both
**applies to**: team metrics, player metrics
**default**: both
**required**: no
**notes**: pairs naturally with foul and win rate metrics

## filter: game_window
**description**: restricts games to a window if specified
**type**: time
**values**: last N games, specific dates, month ranges, full season
**applies to**: all metrics
**default**: full season
**required**: no
**notes**: referees are to be filtered first

## filter: opponent
**description**: restricts games by opponent
**type**: relation
**values**: specific team
**applies to**: player metrics, team metrics
**default**: N/A
**required**: no
**notes**: optional dimension

## filter: game_context
**description**: restricts gamesby situational context
**type**: condition
**values**: close games
**applies to**: foul metrics, free throw metrics
**default**: N/A
**required**: no
**notes**: optional dimension