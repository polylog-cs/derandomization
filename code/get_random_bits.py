import os
import random

# Ask the OS to return 32 random bytes. Nowadays most
# OSes actually use a pseudorandom generator under the
# hood as well, although a cryptographically strong one,
# which is also continually being seeded from "truly
# random" bytes obtained by measuring hardware.
seed = os.getrandom(32, os.GRND_RANDOM)

# Use the random bytes to seed Python's simple, fast and
# cryptographically weak pseudorandom generator.
random.seed(seed)
