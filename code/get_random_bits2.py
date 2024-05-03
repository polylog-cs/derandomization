import os
import random

# Ask the OS to return 32 random bytes.
# There is a caveat, see video description.
seed = os.getrandom(32, os.GRND_RANDOM)

# Use the random bytes to seed Python's pseudorandom generator.
random.seed(seed)
