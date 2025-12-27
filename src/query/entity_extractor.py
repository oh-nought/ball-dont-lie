from typing import Dict, Optional
from models import Entity

class EntityExtractor:
    def __init__(self, db):
        self.db = db
        self.referees: Dict[str, Entity] = {}
        self.teams: Dict[str, Entity] = {}
        self.players: Dict[str, Entity] = {}

    def _load_entities(self):
        cursor = self.db.cursor

        cursor.execute("SELECT * FROM referees;")
        referee_list = cursor.fetchall() # returns in format [..., (official_code, name), ...]
        for id, name in referee_list:
            self.referees[name.lower()] = Entity("referee", id, name)
        
        cursor.execute("SELECT * FROM teams;")
        team_list = cursor.fetchall()
        for id, name, city, abbreviation in team_list:
            full_team_name = f"{city} {name}"
            team_entity = Entity("team", id, name)
            self.teams[full_team_name.lower()] = team_entity
            self.teams[name.lower()] = team_entity
            if city.lower() not in ["la", "los angeles"]: # addresses edge case in whcih 
                self.teams[city.lower()] = team_entity
            self.teams[abbreviation.lower()] = team_entity

        cursor.execute("SELECT * FROM players;")
        player_list = cursor.fetchall()
        first_name_n = {}
        last_name_n = {}
        for id, f_name, l_name, team_id in player_list:
            # counts how many times first/last names occur
            # will allow for parsing of "LeBron" or "Adebayo"
            first_name_n[f_name.lower()] = first_name_n.get(f_name.lower(), 0) + 1
            last_name_n[l_name.lower()] = last_name_n.get(l_name.lower(), 0) + 1
    
        for id, f_name, l_name, team_id in player_list:
            full_name = f"{f_name} {l_name}"
            player_entity = Entity("player", id, full_name)
            self.players[full_name.lower()] = player_entity
            # only one occurrence of first/last name = unique enough to be queried alone
            # will save headaches later :)
            if first_name_n[f_name.lower()] == 1:
                self.players[f_name.lower()] = player_entity
            if last_name_n[l_name.lower()] == 1:
                self.players[l_name.lower()] = player_entity

    def extract(self, query):
        query = query.lower()

        result = {
            "referee": [],
            "team": [],
            "player": []
        }

        all_entities = {
            **self.referees,
            **self.teams,
            **self.players
        }

        aliases = sorted(all_entities.keys(), key=len, reverse=True)
        for alias in aliases:
            entity = all_entities[alias]

            if alias in query:
                if entity not in result[entity.entity_id]:
                    result[entity.entity_type].append(entity)
                query = query.replace(alias, "", 1)

        return result