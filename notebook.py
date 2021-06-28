# Jupyter Notebook (percent format)

# %%
import numpy as np; from numpy import array
from PIL import Image
import requests

# %%
path = "images/mike-dorner-sf_1ZDA1YFw-unsplash.jpg"
image = Image.open(path)
image
# TODO: dynamically via requests? What about the image type then?

# %% [markdown]
# Download the small version of Mike Dorner's banana:
# %%
url = "https://unsplash.com/photos/sf_1ZDA1YFw/download?force=true&w=640"
request = requests.get(url, allow_redirects=True)
# %% [markdown]
# See <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition>
# %%
content_disposition = request.headers["Content-Disposition"]
assert content_disposition.startswith("attachment;filename=")
filename = content_disposition.split('"')[-2]
open(filename, "wb").write(request.content)

# TODO: use the SMALL image version.


# %% [markdown]
# ## Images as arrays
# %%
im_array = array(image)  # PIL image is "array-like"?
# Does it have the array interface ?
print("image provides an array interface ?", "__array_interface__" in dir(image))

# %%
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
a = array([[0, 1, 2], [3, 4, 5]], dtype=uint8)
shape_ = a.shape
print(shape_)
dtype_ = a.dtype
print(dtype_)
data = a.tobytes()  # bytes ("buffer"-like)
print(data)  # Here, on this special case, it's perfectly readable
# (assuming that you know how to read hexadecimal data)
frombuffer(data, dtype=dtype_).reshape(shape_)
# NOTA: framebuffer never required actually ? The `array` constructor does
# accept anything that follows the buffer protocol?
print(array(data, dtype=dtype_))
# Nope. So we need frombuffer ...

# %%
bytes_ = im_array.tobytes()
print(len(bytes_))
# print(bytes_) # That would be sooo slow; don't.
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
a = array([2 ** 64 - 1])
a

# %%
type(a[0])

# %%
uint64

# %% [markdown]
# Didactics: high-level stuff before the details: existence of "data type"
# from image examination *before* the details about data types ?
# Dunno, think of it. Probably, yes.
#
# Yeah and even simpler. Somehow, "array with types" are simpler than "types"
# (and if you really vectorize everything, you almost never get to play with
# numeric types directly, or only in situation when it does not matter).
#
# For example, mutation is far simpler with (dtyped) arrays than it is with
# scalars. **NAH, scalars are not mutable.**. Consider:
# %%
a = array([0], dtype=uint8)
a[0] = 123456789  # 123456789 "coerced" to the 0-255 range.
a
# %% [markdown]
# versus
# %%
a = uint8(0)
a += 123456789
type(a)  # Hey, a is NOT mutable, some promotion has been going on.

# %% [markdown]
# ### Display an image array
# **TODO:** details about the conversion
# %%
Image.fromarray(im_array)
# %%


# TODO: use of colormaps for arrays with floating-point values ???

# %% [markdown]
# ## Advanced Indexing

# %%
pink = im_array[0, 0]  # as sampled in top-left corner
pink
# %%

# %%
# more complex than i was expecting. Fuck ... would need to work
# on grayscale images to demonstrate it simply.
match = im_array == pink  # doesn't work as expected
# matches at the color channel level.
match = (
    (im_array[:, :, 0] == pink[0])
    * (im_array[:, :, 1] == pink[1])
    * (im_array[:, :, 2] == pink[2])
)

# %%
match_b = match.reshape(match.shape + (1,))  # UGLY HACK to make broacasting
# work in `where`!
print(match.shape)
white = array([255, 255, 255], dtype=uint8)
im_array2 = where(match_b, white, im_array).astype(uint8)
im_array2.dtype
Image.fromarray(im_array2)

# %%
