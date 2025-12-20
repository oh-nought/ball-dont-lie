## metric: fouls_called_per_game
**description**: average number of fouls called by a referee per game
**aliases**: foul calls per game, foul rate
**formula**: total fouls called $\div$ games officiated
**grain**: referee-game
**valid entities**: referee
**required**: referee assignments, game box scores
**default**: regular season only
**constraints**: at least 10 games officiated
**bias interpretation**: higher values = stricter?

## metric: free_throw_attempts_allowed
**description**: average number of free throw attempts allowed to an entity officiated by some referee
**aliases**: fta, free throw attempts
**formula**: total free throw attempts $\div$ games
**grain**: team-game, player-game
**valid entities**: team, player, referee (via team/player games)
**required**: referee assignments, game box score
**default**: regular season only
**constraints**: at least 10 games 
**bias interpretation**: higher value = better whistle?

## metric: field_goal_attempts_allowed
**description**: average number of field goal attempts allowed to an entity officiated by some referee
**aliases**: fga, field goal attempts
**formula**: total field goal attempts $\div$ games
**grain**: team-game, player-game
**valid entities**: team, player, referee (via team/player games)
**required**: referee assignments, game box score
**default**:regular season only
**constraints**: at least 10 games
**bias interpretation**: mostly contextual

## metric: home_team_win_rate
**description**: winning percentage of home teams in games officiated by some referee
**aliases**: home win percentage, home team win %
**formula**: home team wins $\div$ games
**grain**: referee-game
**valid entities**: referee
**required**: referee assignments, box score
**default**: regular season only
**constraints**: at least 10 games officiated
**bias interpretation**: higher value = home team favoritism?

## metric: home_team_point_differential
**description**: average point differential in games officiated by some referee
**aliases**: home point differential, home point margin
**formula**: (home points - away points) $\div$ games
**grain**: referee-game
**valid entities**: referee
**required**: referee assignments, box score
**default**: regular season only
**constraints**: at least 10 games officiated
**bias interpretation**: consistent positive values = home team favoritism?

## metric: foul_rate_against_home_teams
**description**: percentage of total fouls in a game that are called against the home team
**aliases**: home team foul rate, fouls on home team
**formula**: fouls against home team $\div$ total fouls in game
**grain**: referee-game
**valid entities**: referee
**required**: referee assignments, box score
**default**: regular season only
**constraints**: at least 10 games officiated
**bias interpretation**: lower value = home team has better whistle? 

## metric: combined_points_per_game
**description**: average combined points scored in games officiated by some referee
**aliases**: total points per game, combined points
**formula**: (homw points + away points) $\div$ games
**grain**: referee-game
**valid entities**: referee
**required**: referee assignments, box score
**default**:regular season only
**constraints**: at least 10 games officiated
**bias interpretation**: mostly contextual

## metric: points_per_game
**description**: average points scored per game by an entity officiated by some referee
**aliases**: total points per game, combined points
**formula**: total points $\div$ games
**grain**: team-game, player-game
**valid entities**: player, team
**required**: referee assignments, box score
**default**:regular season only
**constraints**: at least 10 games
**bias interpretation**: mostly contextual

## metric: home_away_foul_differential
**description**: difference between fouls against road teams and fouls against home teams
**aliases**: home-away foul differential, home vs road fouls
**formula**: fouls against road teams - fouls against home teams
**grain**: referee-game
**valid entities**: referee
**required**: referee assignments, box score
**default**:regular season only
**constraints**: at least 10 games officiated
**bias interpretation**: positive value = favor home teams? negative value = favor road teams? 

## metric: fouls_committed_per_game 
**description**: fouls committed by an entity when officiated by some referee
**aliases**: fouls committed, fouls per game
**formula**: total fouls committed $\div$ games 
**grain**: team-game, player-game
**valid entities**: player, team, referee
**required**: referee assignments, box score
**default**: regular season only
**constraints**: at least 10 games
**bias interpretation**: higher values = stricter on said entity?

## metric: fouls_drawn_per_game
**description**: fouls drawn by an entity when officiated by some referee
**aliases**: fouls drawn, fouls given
**formula**: total fouls drawn $\div$ games
**grain**: player-game
**valid entities**: player, team, referee
**required**: referee assignments, box score
**default**: regular season only
**constraints**: at least 10 games played
**bias interpretation**: higher values = better whistle?