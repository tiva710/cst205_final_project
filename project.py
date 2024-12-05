#################
#Header Shtuff 
#test comment 
#################
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap5
from PIL import Image
import json
import requests
import pickle
import random

def get_random_player_to_guess():
  with open("pickled_top_players.txt", "rb") as pickled_file:
    all_league_players = pickle.load(pickled_file)

  list_of_leagues = ['English Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1']
  random.shuffle(list_of_leagues)
  target_player = all_league_players[list_of_leagues[0]]
  random.shuffle(target_player)
  return target_player[0]

def color_distance(c1, c2):
    r_diff = (c1[0] - c2[0])**2
    g_diff = (c1[1] - c2[1])**2
    b_diff = (c1[2] - c2[2])**2
    return (r_diff + g_diff + b_diff)**(1/2)


def silohouette(src, refp):
    src = Image.open(src).convert("RGBA")
    for x in range(src.width):
        for y in range(src.height):
            cur_pixel = src.getpixel((x,y))
            if color_distance(cur_pixel, refp) <= 75:
                src.putpixel((x,y), (255, 255, 255, 0))
            else:
                src.putpixel((x,y), (0, 0, 0, 255))
    src.save("static/images/silohouette.png", "PNG")

def download_image(url, filepath):
    try:
        r = requests.get(url)

        # Check if the request was successful
        if r.status_code == 200:
            
            # Save the image content to filepath
            with open(filepath, 'wb') as f: 
                f.write(r.content)
                
    except:
        print("Error finding image")


#I am assuming we will have the image generation be done once we initially get the 
#'correct' player for that round. Then we could save the image in the same place and have 
#the same route for it everytime for the hint_image variable... right? 


app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/')

def home(): 
  guess_this_player = get_random_player_to_guess()
  with open("pickled_top_players.txt", "rb") as pickled_file:
    all_league_players = pickle.load(pickled_file)
  print(guess_this_player)
    
  #Downloading player image the path for the raw image will always be 'static/images/image.png'
  download_image(guess_this_player.image,'static/images/image.png')
  
  #Silohuette saves image as "static/images/silohouette.png"
  silohouette('static/images/image.png',(255,255,255))
  
   #IMAGE SRC HERE 
 
  hint_image = "static/images/silohouette.png"
  return render_template ('index.html', hint_image=hint_image, guess_this_player=guess_this_player, dict_of_players=all_league_players)
 

if __name__ == '__main__':
    app.run(debug=True)

