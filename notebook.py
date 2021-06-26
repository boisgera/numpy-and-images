# Jupyter Notebook (percent format)

# %%
from numpy import *
from PIL import Image

# %%
path = "images/mike-dorner-sf_1ZDA1YFw-unsplash.jpg"
image = Image.open(path)
im_array = array(image)
print(im_array)

# %%
Image.fromarray(im_array)