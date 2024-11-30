import requests
import io
from PIL import Image
from project import silohouette

# We ran into an issue where the images provided by the api were given as URL's and needed
# to find a way to convert these URL images into pillow images for our silhouette function.
# 
# Research Citations :
# https://janakiev.com/blog/python-pilow-download-image/ 
# https://requests.readthedocs.io/en/latest/user/advanced/#body-content-workflow

#This function simply uses requests to download an image from a specified url
# Saves the image to specified file path (I could modify to make our static/image folder default)
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
        


#Prototype function for downloading image, opening as a pillow object, and doing silhouette at the same time       
def download_and_save_pillow_image(url, filepath):
    try:
        # Send HTTP request to get the image content in stream mode
        r = requests.get(url, stream=True)

        # Check if the request was successful
        if r.status_code == 200:
            
            # Open the image with pillow using io byte content
            # https://janakiev.com/blog/python-pilow-download-image/ 
            # https://requests.readthedocs.io/en/latest/user/advanced/#body-content-workflow    
            img = Image.open(io.BytesIO(r.content))
            
            #------------- silhouette functionality here I think --------------
            
            img.save(filepath)
    
    except:
        print("Error finding image")

# Testing download image
filepath = '/Users/kevincrapo/Documents/GitHub/cst205_final_project/static/images/image.jpg'
url = 'https://media.api-sports.io/football/players/154.png'

download_image(url=url,filepath=filepath)



