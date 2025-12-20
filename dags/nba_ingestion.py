from airflow.sdk import dag, task
from airflow.exceptions import AirflowSkipException
from datetime import datetime
from database import Database
from transformation import NBADataManager
from settings import SEASONS
from random import random, randint
import time

@dag(
    dag_id='nba_ingestion',
    start_date=datetime.today(),
    schedule=None,
    catchup=False
)
def nba_data_pipeline():
    @task
    def state_discovery():
        db = Database()
        db.cursor.execute('SELECT max(game_date) FROM games;')
        latest_date = db.cursor.fetchone()
        db.close()

        if latest_date[0] is None:
            return None
        return latest_date

    @task
    def structural_ingestion(latest_date):
        db = Database()
        dm = NBADataManager()
        if latest_date is None: # cursor at origin
            season = SEASONS[0] 
        else:
            db.cursor.execute(f'SELECT season_id FROM games WHERE game_date = %s LIMIT 1;', (latest_date))
            season = db.cursor.fetchone()[0]
            if season is None:
                season = SEASONS[0]
        

        i_start = SEASONS.index(season[1:])

        # latest_date being None will just return the entire season -> implicit bootstrap
        for s in SEASONS[i_start:]:
            rs_games_df = dm._get_games(s, 'Regular Season', latest_date)
            time.sleep(random() + randint(1,2))

            if rs_games_df.empty:
                continue

            db.insert(rs_games_df, "games")
            db.commit_changes()

            po_games_df = dm._get_games(s, 'Playoffs', latest_date)
            time.sleep(random() + randint(1,2))

            if po_games_df.empty:
                continue

            db.insert(po_games_df, "games")
            db.commit_changes()

            players_df = dm._get_players(s)
            time.sleep(random() + randint(1,2))
            db.insert(players_df, "players")
            db.commit_changes()

        db.close()
    

    @task
    def fact_ingestion():
        db = Database()
        dm = NBADataManager()
        db.cursor.execute('SELECT games.game_id FROM games WHERE (NOT EXISTS (SELECT stat_lines.game_id FROM stat_lines WHERE games.game_id = stat_lines.game_id) OR NOT EXISTS (SELECT referee_assignments.game_id FROM referee_assignments WHERE games.game_id = referee_assignments.game_id));')
        game_ids = db.cursor.fetchall()
        if not game_ids:
            raise AirflowSkipException("No games in need of fact ingestion, skipping task.")
        else:
            for game_id in game_ids:
                ref_df = dm._get_refs(game_id)
                time.sleep(random() + randint(1,2))
                sl_df = dm._get_stat_lines(game_id)
                time.sleep(random() + randint(1,2))
                ra_df = dm._get_ref_assignments(game_id)
                time.sleep(random() + randint(1,2))

                db.insert(ref_df, "referees")
                db.insert(sl_df, "stat_lines")
                db.insert(ra_df, "referee_assignments")
                db.commit_changes()

        db.close()

    state_discovery >> structural_ingestion >> fact_ingestion