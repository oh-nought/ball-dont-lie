## metric: fouls_called_per_game
**description**: average number of fouls called by a referee per game
**aliases**: "foul calls per game", "foul rate"
**formula**: total fouls called $\div$ games officiated
**grain**: referee-game
**valid entities**: referee
**required**: referee assignments, games table (home_fouls + away_fouls)
**default**: regular season only
**constraints**: referee must have at least 10 games officiated
**bias interpretation**: higher values = stricter?
**SQL mapping**:
```sql
SELECT AVG(home_fouls + away_fouls) as fouls_per_game
FROM games g
JOIN referee_assignments ra ON g.game_id = ra.game_id
WHERE ra.official_code = ...
```

## metric: free_throw_attempts_allowed
**description**: average number of free throw attempts allowed to an entity officiated by some referee
**aliases**: "fta", "free throw attempts", "free throws attempted"
**formula**: total free throw attempts $\div$ games
**grain**: team-game, player-game
**valid entities**: team, player, referee (via team/player games)
**required**: referee assignments, game box score
**default**: regular season only
**constraints**: at least 10 games 
**bias interpretation**: higher value = better whistle?
**SQL mapping**:
```sql
-- player
SELECT AVG(sl.ft_attempted) as fta_per_game
FROM stat_lines sl
JOIN games g ON sl.game_id = g.game_id
JOIN referee_assignments ra ON g.game_id = ra.game_id
WHERE sl.player_id = ... AND ra.official_code = ...

-- team
SELECT AVG(team_fta) AS fta_per_game
FROM (
    SELECT g.game_id, SUM(sl.ft_attempted) AS team_fta
    FROM stat_lines sl
    JOIN games g ON sl.game_id = g.game_id
    WHERE sl.team_id = ...
    GROUP BY g.game_id
) AS sub
JOIN referee_assignments ra ON sub.game_id = ra.game_id
WHERE ra.official_code = ...
```

## metric: field_goal_attempts_allowed
**description**: average number of field goal attempts allowed to an entity officiated by some referee
**aliases**: "fga", "field goal attempts", "shot attempts"
**formula**: total field goal attempts $\div$ games
**grain**: team-game, player-game
**valid entities**:team, player, referee (via team/player games)
**required**: referee assignments, game box score
**default**:regular season only
**constraints**: at least 10 games
**bias interpretation**: mostly contextual
**SQL mapping**:
```sql
-- player
SELECT AVG(sl.fg_attempted) AS fga_per_game
FROM stat_lines sl
JOIN games g ON sl.game_id = g.game_id
JOIN referee_assignments ra ON g.game_id = ra.game_id
WHERE sl.player_id = ... AND ra.refereee_id = ...

-- team
SELECT AVG(team_fga) AS fga_per_game
FROM (
    SELECT g.game_id, SUM(sl.fg_attempted) AS fga_per_game
    FROM stat_lines sl
    JOIN games g ON sl.game_id = g.game_id
    WHERE sl.team_id = ...
    GROUP BY g.game_id
) sub
JOIN referee_assignments ra ON sub.game_id = ra.game_id
WHERE ra.official_code = ...
```

## metric: home_team_win_rate
**description**: winning percentage of home teams in games officiated by some referee
**aliases**: "home win percentage", "home team win %", "home court win rate"
**formula**: home team wins $\div$ games
**grain**: referee-game
**valid entities**: referee
**required**: referee assignments, box score
**default**: regular season only
**constraints**: at least 10 games officiated
**bias interpretation**: higher value = home team favoritism?
**SQL mapping**:
```sql
SELECT SUM(CASE WHEN g.home_score > g.away_score THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS home_win_rate
FROM games g
JOIN referee_assignments ra ON g.game_id = ra.game_id
WHERE ra.official_code = ...
```

## metric: home_team_point_differential
**description**: average point differential in games officiated by some referee
**aliases**: "home point differential", "home point margin"
**formula**: (home points - away points) $\div$ games
**grain**: referee-game
**valid entities**: referee
**required**: referee assignments, box score
**default**: regular season only
**constraints**: at least 10 games officiated
**bias interpretation**: consistent positive values = home team favoritism?
**SQL mapping**:
```sql
SELECT AVG(g.home_score - g.away_score) AS home_point_diff
FROM games g
JOIN referee_assignments ra ON g.game_id = ra.game_id
WHERE ra.official_code = ...
```

## metric: foul_rate_against_home_teams
**description**: percentage of total fouls in a game that are called against the home team
**aliases**: "home team foul rate", "fouls on home team"
**formula**: fouls against home team $\div$ total fouls in game
**grain**: referee-game
**valid entities**: referee
**required**: referee assignments, box score
**default**: regular season only
**constraints**: at least 10 games officiated
**bias interpretation**: lower value = home team has better whistle? 
**SQL mapping**:
```sql
SELECT AVG(home_fouls / (home_fouls + away_fouls)) AS home_foul_rate
FROM (
    SELECT g.game_id, SUM(g.home_fouls), SUM(g.away_fouls)
    FROM games g
    JOIN stat_lines sl ON g.game_id = sl.game_id
    GROUP BY g.game_id, g.home_team_id, g.away_team_id
) foul_counts
JOIN referee_assignments ra ON foul_counts.game_id = ra.game_id
WHERE ra.official_code = ...
```

## metric: combined_points_per_game
**description**: average combined points scored in games officiated by some referee
**aliases**: "total points per game", "combined points", "game total"
**formula**: (homw points + away points) $\div$ games
**grain**: referee-game
**valid entities**: referee
**required**: referee assignments, box score
**default**:regular season only
**constraints**: at least 10 games officiated
**bias interpretation**: mostly contextual
**SQL mapping**:
```sql
SELECT AVG(g.home_score + g.away_score) AS combined_ppg
FROM games g
JOIN referee_assignments ra ON g.game_id = ra.game_id
WHERE ra.official_code = ...
```

## metric: points_per_game
**description**: average points scored per game by an entity officiated by some referee
**aliases**: "points per game", "ppg"
**formula**: total points $\div$ games
**grain**: team-game, player-game
**valid entities**: player, team
**required**: referee assignments, box score
**default**:regular season only
**constraints**: at least 10 games
**bias interpretation**: mostly contextual
**SQL mapping**:
```sql
-- player
SELECT AVG(points) AS ppg
FROM stat_lines sl
JOIN referee_assignments ra ON sl.game_id = ra.game_id
WHERE sl.player_id = ... AND ra.official_code = ...

-- team
SELECT AVG(CASE WHEN g.home_team_id = ... THEN g.home_score WHEN g.away_team_id = ... THEN g.away_score END) as ppg
FROM games g
JOIN referee_assignments ra ON g.game_id = ra.game_id
WHERE (g.home_team_id = ... OR g.away_team_id = ...) AND ra.official_code = ...
```

## metric: home_away_foul_differential
**description**: difference between fouls against road teams and fouls against home teams
**aliases**: "home-away foul differential", "home vs road fouls"
**formula**: (fouls against road teams - fouls against home teams) $\div$ games
**grain**: referee-game
**valid entities**: referee
**required**: referee assignments, box score
**default**:regular season only
**constraints**: at least 10 games officiated
**bias interpretation**: positive value = favor home teams? negative value = favor road teams? 
***SQL mapping**:
```sql
SELECT AVG(away_fouls - home_fouls) AS foul_differential
FROM (
    SELECT g.game_id, SUM(g.home_fouls) AS home_fouls, SUM(g.away_fouls) AS away_fouls
    FROM games g
    JOIN stat_lines sl ON g.game_id = sl.game_id 
    GROUP BY g.game_id, g.home_team_id, g.away_team_id
) foul_counts
JOIN referee_assignments ra ON foul_counts.game_id = ra.game_id
WHERE ra.official_code = ...
```

## metric: fouls_committed_per_game 
**description**: fouls committed by an entity when officiated by some referee
**aliases**: "fouls committed", "fouls per game", "personal fouls", "PF"
**formula**: total fouls committed $\div$ games 
**grain**: team-game, player-game
**valid entities**: player, team, referee
**required**: referee assignments, box score
**default**: regular season only
**constraints**: at least 10 games
**bias interpretation**: higher values = stricter on said entity?
**SQL mapping**:
```sql
-- player
SELECT AVG(sl.fouls) AS fouls_per_game
FROM stat_lines sl
JOIN games g ON sl.game_id = g.game_id
JOIN referee_assignments ra ON g.game_id = ra.game_id
WHERE sl.player_id = ... AND ra.referee_id = ...

-- team
SELECT AVG(CASE WHEN g.home_team_id = ... THEN g.home_fouls WHEN g.away_team_id = ... THEN g.away_fouls END) as ppg
FROM games g
JOIN referee_assignments ra ON g.game_id = ra.game_id
WHERE (g.home_team_id = ... OR g.away_team_id = ...) AND ra.official_code = ...
```

## metric: fouls_drawn_per_game
**description**: fouls drawn by an entity when officiated by some referee
**aliases**: "fouls drawn", "fouls given"
**formula**: total fouls drawn $\div$ games
**grain**: player-game
**valid entities**: player, team, referee
**required**: referee assignments, box score
**default**: regular season only
**constraints**: at least 10 games played
**bias interpretation**: higher values = better whistle?
**SQL mapping**:
```sql
-- player
SELECT AVG(sl.fouls_drawn) AS fouls_drawn_per_game
FROM stat_lines sl
JOIN referee_assignments ra ON sl.game_id = ra.game_id
WHERE ra.official_code = ... AND sl.player_id = ...

-- team
SELECT AVG(team_fouls_drawn) as fouls_drawn_per_game
FROM (
    SELECT g.game_id, SUM(sl.fouls_drawn) AS team_fouls_drawn
    FROM stat_lines sl
    JOIN games g ON sl.game-id = g.game_id
    WHERE sl.team_id = ...
    GROUP BY g.game_id
) sub
JOIN referee_assignments ra ON sub.game_id = ra.game_id
WHERE ra.official_code = ...
```