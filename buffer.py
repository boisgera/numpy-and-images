# %% [markdown]
# Buffers
# ==============================================================================
#
# TODO: bytes, numpy arrays, memoryview, etc. "Buffer-like" testable?
#
# References: 
# 
#   - <https://docs.python.org/3/c-api/buffer.html> (Python C API)
#
# Same stuff in PEP or doc of memoryview: this is the C API, too low-level ...
# 
# More high-level:
#
#   - <https://docs.python.org/3/library/stdtypes.html?highlight=memoryview#memoryview>
#
# NOTA: AFAICT, there is no `buffer` interface testable with `isinstance`.
# The "bufferness" can be tested by calling memoryview directly ...

# %%
memoryview(1)
# %% [markdown]
# raises `TypeError: memoryview: a bytes-like object is required, not 'int'`

# %%
memoryview(b"ABC") # OK!
# %%
from numpy import array
memoryview()