import mysql.connector
from mysql.connector import Error

# Function to schedule a game between two teams
def schedule_game(away_team_id, home_team_id, date):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='',
                                             user='',
                                             password='')

        if connection.is_connected():
            cursor = connection.cursor()
            # Check if both away_team_id and home_team_id exist in the "TEAM" table
            cursor.execute(f"SELECT * FROM Baseball_League.TEAM WHERE Team_ID IN ({away_team_id}, {home_team_id})")
            teams = cursor.fetchall()
            if len(teams) != 2:
                print("One or both of the teams do not exist.")
                return

            # Create a new entry in the "GAME" table
            cursor.execute(f"INSERT INTO Baseball_League.GAME (ATeam_ID, HTeam_ID, Date) VALUES ({away_team_id}, {home_team_id}, '{date}')")
            game_id = cursor.lastrowid

            connection.commit()
            print("Game scheduled successfully.")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to lookup a player's salary based on their player_ID
def lookup_player_salary(player_id):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='',
                                             user='',
                                             password='')

        if connection.is_connected():
            cursor = connection.cursor()
            # Check if the player_ID exists in the "PLAYER" table
            cursor.execute(f"SELECT * FROM Baseball_League.PLAYER WHERE Player_ID = {player_id}")
            player = cursor.fetchone()
            if not player:
                print("Player does not exist.")
                return

            # Query the "CONTRACT" table for the salary associated with the provided player_ID
            cursor.execute(f"SELECT Salary FROM Baseball_League.CONTRACT WHERE Player_ID = {player_id}")
            salary = cursor.fetchone()[0]

            print(f"The player's salary is ${salary}")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to lookup umpires working a game given a game_Id
def lookup_umpires_for_game(game_id):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='',
                                             user='',
                                             password='')

        if connection.is_connected():
            cursor = connection.cursor()
            # Check if the game_Id exists in the "GAME" table
            cursor.execute(f"SELECT * FROM Baseball_League.GAME WHERE Game_ID = {game_id}")
            game = cursor.fetchone()
            if not game:
                print("Game does not exist.")
                return

            # Query the "WORKS" table for umpire_ids associated with the provided game_Id
            cursor.execute(f"SELECT Umpire_ID FROM Baseball_League.WORKS WHERE Game_ID = {game_id}")
            umpire_ids = cursor.fetchall()

            if not umpire_ids:
                print("No umpires assigned to this game.")
                return

            # Retrieve umpire information from the "UMPIRE" table using the retrieved umpire_ids
            umpires = []
            for umpire_id in umpire_ids:
                cursor.execute(f"SELECT * FROM Baseball_League.UMPIRE WHERE Umpire_ID = {umpire_id[0]}")
                umpire = cursor.fetchone()
                umpires.append(umpire)

            print("Umpires working the game:")
            for umpire in umpires:
                print(f"{umpire[3]}")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Example usage
schedule_game(away_team_id=1, home_team_id=2, date='2024-06-15')
lookup_player_salary(player_id=1)
lookup_umpires_for_game(game_id=1)
