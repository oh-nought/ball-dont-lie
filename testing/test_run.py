from transformation import NBADataManager
from database import Database
from datetime import datetime
from settings import *
from psycopg2.errors import ForeignKeyViolation
import pandas as pd
import time
from random import random, randint

# dm = NBADataManager()


# def get_latest_date():
db = Database()
dm = NBADataManager()

def state_discovery():
    db.cursor.execute('SELECT max(game_date) FROM games;')
    latest_date = db.cursor.fetchone()

    if latest_date[0] is None:
        return None
    return latest_date


def structural_ingestion(latest_date):
    if latest_date is None: # cursor at origin
        season = SEASONS[0] 
    else:
        db.cursor.execute(f'SELECT season_id FROM games WHERE game_date = %s LIMIT 1;', (latest_date))
        season = db.cursor.fetchone()[0][1:] # seasons are stored as '22025' <- extra 2 in front

        if season is None:
            season = SEASONS[0]
    
    teams_df = dm._get_teams()
    db.insert(teams_df, 'teams')
    db.commit_changes()

    players_df = dm._get_players()
    db.insert(players_df, "players")
    db.commit_changes()


    i_start = SEASONS.index(season)

    # latest_date being None will just return the entire season -> implicit bootstrap
    for s in SEASONS[i_start:]:
        games_df = dm._get_games(s, latest_date)

        if games_df.empty:
            continue

        db.insert(games_df, "games")
        db.commit_changes()
        time.sleep(random() + randint(1,2))
    
    print('Successfully ingested structural tables.')

def fact_ingestion():
    db.cursor.execute('SELECT games.game_id FROM games WHERE (NOT EXISTS (SELECT stat_lines.game_id FROM stat_lines WHERE games.game_id = stat_lines.game_id) OR NOT EXISTS (SELECT referee_assignments.game_id FROM referee_assignments WHERE games.game_id = referee_assignments.game_id));')
    game_ids = db.cursor.fetchall()
    if not game_ids:
        print('no games cro')
    else:
        for game_id in game_ids:
            print(f"working on {game_id}.....")
            ref_df, ra_df, sl_df = dm._get_game_facts(game_id)

            db.insert(ref_df, "referees")
            missing_players = dm._handle_missing_players(sl_df)
            if missing_players:
                print(f"Found {len(missing_players)} missing player(s) in {game_id}: {missing_players}")
            for player in missing_players:
                db.cursor.execute("INSERT INTO players(player_id, first_name, last_name, team_id) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;", (player, "Unknown", "Unknown", 0))
            db.insert(sl_df, "stat_lines")
            db.insert(ra_df, "referee_assignments")
            db.commit_changes()
            time.sleep(random() + randint(1,2))

    print('Successfully ingested fact tables.')

# db.drop_all_tables()
# db.create_tables()
# db.commit_changes()
ld = state_discovery()
structural_ingestion(ld)
fact_ingestion()
db.close()