import pandas as pd
from nba_api.stats.endpoints import boxscoresummaryv3, leaguegamelog, boxscoretraditionalv3, playerindex, commonallplayers
from nba_api.stats.static import players

class NBADataManager:
    def __init__(self):
        # self.storage = storage
        # self.database = database
        pass

    def _get_teams(self):
        # nba.com's teams.get_teams() doesn't give historical teams so we improvise
        # get list of current + historical players, return unique list of teams
        player_df = playerindex.PlayerIndex(historical_nullable=1).get_data_frames()[0]
        player_df = player_df[['TEAM_ID', 'TEAM_NAME', 'TEAM_ABBREVIATION']]
        teams = player_df.values.tolist()
        teams = set(tuple(team) for team in teams)
        team_df = pd.DataFrame(teams)
        team_df.columns = ['TEAM_ID', 'TEAM_NAME', 'TEAM_ABBREVIATION']
        team_df.loc[len(team_df)] = [0, 'No Team', 'N/A']
        
        return team_df

    def _get_players(self):
        player_df = playerindex.PlayerIndex(historical_nullable=1).get_data_frames()[0]
        player_df = player_df[['PERSON_ID', 'PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'TEAM_ID']]
        player_df = player_df.rename(columns={'PERSON_ID': 'PLAYER_ID', 'PLAYER_FIRST_NAME': 'FIRST_NAME', 'PLAYER_LAST_NAME': 'LAST_NAME'})
        
        return player_df       

    def _get_games(self, season, date_from=None):
        # separate regular season and playoff dataframes and mark them as such
        rs_games_df = leaguegamelog.LeagueGameLog(season=season, season_type_all_star='Regular Season').get_data_frames()[0]
        rs_games_df['SEASON_TYPE'] = 'Regular Season'
        po_games_df = leaguegamelog.LeagueGameLog(season=season, season_type_all_star='Playoffs').get_data_frames()[0]
        po_games_df['SEASON_TYPE'] = 'Playoffs'
        games_df = pd.concat([rs_games_df, po_games_df], ignore_index=True)

        # home games will appear as '___ vs. other team', away games would show '___ @ other team'  
        home_games_df = games_df[games_df['MATCHUP'].str.contains('vs')]
        home_games_df = home_games_df.rename(columns={'TEAM_ID': 'HOME_TEAM_ID', 'PTS': 'HOME_SCORE', 'PF': 'HOME_FOULS'})
        away_games_df = games_df[games_df['MATCHUP'].str.contains('@')]
        away_games_df = away_games_df.rename(columns={'TEAM_ID': 'AWAY_TEAM_ID', 'PTS': 'AWAY_SCORE', 'PF': 'AWAY_FOULS'})
        games_df = pd.merge(home_games_df, away_games_df, on=['GAME_ID', 'GAME_DATE', 'SEASON_ID'], suffixes=('_x', None))[['GAME_ID', 'GAME_DATE', 'SEASON_ID', 'HOME_TEAM_ID', 'AWAY_TEAM_ID', 'HOME_SCORE', 'AWAY_SCORE', 'HOME_FOULS', 'AWAY_FOULS', 'SEASON_TYPE']]
        
        # international games/neutral courts have both teams as 'away', so we need to get those
        processed_ids = set(games_df['GAME_ID'])
        rs_game_ids = set(leaguegamelog.LeagueGameLog(season=season, season_type_all_star='Regular Season', date_from_nullable=date_from).get_data_frames()[0]['GAME_ID'])
        po_game_ids = set(leaguegamelog.LeagueGameLog(season=season, season_type_all_star='Playoffs', date_from_nullable=date_from).get_data_frames()[0]['GAME_ID'])

        all_ids = rs_game_ids | po_game_ids
        missing_ids = all_ids - processed_ids

        if missing_ids: 
            raw_rs_df = leaguegamelog.LeagueGameLog(season=season, season_type_all_star='Regular Season', date_from_nullable=date_from).get_data_frames()[0]
            raw_po_df = leaguegamelog.LeagueGameLog(season=season, season_type_all_star='Playoffs', date_from_nullable=date_from).get_data_frames()[0]
            raw_df = pd.concat([raw_rs_df, raw_po_df], ignore_index=True)
            neutral_df = raw_df[raw_df['GAME_ID'].isin(missing_ids)]

            # split the 2 rows (will always be two since only two teams can play in a game)
            neutral_home = neutral_df.groupby('GAME_ID').head(1).copy()
            neutral_away = neutral_df.groupby('GAME_ID').tail(1).copy()

            neutral_home = neutral_home.rename(columns={'TEAM_ID': 'HOME_TEAM_ID', 'PTS': 'HOME_SCORE', 'PF':'HOME_FOULS'})
            neutral_away = neutral_away.rename(columns={'TEAM_ID': 'AWAY_TEAM_ID', 'PTS': 'AWAY_SCORE', 'PF':'AWAY_FOULS'})

            neutral_final = pd.merge(neutral_home, neutral_away, on=['GAME_ID', 'GAME_DATE', 'SEASON_ID'])[['GAME_ID', 'GAME_DATE', 'SEASON_ID', 'HOME_TEAM_ID', 'AWAY_TEAM_ID', 'HOME_SCORE', 'AWAY_SCORE', 'HOME_FOULS', 'AWAY_FOULS']]
            games_df = pd.concat([games_df, neutral_final], ignore_index=True)

        return games_df
    
    def _get_game_facts(self, game_id):
        officials_df = boxscoresummaryv3.BoxScoreSummaryV3(game_id=game_id).officials.get_data_frame()

        referee_df = officials_df.copy()
        referee_df = referee_df[['personId', 'name']]
        referee_df = referee_df.rename(columns={'personId': 'OFFICIAL_CODE'})

        ra_df = officials_df.copy()
        ra_df = ra_df[['gameId', 'personId']]
        ra_df = ra_df.rename(columns={'gameId': 'GAME_ID', 'personId': 'OFFICIAL_CODE'})

        statline_df = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=game_id).get_data_frames()[0]
        statline_df = statline_df[['gameId', 'teamId', 'personId', 'minutes', 'fieldGoalsMade', 'fieldGoalsAttempted', 'freeThrowsMade', 'freeThrowsAttempted', 'reboundsOffensive', 'reboundsDefensive', 'assists', 'steals', 'blocks', 'turnovers', 'foulsPersonal', 'points', 'plusMinusPoints']]
        statline_df = statline_df.rename(columns={'gameId': 'GAME_ID', 'teamId': 'TEAM_ID', 'personId': 'PLAYER_ID', 'fieldGoalsMade': 'FG_MADE', 'fieldGoalsAttempted': 'FG_ATTEMPTED', 'freeThrowsMade': 'FT_MADE', 'freeThrowsAttempted': 'FT_ATTEMPTED', 'reboundsOffensive': 'O_REB', 'reboundsDefensive': 'D_REB', 'foulsPersonal': 'FOULS', 'plusMinusPoints': 'PLUS_MINUS'})

        return referee_df, ra_df, statline_df


    # addresses the edge case in which some players have ids, but for some reason are banished from nba.com's api
    def _handle_missing_players(self, sl_df):
        missing_players = []
        for row in sl_df.itertuples():
            if not players.find_player_by_id(row.PLAYER_ID):
                missing_players.append(row.PLAYER_ID)
            

        return missing_players