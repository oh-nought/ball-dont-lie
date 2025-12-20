## entity: referee
**description**: nba official asssigned to officiate a game
**aliases**: official, ref, referee, their name
**primary key**: referee_id
**attributes**: name
**valid metrics**: fouls_per_game, home_team_win_rate, home_team_point_differential, foul_rate_against_home_teams, home_away_foul_differential, combined_points_per_game
**constraints**: at least one game officiated

## entity: player
**description**: nba player
**aliases**: their name, common nicknames
**primary key**: player_id
**attributes**: team_id
**valid metrics**: fouls_drawn_per_game, fouls_committed_per_game, free_throw_attempts_allowed, field_goal_attempts_allowed, points_per_game
**constraints**: tbd

## entity: team
**description**: nba franchise
**aliases**: team name, city name, abbreviation, maybe nickname?
**primary key**: team_id
**attributes**: None
**valid metrics**: free_throw_attempts_allowed, field_goal_attempts_allowed, fouls_committed_per_game, fouls_drawn_per_game
**constraint**: tbd