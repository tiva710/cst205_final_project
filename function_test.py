import requests
from PIL import Image

# We ran into an issue where the images provided by the api were given as URL's and needed
# to find a way to convert these URL images into pillow images for our silhouette function.
# 
# Research Citations :
# https://janakiev.com/blog/python-pilow-download-image/ 
# https://requests.readthedocs.io/en/latest/user/advanced/#body-content-workflow


filepath = 
url = "https://images.unsplash.com/photo-1465056836041-7f43ac27dcb5?w=720"

r = requests.get(url)
if r.status_code == 200:
    with open(filepath, 'wb') as f:
        f.write(r.content)
