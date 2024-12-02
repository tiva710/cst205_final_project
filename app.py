# # from flask import Flask, render_template

# # app = Flask(__name__)

# # players = [
# #     {
# #         "name": "Lionel Messi",
# #         "team": "Inter Miami",
# #         "position": "Forward",
# #         "nationality": "Argentina",
# #         "league": "MLS",
# #         "age": 36
# #     },
# #     {
# #         "name": "Cristiano Ronaldo",
# #         "team": "Al-Nassr",
# #         "position": "Forward",
# #         "nationality": "Portugal",
# #         "league": "Saudi Pro League",
# #         "age": 38
# #     },
# # ]


# # ##Function calculate how close age is with color
# # def age_closeness(age1, age2):
# #     difference = abs(age1 - age2)
# #     if difference == 0:
# #         return "green"
# #     elif difference <= 2:
# #         return "yellow"
# #     else:
# #         return "red"
    

# # def compare_players(player1, player2):
# #     comparison = []
# #     for key in player1.keys():
# #         if player1[key] == player2[key]:  
# #             comparison.append({"attribute": key, "player1": player1[key], "player2": player2[key], "color": "green"})
# #         elif key == "age":  
# #             color = age_closeness(player1[key], player2[key])
# #             comparison.append({"attribute": key, "player1": player1[key], "player2": player2[key], "color": color})
# #         else: 
# #             comparison.append({"attribute": key, "player1": player1[key], "player2": player2[key], "color": "red"})
# #     return comparison


# # @app.route("/")
# # def index():
# #     # Compare the two players
# #     player1 = players[0]
# #     player2 = players[1]
# #     comparison = compare_players(player1, player2)
# #     return render_template("index.html", comparison=comparison, player1=player1["name"], player2=player2["name"])

# # if __name__ == "__main__":
# #     app.run(debug=True)



# ##First function that compares data and says different or same

# # def compare_players(player1, player2):
# #     print(f"Comparing {player1['name']} and {player2['name']}:")

# #     for key in player1.keys():
# #         if player1[key] == player2[key]:
# #             print(f" - Same {key}: {player1[key]}")
# #         else:
# #             print(f" - Different {key}: {player1[key]} vs {player2[key]}")
    
# # player1 = players[0]
# # player2 = players[1]


# # compare_players(player1, player2)


# from flask import Flask, render_template

# app = Flask(__name__)

# class SoccerPlayer:
#     def __init__(self, name, team, position, nationality, jersey_number):
#         self.name = name
#         self.team = team
#         self.position = position
#         self.nationality = nationality
#         self.jersey_number = jersey_number

# # Sample players
# players = [
#     SoccerPlayer("Lionel Messi", "Inter Miami", "Forward", "Argentina", 10),
#     SoccerPlayer("Cristiano Ronaldo", "Al-Nassr", "Forward", "Portugal", 7),
#     SoccerPlayer("Kylian Mbappe", "Paris Saint-Germain", "Forward", "France", 7),
#     SoccerPlayer("Kevin De Bruyne", "Manchester City", "Midfielder", "Belgium", 17),
#     SoccerPlayer("Virgil van Dijk", "Liverpool", "Defender", "Netherlands", 4)
# ]



# @app.route("/")
# def index():
#     return render_template("index.html", players=players)


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request
import random

app = Flask(__name__)


class Player:
    def __init__(self, name, position, team, goals, assists, age, nationality, league):
        self.name = name
        self.position = position
        self.team = team
        self.goals = goals
        self.assists = assists
        self.age = age
        self.nationality = nationality
        self.league = league


def safe_int(value):
    try:
        return int(value)
    except ValueError:
        return 0  

#load players from top_players.txt
def load_players(file_path):
    players = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        player_data = {}
        for line in lines:
            line = line.strip()
            if line.startswith("Name:"):
                player_data['name'] = line.split(":")[1].strip()
            elif line.startswith("Position:"):
                player_data['position'] = line.split(":")[1].strip()
            elif line.startswith("Team:"):
                player_data['team'] = line.split(":")[1].strip()
            elif line.startswith("Goals:"):
                player_data['goals'] = safe_int(line.split(":")[1].strip())
            elif line.startswith("Assists:"):
                player_data['assists'] = safe_int(line.split(":")[1].strip())
            elif line.startswith("Age:"):
                player_data['age'] = safe_int(line.split(":")[1].strip())
            elif line.startswith("Nationality:"):
                player_data['nationality'] = line.split(":")[1].strip()
            elif line.startswith("League:"):
                player_data['league'] = line.split(":")[1].strip()
            elif line.startswith("----------------------------------------"):
                
                if player_data:
                    players.append(
                        Player(
                            player_data['name'], player_data['position'], player_data['team'],
                            player_data['goals'], player_data['assists'], player_data['age'],
                            player_data['nationality'], player_data['league']
                        )
                    )
                    player_data = {}
    return players

# Load players from the file
players = load_players("top_players.txt")

# Choose a random player
chosen_player = random.choice(players)

@app.route('/')
def home():
    return render_template('guess.html', players=players)

@app.route('/submit_guess', methods=['POST'])
def submit_guess():
    guessed_player_name = request.form['player_name']
    guessed_player = next((p for p in players if p.name == guessed_player_name), None)

    if not guessed_player:
        return "Player not found!", 400

    # Compare guessed player with the chosen player
    feedback = compare_guess(chosen_player, guessed_player)

    
    return render_template('feedback.html', guessed_player=guessed_player, chosen_player=chosen_player, feedback=feedback)

def compare_guess(chosen_player, guessed_player):
    feedback = [
        ("Player Name", guessed_player.name, "Match" if guessed_player.name == chosen_player.name else "Incorrect"),
        ("Position", guessed_player.position, "Match" if guessed_player.position == chosen_player.position else "Incorrect"),
        ("Team", guessed_player.team, "Match" if guessed_player.team == chosen_player.team else "Incorrect"),
        ("Goals", guessed_player.goals, "Match" if guessed_player.goals == chosen_player.goals else "Incorrect"),
        ("Assists", guessed_player.assists, "Match" if guessed_player.assists == chosen_player.assists else "Incorrect"),
        ("Age", guessed_player.age, "Match" if guessed_player.age == chosen_player.age else "Incorrect"),
        ("Nationality", guessed_player.nationality, "Match" if guessed_player.nationality == chosen_player.nationality else "Incorrect"),
        ("League", guessed_player.league, "Match" if guessed_player.league == chosen_player.league else "Incorrect")
    ]
    return feedback

if __name__ == '__main__':
    app.run(debug=True)
