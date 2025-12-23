import psycopg2
import os
from settings import *
from psycopg2 import extras
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("Couldn't connect to database:", e)
            exit()

    def create_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS referees(official_code VARCHAR(20) PRIMARY KEY, name VARCHAR(100) NOT NULL, UNIQUE(name));")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS teams(team_id INTEGER PRIMARY KEY, team_name VARCHAR(100) NOT NULL, team_abbreviation VARCHAR(10) NOT NULL);")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS players(player_id INTEGER PRIMARY KEY, first_name VARCHAR(100), last_name VARCHAR(100), team_id INTEGER REFERENCES teams(team_id));")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS games(game_id VARCHAR(20) PRIMARY KEY, game_date DATE, season_id VARCHAR(10), season_type VARCHAR(20), home_team_id INTEGER REFERENCES teams(team_id), away_team_id INTEGER REFERENCES teams(team_id), home_score INTEGER, away_score INTEGER, home_fouls INTEGER, away_fouls INTEGER);")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS stat_lines(game_id VARCHAR(20) REFERENCES games(game_id), team_id INTEGER REFERENCES teams(team_id), player_id INTEGER REFERENCES players(player_id), minutes VARCHAR(10), fg_made INTEGER, fg_attempted INTEGER, ft_made INTEGER, ft_attempted INTEGER, o_reb INTEGER, d_reb INTEGER, assists INTEGER, steals INTEGER, blocks INTEGER, turnovers INTEGER, fouls INTEGER, points INTEGER, plus_minus INTEGER, fouls_drawn INTEGER, PRIMARY KEY(game_id, player_id));")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS referee_assignments(game_id VARCHAR(20) REFERENCES games(game_id), official_code VARCHAR(20) REFERENCES referees(official_code), PRIMARY KEY(game_id, official_code));")
        
    def insert(self, df, table):
        rows = [tuple(x) for x in df.to_numpy()]
        cols = ','.join(list(df.columns))
        query = "INSERT INTO %s(%s) VALUES %%s ON CONFLICT DO NOTHING" % (table, cols)

        extras.execute_values(self.cursor, query, rows)

    def commit_changes(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
        
    def drop_all_tables(self):
        self.cursor.execute("DROP TABLE IF EXISTS referee_assignments, stat_lines, games, players, teams, referees;")

test = Database() 
test.create_tables()
