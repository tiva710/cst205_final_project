import requests

# Replace Here if u want to use a different key
api_key = 'ad24ab0e4af27534f6451c76bbd7f140'

# Function to call the API and get players data. Allows dynamic endpoints/params
def call_api(endpoint, params=None):
    if params is None:
        params = {}

    # Base URL for the API
    base_url = 'https://v3.football.api-sports.io/'
    url = f'{base_url}{endpoint}'
    
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': 'v3.football.api-sports.io'  
    }

    # Send GET request to the API
    response = requests.get(url, headers=headers, params=params)
    
    # Check if response is valid (refer to Api documentation for error codes)
    if response.status_code != 200:
        raise Exception(f"API request failed with code {response.status_code}")
    
    return response.json()


# Function to get the top 20 players of a league
# Apparently free users only have access to 2022 and below 
# This function takes in a league id and a static season, fetches player data using call_api
# It then parses the top 20 players information, adds it to an organized dictionary and appends 
# each dictionary to a list of player dictionaries, returns said list.

def get_top_players(league_id, season=2022):
    
    # Fetch players for the given league and season (first page)
    players_data = call_api('players/topscorers', {'league': league_id, 'season': season})
    
    # Extract player information from the response
    players = players_data.get('response', [])
    
    top_players = []
    
    # Refer to sample response below for information access logic
    for player in players:
        player_info = {
            'name': player['player']['name'],
            'team': player['statistics'][0]['games']['position'],
            'position': player['statistics'][0]['games']['position'],
            'image': player['player']['photo'], 
            'nationality': player['player']['nationality'],
            'goals': player['statistics'][0]['goals']['total'],
            'assists': player['statistics'][0]['goals']['assists'],
            'age' : player['player']['age']
        }
        
        # Append to the list
        top_players.append(player_info)
    
    return top_players

# Function for compiling results from a dictionary of league_id's     
def get_all_league_players(league_ids):
    all_league_players = {}

    for league_name, league_id in league_ids.items():
        players = get_top_players(league_id)
        all_league_players[league_name] = players
    
    return all_league_players

# Id's gathered through dashboard https://dashboard.api-football.com/soccer/ids
league_ids = {
    'English Premier League': 39,   
    'La Liga': 140,                  
    'Serie A': 135,                  
    'Bundesliga': 78,                
    'Ligue 1': 61   
    
    # More League Id's if wanted     
    # ,'Primeira Liga': 94
    # ,'Eredivisie': 88  
}

#
all_league_players = get_all_league_players(league_ids)

#Writing information to file for outputput checking
with open('top_players.txt', 'w') as file:

    # Loop through all the leagues and their respective players
    for league_name, players in all_league_players.items():
        file.write(f"\nTop Players for {league_name}:\n")
        file.write("=" * 40 + "\n")
        for player in players:
            file.write(f"Name: {player['name']}\n")
            file.write(f"Team: {player['team']}\n")
            file.write(f"Position: {player['position']}\n")
            file.write(f"Goals: {player['goals']}\n")
            file.write(f"Assists: {player['assists']}\n")
            file.write(f"Age: {player['age']}\n")
            file.write(f"Nationality: {player['nationality']}\n")
            file.write(f"Image: {player['image']}\n")
            file.write("-" * 40 + "\n")  

print("Player data has been written to top_players.txt")
    
    
    
#### This is just a sample response from the website so that i can refer to it #####
# Sample response data
response_data_sample = {
    "player": {
        "id": 625,
        "name": "P. Sandler",
        "firstname": "Philippe",
        "lastname": "Sandler",
        "age": 25,
        "birth": {
            "date": "1997-02-10",
            "place": "Amsterdam",
            "country": "Netherlands"
        },
        "nationality": "Netherlands",
        "height": "188 cm",
        "weight": "76 kg",
        "injured": False,
        "photo": "https://media.api-sports.io/football/players/625.png"
    },
    "statistics": [
        {
            "team": {
                "id": 50,
                "name": "Manchester City",
                "logo": "https://media.api-sports.io/football/teams/50.png"
            },
            "games": {
                "position": "Defender",  
                "appearances": 0,
                "lineups": 0,
                "minutes": 0,
                "number": None,
                "rating": None,
                "captain": False
            }
        }
    ]
}