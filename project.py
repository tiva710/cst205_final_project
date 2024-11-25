#################
#Header Shtuff 
#test comment 
#################
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap5
from PIL import Image
import json
import requests

#I am assuming we will have the image generation be done once we initially get the 
#'correct' player for that round. Then we could save the image in the same place and have 
#the same route for it everytime for the hint_image variable... right? 


app = Flask(__name__)
bootstrap = Bootstrap5(app)

hint_showing = False

@app.route('/')
def home(): 
   #IMAGE SRC HERE 
  global hint_showing
  if hint_showing == True: 
    hint_image = 'https://upload.wikimedia.org/wikipedia/commons/6/6a/JavaScript-logo.png' 
  else:
     hint_image = None
  return render_template ('index.html', hint_image=hint_image)


@app.route('/show_hint', methods=['POST'])
def show_hint():
  global hint_showing

  hint_showing = not hint_showing

  return redirect(url_for('home'))
 

if __name__ == '__main__':
    app.run(debug=True)


