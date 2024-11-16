#################
#Header Shtuff 
#test comment 
#################
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from PIL import Image
import json
import requests


app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/')
def home():
  return render_template ('index.html')
