# Jupyter Notebook (percent format)

# %%
from numpy import *
from PIL import Image

# %%
path = "images/mike-dorner-sf_1ZDA1YFw-unsplash.jpg"
image = Image.open(path)
image

# %% [markdown]
# ## Images as arrays
# %%
im_array = array(image)
im_array

# %%

# TODO: shape + data type + raw data (buffer/bytes)
print(f"shape: {im_array.shape}")
print(f"data type: {im_array.dtype}")
print(f"memory view: {memoryview(im_array)}")
# Nota: memory views (https://docs.python.org/3/library/stdtypes.html?highlight=memory%20view#memoryview) 
# are interesting but this is probably too technical,
# since they retain info about so many things (item size,
# nesting, etc.). (Nota: memoryview creates a *buffer* from
# the array, that's the buffer that is still rich).

# A simple substitute is the bytes representation I guess.
# There are probably caveats (for strided data, wrt byte ordering
# and more ?)
raw_data = im_array.tobytes()[:100]
print(f"data (raw): {raw_data}...")
# TODO: exercise to tweak independently each attribute:
# reshape, change of data type, change of raw data.


# %% [markdown]
# Create an array, get its components (shape, dtype and
# bytes), then build it back. (this is simplified, arrays
# are more complex but forget it for now).
# %%
a = array([[1, 2, 3], [4, 5, 6]], dtype=uint8)
data = a.tobytes() # bytes ("buffer"-like) 
shape_ = a.shape
dtype_ = a.dtype
frombuffer(data, dtype=dtype_).reshape(shape_)

# %%
bytes_ = im_array.tobytes()
print(len(bytes_))
#print(bytes_) # That would be sooo slow; don't.
print(bytes_[:100])
print(bytes_[0])

# %% [markdown] 
# ### Display an image array
# **TODO:** details about the conversion
# %%
Image.fromarray(im_array)
# %%


# TODO: use of colormaps for floating-point values ???