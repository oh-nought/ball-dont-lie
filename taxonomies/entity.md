## entity: referee
**description**: nba official asssigned to officiate a game
**aliases**: official, ref, referee, their name
**primary key**: official_code
**attributes**: name
**relationships**: 
    - officiates: games (referee_assignments)
    - works_with: other referees (not sure if I want this yet)
**valid metrics**:
    - fouls_per_game
    - home_team_win_rate
    - home_team_point_differential
    - foul_rate_against_home_teams
    - home_away_foul_differential
    - combined_points_per_game
    - fouls_committed_per_game
    - fouls_drawn_per_game
**constraints**: 
    - at least one game officiated
    - must exist in referee_assignments for queried time period
**edge cases**:
    - misspellings
    - retired referees

## entity: player
**description**: nba player
**aliases**:their name, common nicknames
**primary key**: player_id
**attributes**: first_name, last_name, team_id
**relationships**:
    - belongs_to: team (stat_lines.team_id)
    - plays_in: games (stat_lines)
    - officiated_by: referees (referee_assignments)
**valid metrics**: 
    - fouls_drawn_per_game
    - fouls_committed_per_game
    - free_throw_attempts_allowed
    - field_goal_attempts_allowed
    - points_per_game
**constraints**: 
    - at least one game played
    - must exist in stat_lines for queried time period
    - minimum minutes needed?
**edge cases**:
    - mid-season trades
    - players with same names
    - two way players

## entity: team
**description**: nba franchise
**aliases**: team name, city name, abbreviation, maybe nickname?
**primary key**: team_id
**attributes**: 
    - team_name
    - city_name
    - team_abbreviation
    - nickname maybe
**relationships**:
    - has: players (players.team_id)
    - plays: games (games)
    - officiated_by: referees (referee_assignments)
**valid metrics**: 
    - free_throw_attempts_allowed
    - field_goal_attempts_allowed
    - fouls_committed_per_game
    - fouls_drawn_per_game
    - points_per_game
    - home_team_win_rate
    - home_team_point_differential
**constraint**: 
    - team must be active in queried season
**edge cases**:
    - historical teams
    - relocations
    - lakes/clips city name

## entity: game
**description**: single nba game between two teams
**aliases**: game, matchup
**primary key**: game_id
**attributes**:
    - game_date
    - season_id
    - home_team_id
    - away_team_id
    - home_score
    - away_score
**relationships**:
    - has: stat_lines (stat_lines.game_id)
    - has: referee_assignments (referee_assignments.game_id)
    - belongs_to: home_team
    - belongs_to: away_team
    - part_of: season
**valid metrics**:
    - fouls_called_per_game
    - home_away_foul_differential
    - total_free_throws_attempted
    - home_team_point_differential
    - combined_points_per_game
**constraints**:
    - game must have occurred
    - must have referee_assignments and stat_lines data
**edge cases**:
    - in season tournament shifting game schedule

## entity: season
**description**: nba season
**aliases**: "XXXX-XX season", "XXXX season", this/last season/year
**primary key**: season_id 
**attributes**: 
    - start_date
    - end_date
    - season_type
**relationships**:
    - has: games
**valid metrics**:
    - all game-level metrics that can be aggregated to season level
**constraints**:
    - season must exist in database (2003 - current)
**edge cases**:
    - off season queries