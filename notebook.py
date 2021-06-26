# Jupyter Notebook (percent format)

# %%
from numpy import *
from PIL import Image

# %%
path = "images/mike-dorner-sf_1ZDA1YFw-unsplash.jpg"
image = Image.open(path)
image
# TODO: dynamically via requests? What about the image type then?

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
# Data type would need a section by itself; they key point is that in pure
# Python, it's obvious to tell what the type of numeric datum is: it's either
# int or float (or complex or bool, but you get the point), so beyond that,
# you don't need to care.
# %%
type(1)
# %%
type(1.0)

# In NumPy, there are several integer and floating-point types, and it's
# not always obvious to tell which one is used.

# %%
int64(42)

# %%
uint8(42)

# %%
float32(3.14)

# %%
float64(3.14)

# %% [markdown]
# **TODO:** Explain why several types are needed (array of fixed-size objects)
# are "easier" to deal with and lend themselves to faster operations; think
# random access for example. We need fixed-size + no dereferencing to be fast.
# Can't explain properly this here.
# **BUT** we can talk about *size* and how that would be wasteful to represent
# 
# Also say how these type differ from the corresponding python type 
# (especially for integers where things get tricky! For floating-points,
# you can consider that `float` and `float64` aka `double` are the same thing
# and forget entirely about `single` / `float32`).

# %% [markdown]
# This is very interesting how `array(i)` works when `i` is a Python `int`.
# The `array` factory tries very hard to help you to represent the integer
# without loss of information, but at the same time to keep the integer
# size small. So depending on the number it will generate `int64`, `uint64`
# or `object` data type (`object` only stores the reference to the integer,
# which is stored elsewhere).

# %% [markdown]
# Ho, fuck me, there are weird things going on :
# 
#     >>> a = array([2**64-1])
#     >>> a
#     array([18446744073709551615], dtype=uint64)
#     >>> type(a[0])
#     <class 'numpy.ulonglong'>
#     >>> uint64
#     <class 'numpy.uint64'>

# %%
a = array([2**64-1])
a

# %%
type(a[0])

# %%
uint64

# %% [markdown]
# Didactics: high-level stuff before the details: existence of "data type"
# from image examination *before* the details about data types ?
# Dunno, think of it. Probably, yes. 

# %% [markdown] 
# ### Display an image array
# **TODO:** details about the conversion
# %%
Image.fromarray(im_array)
# %%


# TODO: use of colormaps for floating-point values ???