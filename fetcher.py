import sqlite3

# following the example of python docs given here
# https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factor
def dict_factory (cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Fetcher:
    def __init__ (self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = dict_factory

    # returns a tuple (player, player_attrs)
    # `player` is a dictionary containing the row from the Player table
    # `player_attrs` is list of dictionaries, each dictionary is the
    # row from the Player_Attributes for the player with given api_id
    # (each player has many such entries in the dictionary)
    def get_player_data (self, api_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM Player WHERE player_api_id=?", (api_id,))
        player = cur.fetchone()
        cur.execute("SELECT * FROM Player_Attributes WHERE player_api_id=?", (api_id,))
        player_attrs = cur.fetchall()
        return (player, player_attrs)

    # returns a tuple (team, team_attrs)
    # the meaning of these is the same as in get_player_data
    def get_team_data (self, api_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM Team WHERE team_api_id=?", (api_id,))
        team = cur.fetchone()
        cur.execute("SELECT * FROM Team_Attributes WHERE team_api_id=?", (api_id,))
        team_attrs = cur.fetchall()
        return (team, team_attrs)

    # returns all player_api_ids that are present in the data
    def get_player_api_ids (self):
        cur = self.conn.cursor()
        cur.execute("SELECT DISTINCT player_api_id FROM Player")
        api_ids = cur.fetchall()
        return [d['player_api_id'] for d in api_ids]

    # returns all team_api_ids that are present in the data
    def get_team_api_ids (self):
        cur = self.conn.cursor()
        cur.execute("SELECT DISTINCT team_api_id FROM Team")
        api_ids = cur.fetchall()
        return [d['team_api_id'] for d in api_ids]

    # returns everything about every match
    def get_all_matches (self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM Match")
        matches = cur.fetchall()
        return matches

    def get_leagues(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT *
                        FROM League
                        JOIN Country ON Country.id = League.country_id;""")
        return cur.fetchall()

# fetcher = Fetcher("data/database.sqlite")
